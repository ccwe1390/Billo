import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "cn"
import { Slot } from "radix-ui"

// Restyled for Billo (not the shadcn default): 48px minimum tap target (team UI rule 10), solid colour
// changes on hover instead of opacity fades, explicit disabled colours, a 2px press offset instead of scaling.
const buttonVariants = cva(
  "inline-flex shrink-0 items-center justify-center gap-2 rounded-[var(--radius)] border-2 font-bold whitespace-nowrap select-none transition-colors duration-150 outline-none active:translate-y-0.5 disabled:pointer-events-none disabled:border-border disabled:bg-muted disabled:text-muted-foreground [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "border-primary bg-primary text-primary-foreground hover:border-primary-hover hover:bg-primary-hover",
        outline: "border-input bg-transparent text-foreground hover:border-foreground hover:bg-muted-hover",
        ghost: "border-transparent bg-transparent text-muted-foreground underline-offset-4 hover:text-foreground hover:underline",
      },
      size: {
        default: "h-12 px-5 text-base",
        lg: "h-14 px-7 text-lg",
        square: "size-12 px-0 text-xl",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot.Root : "button"

  return (
    <Comp
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
