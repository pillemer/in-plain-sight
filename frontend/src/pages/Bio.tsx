import { useQuery } from "@tanstack/react-query";
import { graphqlClient } from "../lib/graphqlClient";
import { GetArtistDocument, GetCollectionsDocument } from "../generated/graphql";
import { Header } from "../components/Navigation/Header";
import styles from './Bio.module.scss'
import artist from '../../public/artist.avif'

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
            <div className={styles.page}>
                <div className={styles.postcard}>
                    <div className={styles.imagePanel}>
                        <img src={artist} alt={data.artist.name} />
                        <span className={styles.photoCredit}>Photo by Claudio Amdur, 2017</span>
                    </div>
                    <div className={styles.infoPanel}>
                        <h1>{data.artist.name}</h1>
                        <div className={styles.divider} />
                        <p>{data.artist.bio}</p>
                    </div>
                </div>
            </div>
        </>
    )
}