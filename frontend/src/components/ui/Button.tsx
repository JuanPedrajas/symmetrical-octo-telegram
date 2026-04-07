import { cn } from "@/lib/utils";
import type { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "ghost";
}

export function Button({ variant = "primary", className, children, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "rounded-lg px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
        variant === "primary" &&
          "bg-zinc-100 text-zinc-900 hover:bg-zinc-200",
        variant === "ghost" &&
          "border border-zinc-700 text-zinc-300 hover:bg-zinc-800",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
