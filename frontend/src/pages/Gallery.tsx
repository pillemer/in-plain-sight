import { useQuery } from '@tanstack/react-query'
import { graphqlClient } from '../lib/graphqlClient'
import { GetArtistDocument } from '../generated/graphql'
import styles from './Gallery.module.scss'

export function Gallery() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['artist'],
    queryFn: async () => {
      return graphqlClient.request(GetArtistDocument)
    },
  })

  if (isLoading) {
    return <div className={styles.container}>Loading...</div>
  }

  if (error) {
    return (
      <div className={styles.container}>
        <p className={styles.error}>Error loading artist data</p>
        <pre className={styles.debug}>
          {error instanceof Error ? error.message : JSON.stringify(error, null, 2)}
        </pre>
      </div>
    )
  }

  if (!data?.artist) {
    return <div className={styles.container}>No artist found</div>
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>{data.artist.name}</h1>
      </header>

      <div className={styles.content}>
        <p className={styles.debug}>
          Artist ID: {data.artist.id}
        </p>
        <p className={styles.status}>
          Backend connected successfully. GraphQL query working.
        </p>
      </div>
    </div>
  )
}
