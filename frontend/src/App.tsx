import { QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { queryClient } from './lib/queryClient'
import { Gallery } from './pages/Gallery'

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Gallery />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
