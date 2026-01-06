import { memo } from 'react';
import type { ArtworkVisualState } from './calculations';
import styles from './Artwork.module.scss';

interface ArtworkProps {
  id: string;
  title: string;
  imageUrl: string;
  visualState: ArtworkVisualState;
  offsetDirection: 'left' | 'right' | 'center';
}

/**
 * Stateless presentation component for a single artwork in the depth gallery.
 * Visual state (scale, opacity, position) is controlled by parent.
 * Memoized to prevent unnecessary re-renders.
 */
export const Artwork = memo(function Artwork({
  title,
  imageUrl,
  visualState,
  offsetDirection,
}: ArtworkProps) {
  const { translateZ, scale, opacity, zIndex, isVisible, isFocused } =
    visualState;

  if (!isVisible) {
    return null;
  }

  // Build inline transform style - CSS handles transitions
  const transformStyle: React.CSSProperties = {
    transform: `translateZ(${translateZ}px) scale(${scale})`,
    opacity,
    zIndex,
  };

  const offsetClass =
    offsetDirection === 'left'
      ? styles.offsetLeft
      : offsetDirection === 'right'
        ? styles.offsetRight
        : styles.offsetCenter;

  const titleClass = isFocused
    ? `${styles.title} ${styles.titleVisible}`
    : styles.title;

  return (
    <article
      className={`${styles.wrapper} ${offsetClass}`}
      style={transformStyle}
      aria-hidden={!isFocused}
    >
      <div className={styles.card}>
        <img
          src={imageUrl}
          alt={title}
          className={styles.image}
          loading="eager"
        />
        <h3 className={titleClass}>{title}</h3>
      </div>
    </article>
  );
});
