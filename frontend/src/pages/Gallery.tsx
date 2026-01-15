import { useQuery } from '@tanstack/react-query'
import { graphqlClient } from '../lib/graphqlClient'
import { GetCollectionsDocument } from '../generated/graphql'
import { GalleryView } from '../components/Gallery'
import { Header } from '../components/Navigation/Header'
import styles from './Gallery.module.scss'

export function Gallery() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['collections'],
    queryFn: async () => {
      return graphqlClient.request(GetCollectionsDocument)
    },
  })

  if (isLoading) {
    return <div className={styles.loading}>Loading...</div>
  }

  if (error) {
    return (
      <div className={styles.errorContainer}>
        <p className={styles.error}>Error loading gallery</p>
        <pre className={styles.debug}>
          {error instanceof Error ? error.message : JSON.stringify(error, null, 2)}
        </pre>
      </div>
    )
  }

  if (!data?.collections || data.collections.length === 0) {
    return <div className={styles.loading}>No collections found</div>
  }

  // For MVP, flatten all artworks from all collections into a single depth sequence
  // Future: could have collection navigation or separate galleries
  const allArtworks = data.collections.flatMap((collection) =>
    collection.artworks.map((artwork) => ({
      id: artwork.id,
      title: artwork.title,
      imageUrl: artwork.imageUrl,
      artistName: artwork.artist.name,
    }))
  )

  if (allArtworks.length === 0) {
    return <div className={styles.loading}>No artworks found</div>
  }

  return (
    <>
      <Header collections={data.collections.map(c => ({ id: c.id, title: c.title }))} />
      <GalleryView artworks={allArtworks} />
    </>
  )
}
