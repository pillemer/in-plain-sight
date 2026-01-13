import { useQuery } from "@tanstack/react-query";
import { graphqlClient } from "../lib/graphqlClient";
import { GetArtistDocument, GetCollectionsDocument } from "../generated/graphql";
import { Header } from "../components/Navigation/Header";
import styles from './Bio.module.scss'

export function Bio() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['artist'],
        queryFn: async () => {
            return graphqlClient.request(GetArtistDocument)
        }
    })

    const { data: collectionsData } = useQuery({
        queryKey: ['collections'],
        queryFn: async () => {
            return graphqlClient.request(GetCollectionsDocument)
        }
    })

    if (isLoading) {
        return <div className={styles.loading}>Loading...</div>
    }
    if (error) {
        return (
            <div className={styles.errorContainer}>
                <p className={styles.error}>Error Loading artist information</p>
                <pre className={styles.debug}>
                    {error instanceof Error ? error.message : JSON.stringify(error, null, 2)}
                </pre>
            </div>)
    }

    if (!data?.artist) {
        return <div className={styles.loading}>No artist found</div>
    }

    return (
        <>
            {collectionsData?.collections && (
                <Header
                    collections={collectionsData.collections.map(c => ({ id: c.id, title: c.title }))}
                    title="About the Artist"
                />
            )}
            <div className={styles.container} >
                <h1>{data.artist.name}</h1>
                <p>{data.artist.bio}</p>
            </div>
        </>
    )
}