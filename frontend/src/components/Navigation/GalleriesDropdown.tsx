import { Link } from 'react-router-dom'
import styles from './GalleriesDropdown.module.scss'

interface Collection {
  id: string
  title: string
}

interface GalleriesDropdownProps {
  collections: Collection[]
  onSelect: () => void
}

export function GalleriesDropdown({ collections, onSelect }: GalleriesDropdownProps) {
  const activeCollectionTitle = "Watercolours"

  return (
    <div className={styles.dropdown}>
      <ul className={styles.list}>
        {collections.map((collection) => {
          const isActive = collection.title === activeCollectionTitle

          return (
            <li key={collection.id} className={styles.item}>
              {isActive ? (
                <Link
                  to={`/`}
                  className={styles.link}
                  onClick={onSelect}
                >
                  {collection.title}
                </Link>
              ) : (
                <span className={styles.linkDisabled}>
                  {collection.title}
                </span>
              )}
            </li>
          )
        })}

        {/* Placeholder collections */}
        <li className={styles.item}>
          <span className={styles.linkDisabled}>Oils</span>
        </li>
        <li className={styles.item}>
          <span className={styles.linkDisabled}>Sketches</span>
        </li>
      </ul>
    </div>
  )
}
