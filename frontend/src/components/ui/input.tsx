import * as React from "react"
import { cn } from "cn"

// Restyled for Bill to Help: 48px tall, 2px border that turns solid teal on focus, dark field surface.
function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "h-12 w-full min-w-0 rounded-[var(--radius)] border-2 border-input bg-background px-3 text-base text-foreground transition-colors duration-150 outline-none placeholder:text-muted-foreground focus-visible:border-primary focus-visible:outline-none aria-invalid:border-destructive disabled:cursor-not-allowed disabled:border-border disabled:text-muted-foreground",
        className
      )}
      {...props}
    />
  )
}

export { Input }
