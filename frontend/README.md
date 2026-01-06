# In Plain Sight - Frontend

React frontend for the In Plain Sight art gallery application.

## Tech Stack

- **Build Tool**: Vite
- **Framework**: React 18 + TypeScript
- **Data Fetching**: TanStack Query + graphql-request
- **Routing**: React Router
- **Styling**: SCSS Modules
- **Type Generation**: GraphQL Code Generator

## Prerequisites

- Node.js 18+ (or compatible version)
- Backend server running at `http://localhost:8000/graphql`

## Installation

```bash
npm install
```

## Environment Variables

Create a `.env.local` file (see `.env.example` for template):

```bash
VITE_API_URL=http://localhost:8000/graphql
```

## Development Commands

### Start dev server
```bash
npm run dev
```

Server runs at `http://localhost:5173` with hot module replacement.

### Type checking
```bash
npm run build      # Build for production (includes type checking)
npx tsc --noEmit   # Type check without building
```

### Preview production build
```bash
npm run preview
```

## GraphQL Code Generator Workflow

The project uses GraphQL Code Generator to create TypeScript types from the backend schema.

### Generate types
```bash
npm run codegen
```

**Requirements:**
- Backend must be running at `http://localhost:8000/graphql`
- Run this command whenever you:
  - Add or modify `.graphql` query files in `src/queries/`
  - Backend GraphQL schema changes

### Watch mode (auto-regenerate on changes)
```bash
npm run codegen:watch
```

### Generated files
- `src/generated/graphql.ts` - Auto-generated TypeScript types and documents
- **Do not edit manually** - this file is regenerated from schema

## Project Structure

```
src/
├── components/         # React components (with .module.scss)
│   └── Gallery/        # Depth-camera gallery system
│       ├── GalleryView.tsx       # Container with scroll handling
│       ├── Artwork.tsx           # Individual artwork presentation
│       ├── useCamera.ts          # Scroll-to-camera position hook
│       ├── calculations.ts       # Pure functions for visual state
│       └── *.module.scss         # Component styles
├── pages/              # Page-level components
│   └── Gallery.tsx
├── styles/
│   ├── abstracts/      # Variables, mixins
│   ├── base/           # Reset, typography
│   └── global.scss     # Global styles entry point
├── queries/            # GraphQL query definitions (.graphql files)
│   └── artist.graphql
├── lib/                # Client setup
│   ├── graphqlClient.ts
│   └── queryClient.ts
├── hooks/              # Custom React hooks
├── generated/          # Auto-generated (gitignored)
│   └── graphql.ts
└── types/              # Manual TypeScript types

```

## Adding New GraphQL Queries

1. Create a `.graphql` file in `src/queries/`:
   ```graphql
   # src/queries/myQuery.graphql
   query GetCollections {
     collections {
       id
       title
     }
   }
   ```

2. Run codegen to generate TypeScript types:
   ```bash
   npm run codegen
   ```

3. Import and use the generated document in your component:
   ```typescript
   import { useQuery } from '@tanstack/react-query'
   import { graphqlClient } from '../lib/graphqlClient'
   import { GetCollectionsDocument } from '../generated/graphql'

   const { data } = useQuery({
     queryKey: ['collections'],
     queryFn: async () => graphqlClient.request(GetCollectionsDocument)
   })
   ```

## SCSS Architecture

- **CSS Modules** for component styles (`.module.scss`)
- **Global SCSS** for base styles, variables, and mixins
- **Modern `@use`/`@forward`** syntax (no deprecated `@import`)

### Using SCSS in components

```tsx
// Component file
import styles from './MyComponent.module.scss'

export function MyComponent() {
  return <div className={styles.container}>...</div>
}
```

```scss
// MyComponent.module.scss
@use '../styles/abstracts' as *;

.container {
  padding: $spacing-lg;
  color: var(--color-text);

  @include respond-to(tablet) {
    padding: $spacing-xl;
  }
}
```

## Notes

- Backend server must be running for GraphQL queries to work
- CORS is configured in the backend for `http://localhost:5173`
- CSS custom properties in `:root` support runtime changes (for Curtain mode)
