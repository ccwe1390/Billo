import * as React from "react"
import { cn } from "cn"
import { Checkbox as CheckboxPrimitive } from "radix-ui"

// Restyled for Billo: 24px box with a 2px border, solid fill when checked, and a drawn tick (CSS, no icon
// library), so the checked state is a shape change and not colour alone (team UI rule 10).
function Checkbox({
  className,
  ...props
}: React.ComponentProps<typeof CheckboxPrimitive.Root>) {
  return (
    <CheckboxPrimitive.Root
      data-slot="checkbox"
      className={cn(
        "relative grid size-6 shrink-0 place-items-center rounded-md border-2 border-input bg-transparent outline-none transition-colors duration-150 focus-visible:outline-3 focus-visible:outline-offset-2 focus-visible:outline-ring disabled:cursor-not-allowed disabled:border-border data-[state=checked]:border-success data-[state=checked]:bg-success",
        className
      )}
      {...props}
    >
      <CheckboxPrimitive.Indicator data-slot="checkbox-indicator" className="block">
        <span aria-hidden className="mb-0.5 block h-3 w-1.5 rotate-45 border-e-[3px] border-b-[3px] border-success-foreground" />
      </CheckboxPrimitive.Indicator>
    </CheckboxPrimitive.Root>
  )
}

export { Checkbox }
