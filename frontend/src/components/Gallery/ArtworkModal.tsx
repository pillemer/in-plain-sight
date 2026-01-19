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
 * Layer 1: Full-screen artwork view with "View Interpretation" button
 * Layer 2: Info overlay with artwork details and AI interpretation
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
    enabled: viewMode === 'info', // Only fetch when user switches to info view
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
    // Only close if clicking the backdrop itself, not content
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  // Shared "Return to Gallery" button used in both views
  const returnButton = (
    <button className={styles.returnButton} onClick={onClose}>
      <span className={styles.returnArrow}>←</span>
      Return to Gallery
    </button>
  );

  return (
    <div className={styles.backdrop} onClick={handleBackdropClick}>
      {/* Layer 1: Artwork View */}
      {viewMode === 'artwork' && (
        <>
          {returnButton}

          <button
            className={styles.viewInterpretationButton}
            onClick={() => setViewMode('info')}
          >
            View Interpretation
          </button>

          <div className={styles.artworkView}>
            <img
              src={artworkImageUrl}
              alt={artworkTitle || 'Artwork'}
              className={styles.artworkImage}
            />
          </div>
        </>
      )}

      {/* Layer 2: Info Overlay */}
      {viewMode === 'info' && (
        <>
          {returnButton}

          <button
            className={styles.backToArtButton}
            onClick={() => setViewMode('artwork')}
          >
            <span className={styles.returnArrow}>←</span>
            Back to Art View
          </button>

          <div className={styles.infoOverlay}>
            <div className={styles.infoContent}>
              <img
                src={artworkImageUrl}
                alt={artworkTitle || 'Artwork'}
                className={styles.infoImage}
              />

              <div className={styles.infoText}>
                <div className={styles.artworkMetadata}>
                  <h2 className={styles.artworkTitle}>{artworkTitle}</h2>
                  <p className={styles.artistName}>{artistName}</p>
                  {/* Placeholder for future metadata */}
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
          </div>
        </>
      )}
    </div>
  );
}
