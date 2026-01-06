import { useEffect, useRef, useState } from 'react';
import {
  scrollToCameraZ,
  calculateScrollProgress,
  type CameraConfig,
  DEFAULT_CONFIG,
} from './calculations';

interface CameraState {
  cameraZ: number;
  scrollProgress: number;
}

interface UseCameraOptions {
  artworkCount: number;
  config?: CameraConfig;
}

interface UseCameraReturn {
  containerRef: React.RefObject<HTMLDivElement | null>;
  cameraZ: number;
  scrollProgress: number;
}

/**
 * Custom hook that manages the depth camera state.
 * Updates on scroll events only (not continuous RAF) for better performance.
 */
export function useCamera({
  artworkCount,
  config = DEFAULT_CONFIG,
}: UseCameraOptions): UseCameraReturn {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [state, setState] = useState<CameraState>(() => {
    // Initialize camera ahead of all artworks (scroll=0 position)
    // This gets recalculated on first scroll update anyway
    return {
      cameraZ: config.depthGap * 10, // High Z = ahead of artworks
      scrollProgress: 0,
    };
  });

  // Stable reference to config
  const configRef = useRef(config);
  configRef.current = config;

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let ticking = false;

    const updateCamera = () => {
      const scrollTop = container.scrollTop;
      const scrollHeight = container.scrollHeight;
      const viewportHeight = container.clientHeight;

      const cameraZ = scrollToCameraZ(
        scrollTop,
        scrollHeight,
        viewportHeight,
        artworkCount,
        configRef.current
      );

      const scrollProgress = calculateScrollProgress(
        scrollTop,
        scrollHeight,
        viewportHeight
      );

      setState({ cameraZ, scrollProgress });
      ticking = false;
    };

    const handleScroll = () => {
      // Throttle updates using RAF - only one update per frame
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(updateCamera);
      }
    };

    // Use passive listener for better scroll performance
    container.addEventListener('scroll', handleScroll, { passive: true });

    // Initial update
    updateCamera();

    return () => {
      container.removeEventListener('scroll', handleScroll);
    };
  }, [artworkCount]);

  return {
    containerRef,
    cameraZ: state.cameraZ,
    scrollProgress: state.scrollProgress,
  };
}
