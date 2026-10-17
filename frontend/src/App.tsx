import { FileText } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

// Setup check only: Tailwind + shadcn + lucide + the @ alias. Replaced by the real screens next.
function App() {
  return (
    <main className="mx-auto max-w-md p-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="size-5" /> Bill to Help
          </CardTitle>
          <CardDescription>Tailwind, shadcn and the @ alias are working.</CardDescription>
        </CardHeader>
        <CardContent className="flex items-center gap-3">
          <Badge>Synthetic demo</Badge>
          <Button>Start</Button>
        </CardContent>
      </Card>
    </main>
  )
}

export default App
