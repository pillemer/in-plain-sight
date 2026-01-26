import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { GenerateArtworkInterpretationDocument } from '../../generated/graphql';
import { graphqlClient } from '../../lib/graphqlClient';
import styles from './ArtworkModal.module.scss';

interface ArtworkModalProps {
  artworkId: string;
  artworkTitle: string;
  artworkImageUrl: string;
  artistName: string;
  onClose: () => void;
}

type ViewMode = 'artwork' | 'info';

/**
 * Two-layer modal for viewing artwork in detail.
 * Front: Full artwork image
 * Back: Artwork metadata and AI interpretation
 * Both sides share the same dimensions (determined by the image).
 */
export function ArtworkModal({
  artworkId,
  artworkTitle,
  artworkImageUrl,
  artistName,
  onClose,
}: ArtworkModalProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('artwork');

  // Only fetch AI interpretation when info overlay is requested
  const { data, isLoading, error } = useQuery({
    queryKey: ['artwork-interpretation', artworkId],
    queryFn: async () => {
      const result = await graphqlClient.request(
        GenerateArtworkInterpretationDocument,
        { artworkId }
      );

      return result.generateArtworkInterpretation;
    },
    enabled: viewMode === 'info',
  });

  // Handle ESC key to close modal
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = '';
    };
  }, []);

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={styles.backdrop} onClick={handleBackdropClick}>
      <button className={styles.returnButton} onClick={onClose}>
        <span className={styles.returnArrow}>←</span>
        Return to Gallery
      </button>

      <button
        className={styles.actionButton}
        onClick={() => setViewMode(viewMode === 'artwork' ? 'info' : 'artwork')}
      >
        {viewMode === 'info' && <span className={styles.returnArrow}>←</span>}
        {viewMode === 'artwork' ? 'View Interpretation' : 'Back to Art View'}
      </button>

      <div
        className={`${styles.card} ${viewMode === 'artwork' ? styles.cardPassthrough : ''}`}
      >
        {/* Image always rendered — determines card dimensions */}
        <img
          src={artworkImageUrl}
          alt={artworkTitle || 'Artwork'}
          className={styles.artworkImage}
        />

        {/* Info overlay — fills the card, sits on top of the image */}
        {viewMode === 'info' && (
          <div className={styles.infoOverlay}>
            <div className={styles.infoContent}>
              <div className={styles.artworkMetadata}>
                <h2 className={styles.artworkTitle}>{artworkTitle}</h2>
                <p className={styles.artistName}>{artistName}</p>
                <p className={styles.metadataPlaceholder}>
                  Watercolour on canvas, 24" × 36", 2023
                </p>
              </div>

              <div className={styles.divider} />

              <div className={styles.interpretationSection}>
                <h3 className={styles.interpretationHeading}>
                  AI Curator's Interpretation
                  <span
                    className={styles.infoIcon}
                    data-tooltip="AI-generated, may vary between views"
                  >
                    ⓘ
                  </span>
                </h3>
                {isLoading && (
                  <p className={styles.loadingText}>
                    Our AI curator is generating an interpretation just for you...
                  </p>
                )}
                {error && (
                  <p className={styles.errorText}>
                    Unable to generate interpretation at this time.
                  </p>
                )}
                {data && (
                  <p className={styles.interpretationText}>{data.content}</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
