/**
 * Pure calculation functions for depth camera gallery navigation.
 * These functions determine visual state based on camera position and artwork depth.
 */

export interface CameraConfig {
  depthGap: number;        // Distance between artworks on Z-axis
  focusZone: number;       // Distance from camera for full clarity
  maxVisible: number;      // Distance at which artwork is fully faded
  cullBehind: number;      // Distance behind camera to stop rendering
  cullAhead: number;       // Distance ahead of camera to stop rendering
  behindFadeFactor: number; // How much faster items behind fade (1.0 = same as ahead)
}

export const DEFAULT_CONFIG: CameraConfig = {
  depthGap: 800,         // Reduced for faster progression
  focusZone: 300,        // Tighter focus zone
  maxVisible: 1500,      // Reduced visibility range
  cullBehind: 600,       // Cull sooner behind
  cullAhead: 2000,       // Keep more visible ahead
  behindFadeFactor: 2.0, // Fade faster behind
};

export interface ArtworkVisualState {
  translateZ: number;   // Relative Z position for CSS transform
  scale: number;        // 0.4 to 1.0
  opacity: number;      // 0.0 to 1.0
  zIndex: number;       // Layer ordering (closer = higher)
  isVisible: boolean;   // Whether to render at all (for culling)
  isFocused: boolean;   // Whether artwork is in focus zone (for title visibility)
}

/**
 * Convert scroll position to camera Z position.
 * Camera starts PAST the last artwork and moves backward through to the first.
 * This way, scrolling DOWN moves you FORWARD through the gallery (approaching artworks).
 *
 * At scroll=0: Camera is ahead of all artworks (high Z), first artwork visible in distance
 * At scroll=max: Camera has passed all artworks (negative Z)
 */
export function scrollToCameraZ(
  scrollTop: number,
  scrollHeight: number,
  viewportHeight: number,
  artworkCount: number,
  config: CameraConfig = DEFAULT_CONFIG
): number {
  const maxScroll = scrollHeight - viewportHeight;
  if (maxScroll <= 0) return -config.focusZone;

  const scrollProgress = Math.max(0, Math.min(1, scrollTop / maxScroll));

  // Total depth span of all artworks
  const totalDepth = config.depthGap * (artworkCount - 1);

  // Camera starts ahead of first artwork, ends past last artwork
  const startZ = -config.focusZone * 2;  // Start behind/before first artwork
  const endZ = totalDepth + config.focusZone;  // End past last artwork

  // INVERTED: scroll=0 means camera at END (past artworks), scroll=max means camera at START
  // This makes scrolling DOWN feel like walking FORWARD
  return endZ - scrollProgress * (endZ - startZ);
}

/**
 * Calculate the Z position for an artwork based on its index.
 */
export function artworkZPosition(
  index: number,
  config: CameraConfig = DEFAULT_CONFIG
): number {
  return index * config.depthGap;
}

/**
 * Calculate the visual state of an artwork based on its distance from the camera.
 */
export function calculateArtworkState(
  artworkZ: number,
  cameraZ: number,
  config: CameraConfig = DEFAULT_CONFIG
): ArtworkVisualState {
  // Distance from camera (positive = ahead, negative = behind/passed)
  const distance = artworkZ - cameraZ;
  const absDistance = Math.abs(distance);
  const isBehind = distance < 0;

  // Culling: hide if too far behind or ahead
  const isVisible =
    distance > -config.cullBehind && distance < config.cullAhead;

  if (!isVisible) {
    return {
      translateZ: distance,
      scale: 0,
      opacity: 0,
      zIndex: 0,
      isVisible: false,
      isFocused: false,
    };
  }

  // Focused: within the focus zone
  const isFocused = absDistance < config.focusZone;

  // Calculate falloff ratio (0 = at camera, 1 = at max visible distance)
  const effectiveDistance = Math.max(0, absDistance - config.focusZone);
  const falloffRange = config.maxVisible - config.focusZone;
  const baseFalloff = Math.min(effectiveDistance / falloffRange, 1);

  // Items behind fade faster
  const falloff = isBehind ? Math.min(baseFalloff * config.behindFadeFactor, 1) : baseFalloff;

  // Scale: 1.0 in focus zone, down to 0.4 at max distance
  const scale = isFocused ? 1 : 1 - falloff * 0.6;

  // Opacity: 1.0 in focus zone, down to 0.1 at max distance
  const opacity = isFocused ? 1 : Math.max(0.1, 1 - falloff * 0.9);

  // Z-index: items closer to camera render on top
  // Use large base to ensure positive values, subtract distance
  const zIndex = Math.round(10000 - absDistance);

  return {
    translateZ: distance,
    scale,
    opacity,
    zIndex,
    isVisible,
    isFocused,
  };
}

/**
 * Calculate the total scroll height needed for the runway.
 * This creates enough scrollable space to navigate through all artworks.
 */
export function calculateRunwayHeight(
  artworkCount: number,
  viewportHeight: number,
): number {
  if (artworkCount <= 1) return viewportHeight;

  // We want scrolling to feel natural:
  // - One viewport height of scroll should move roughly one artwork's depth
  // - Total scroll = viewportHeight * artworkCount gives us this ratio
  const scrollPerArtwork = viewportHeight;
  return viewportHeight + scrollPerArtwork * (artworkCount - 1);
}

/**
 * Calculate scroll progress as a percentage (0-100).
 */
export function calculateScrollProgress(
  scrollTop: number,
  scrollHeight: number,
  viewportHeight: number
): number {
  const maxScroll = scrollHeight - viewportHeight;
  if (maxScroll <= 0) return 0;
  return Math.max(0, Math.min(100, (scrollTop / maxScroll) * 100));
}

/**
 * Image loading strategy type.
 * - 'eager': Load immediately (for above-the-fold content)
 * - 'preload': Load with high priority (for upcoming content)
 * - 'lazy': Load when needed (for distant content)
 */
export type LoadingStrategy = 'eager' | 'preload' | 'lazy';

/**
 * Calculate the optimal loading strategy for an artwork based on its position
 * relative to the camera.
 *
 * Strategy:
 * - Last 2 artworks: Always eager (visible at scroll=0, camera starts past them)
 * - Within preload zone (behind camera): Preload with high priority
 * - Everything else: Lazy load
 *
 * @param artworkIndex - Index of the artwork (0-based)
 * @param artworkZ - Z position of the artwork
 * @param cameraZ - Current Z position of the camera
 * @param totalArtworks - Total number of artworks in gallery
 * @param config - Camera configuration
 * @returns Loading strategy for this artwork
 */
export function calculateLoadingStrategy(
  artworkIndex: number,
  artworkZ: number,
  cameraZ: number,
  totalArtworks: number,
  config: CameraConfig = DEFAULT_CONFIG
): LoadingStrategy {
  // Always eager-load LAST 2 artworks (visible at scroll=0)
  // Camera starts past all artworks, so last ones are closest to initial camera position
  if (artworkIndex >= totalArtworks - 2) {
    return 'eager';
  }

  // Distance from camera (positive = ahead, negative = behind)
  const distance = artworkZ - cameraZ;

  // Preload zone: 3 artworks BEHIND camera (where we're scrolling toward)
  // Using depthGap * 3 as threshold (roughly next 3 artworks in scroll direction)
  const preloadThreshold = config.depthGap * 3;

  // Preload artworks behind camera (negative distance) within threshold
  // As camera moves backward (scrolling down), these are the artworks we're approaching
  if (distance < 0 && Math.abs(distance) < preloadThreshold) {
    return 'preload';
  }

  // Everything else: lazy load
  return 'lazy';
}
