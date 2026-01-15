import { useState, useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { GalleriesDropdown } from './GalleriesDropdown'
import styles from './Header.module.scss'

interface Collection {
    id: string
    title: string
}

interface HeaderProps {
    collections: Collection[]
    title?: string
}

export function Header({ collections, title = "Art in the Forest" }: HeaderProps) {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false)

    const dropdownRef = useRef<HTMLDivElement>(null)

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen)
    }

    useEffect(() => {
        if (!isDropdownOpen) return
        const handleOutsideClick = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsDropdownOpen(false)
            }
        }

        document.addEventListener('mousedown', handleOutsideClick)
        return () => {
            document.removeEventListener('mousedown', handleOutsideClick)
        }
    }, [isDropdownOpen])

    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <h1 className={styles.title}>{title}</h1>

                <nav className={styles.nav}>
                    <div className={styles.dropdownContainer}>
                        <button
                            onClick={toggleDropdown}
                            className={styles.link}
                        >
                            Galleries
                        </button>
                    </div>
                    <Link to="/about" className={styles.link}>About</Link>
                </nav>
            </div>

            {/* Render dropdown at header level so it can position relative to header */}
            {isDropdownOpen && (
                <div ref={dropdownRef}>
                    <GalleriesDropdown
                        collections={collections}
                        onSelect={() => setIsDropdownOpen(false)}
                    />
                </div>
            )}
        </header>
    )
}
