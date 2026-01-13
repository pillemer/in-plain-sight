import { QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { queryClient } from './lib/queryClient'
import { Gallery } from './pages/Gallery'
import { Bio } from './pages/Bio'

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Gallery />} />
          <Route path="/about" element={<Bio />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
