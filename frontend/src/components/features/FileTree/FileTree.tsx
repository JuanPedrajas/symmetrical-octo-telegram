import { useState } from "react";
import { useNavigate } from "react-router";
import { cn } from "@/lib/utils";
import type { TreeNode } from "@/types";

interface FileTreeProps {
  tree: TreeNode;
  selectedPath?: string;
}

interface NodeProps {
  name: string;
  node: TreeNode | string;
  selectedPath?: string;
  depth: number;
}

function TreeNodeItem({ name, node, selectedPath, depth }: NodeProps) {
  const navigate = useNavigate();
  const [open, setOpen] = useState(true);
  const isLeaf = typeof node === "string";
  const indent = depth * 12;

  if (isLeaf) {
    const path = node as string;
    const isSelected = selectedPath === path;
    return (
      <button
        onClick={() => navigate(`/?path=${encodeURIComponent(path)}`)}
        style={{ paddingLeft: `${indent + 8}px` }}
        className={cn(
          "flex w-full items-center gap-1.5 rounded py-1 pr-2 text-left text-sm transition-colors",
          isSelected
            ? "bg-zinc-700 text-white"
            : "text-zinc-300 hover:bg-zinc-800 hover:text-white"
        )}
        title={path}
      >
        <span className="text-zinc-500">📄</span>
        <span className="truncate">{name}</span>
      </button>
    );
  }

  return (
    <div>
      <button
        onClick={() => setOpen((o) => !o)}
        style={{ paddingLeft: `${indent + 8}px` }}
        className="flex w-full items-center gap-1.5 rounded py-1 pr-2 text-left text-sm font-medium text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-zinc-200"
      >
        <span>{open ? "▾" : "▸"}</span>
        <span>{name}</span>
      </button>
      {open && (
        <div>
          {Object.entries(node as TreeNode)
            .sort(([, a], [, b]) => {
              // Folders before files
              const aIsFolder = typeof a !== "string";
              const bIsFolder = typeof b !== "string";
              if (aIsFolder !== bIsFolder) return aIsFolder ? -1 : 1;
              return 0;
            })
            .map(([childName, childNode]) => (
              <TreeNodeItem
                key={childName}
                name={childName}
                node={childNode}
                selectedPath={selectedPath}
                depth={depth + 1}
              />
            ))}
        </div>
      )}
    </div>
  );
}

export function FileTree({ tree, selectedPath }: FileTreeProps) {
  return (
    <nav className="w-full overflow-auto">
      {Object.entries(tree)
        .sort(([, a], [, b]) => {
          const aIsFolder = typeof a !== "string";
          const bIsFolder = typeof b !== "string";
          if (aIsFolder !== bIsFolder) return aIsFolder ? -1 : 1;
          return 0;
        })
        .map(([name, node]) => (
          <TreeNodeItem
            key={name}
            name={name}
            node={node}
            selectedPath={selectedPath}
            depth={0}
          />
        ))}
    </nav>
  );
}
