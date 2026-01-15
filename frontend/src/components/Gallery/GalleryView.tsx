import { useMemo, useState } from 'react';
import { useCamera } from './useCamera';
import {
  artworkZPosition,
  calculateArtworkState,
  calculateLoadingStrategy,
  calculateRunwayHeight,
  type CameraConfig,
  DEFAULT_CONFIG,
} from './calculations';
import { Artwork } from './Artwork';
import { ArtworkModal } from './ArtworkModal';
import styles from './GalleryView.module.scss';

interface ArtworkData {
  id: string;
  title: string;
  imageUrl: string;
  artistName: string;
}

interface GalleryViewProps {
  artworks: ArtworkData[];
  config?: CameraConfig;
}

/**
 * Container component for the depth camera gallery.
 * Manages scroll handling, camera state, and renders artworks with calculated visual states.
 */
export function GalleryView({
  artworks,
  config = DEFAULT_CONFIG,
}: GalleryViewProps) {
  const [selectedArtworkId, setSelectedArtworkId] = useState<string | null>(null);
  const isCameraLocked = selectedArtworkId !== null;

  const { containerRef, cameraZ, scrollProgress } = useCamera({
    artworkCount: artworks.length,
    config,
    locked: isCameraLocked,
  });

  // Calculate runway height based on artwork count
  // Using a reasonable viewport height estimate; actual will be dynamic
  const runwayHeight = useMemo(
    () => calculateRunwayHeight(artworks.length, window.innerHeight, config),
    [artworks.length, config]
  );

  // Determine offset pattern for each artwork (alternating left/right)
  const getOffsetDirection = (index: number): 'left' | 'right' | 'center' => {
    // First artwork centered, then alternate
    if (index === 0) return 'center';
    return index % 2 === 1 ? 'left' : 'right';
  };

  const handleArtworkClick = (artworkId: string) => {
    setSelectedArtworkId(artworkId);
  };

  const handleCloseModal = () => {
    setSelectedArtworkId(null);
  };

  return (
    <div className={styles.container} ref={containerRef}>
      {/* Scroll runway: creates scrollable height */}
      <div className={styles.runway} style={{ height: `${runwayHeight}px` }} />

      {/* Fixed viewport for 3D scene */}
      <div className={styles.viewport}>
        {artworks.map((artwork, index) => {
          const artworkZ = artworkZPosition(index, config);
          const visualState = calculateArtworkState(artworkZ, cameraZ, config);
          const loadingStrategy = calculateLoadingStrategy(
            index,
            artworkZ,
            cameraZ,
            artworks.length,
            config
          );

          return (
            <Artwork
              key={artwork.id}
              id={artwork.id}
              title={artwork.title}
              imageUrl={artwork.imageUrl}
              visualState={visualState}
              offsetDirection={getOffsetDirection(index)}
              loadingStrategy={loadingStrategy}
              onArtworkClick={handleArtworkClick}
            />
          );
        })}
      </div>

      {/* Progress indicator */}
      <div className={styles.progressContainer}>
        <div className={styles.progressTrack}>
          <div
            className={styles.progressFill}
            style={{ height: `${scrollProgress}%` }}
          />
        </div>
        <span className={styles.progressLabel}>
          {Math.round(scrollProgress)}%
        </span>
      </div>

      {/* Artwork Modal */}
      {selectedArtworkId && (() => {
        const selectedArtwork = artworks.find(a => a.id === selectedArtworkId);
        if (!selectedArtwork) return null;

        return (
          <ArtworkModal
            artworkId={selectedArtwork.id}
            artworkTitle={selectedArtwork.title}
            artworkImageUrl={selectedArtwork.imageUrl}
            artistName={selectedArtwork.artistName}
            onClose={handleCloseModal}
          />
        );
      })()}
    </div>
  );
}
