#!/usr/bin/env node

/**
 * Import Fix Script for Sim → Services Migration
 * Converts Next.js specific imports and patterns to React/Vite equivalents
 */

const fs = require('fs');
const path = require('path');

const FRONTEND_DIR = path.join(__dirname, 'services/frontend/src');

// Counters for reporting
const stats = {
  filesProcessed: 0,
  filesModified: 0,
  useClientRemoved: 0,
  routerReplaced: 0,
  importsFixed: 0,
  imageReplaced: 0,
  linkReplaced: 0,
  envFixed: 0,
};

/**
 * Process a single file
 */
function processFile(filePath) {
  const ext = path.extname(filePath);
  if (!['.ts', '.tsx', '.js', '.jsx'].includes(ext)) {
    return;
  }

  stats.filesProcessed++;
  let content = fs.readFileSync(filePath, 'utf8');
  const originalContent = content;
  let modified = false;

  // 1. Remove 'use client' directives
  if (content.includes("'use client'") || content.includes('"use client"')) {
    content = content.replace(/['"]use client['"]\s*\n/g, '');
    stats.useClientRemoved++;
    modified = true;
  }

  // 2. Replace Next.js router imports with react-router-dom
  if (content.includes("from 'next/navigation'") || content.includes('from "next/navigation"')) {
    // Replace useRouter import
    content = content.replace(
      /import\s*{([^}]*useRouter[^}]*)}\s*from\s*['"]next\/navigation['"]/g,
      (match, imports) => {
        const importList = imports.split(',').map(i => i.trim()).filter(i => i);
        const routerImports = [];
        const otherImports = [];

        importList.forEach(imp => {
          if (imp === 'useRouter') {
            routerImports.push('useNavigate');
          } else if (imp === 'useParams') {
            routerImports.push('useParams');
          } else if (imp === 'useSearchParams') {
            routerImports.push('useSearchParams');
          } else if (imp === 'usePathname') {
            // usePathname → useLocation
            routerImports.push('useLocation');
          } else {
            otherImports.push(imp);
          }
        });

        return `import { ${routerImports.join(', ')} } from 'react-router-dom'`;
      }
    );
    stats.routerReplaced++;
    modified = true;
  }

  // 3. Replace router.push() with navigate()
  if (content.includes('router.push(')) {
    content = content.replace(/const\s+router\s*=\s*useRouter\(\)/g, 'const navigate = useNavigate()');
    content = content.replace(/router\.push\(/g, 'navigate(');
    content = content.replace(/router\.replace\(/g, 'navigate(');
    modified = true;
  }

  // 4. Replace usePathname() with useLocation()
  if (content.includes('usePathname()')) {
    content = content.replace(/const\s+pathname\s*=\s*usePathname\(\)/g, 'const location = useLocation()\n  const pathname = location.pathname');
    modified = true;
  }

  // 5. Fix @/app/* imports to @/components/* or @/lib/*
  const appImportRegex = /from\s+['"]@\/app\/([^'"]+)['"]/g;
  content = content.replace(appImportRegex, (match, importPath) => {
    // Determine new path based on what's being imported
    if (importPath.includes('components/')) {
      const newPath = importPath.replace(/.*components\//, '');
      return `from '@/components/${newPath}'`;
    } else if (importPath.includes('lib/')) {
      const newPath = importPath.replace(/.*lib\//, '');
      return `from '@/lib/${newPath}'`;
    } else if (importPath.includes('hooks/')) {
      const newPath = importPath.replace(/.*hooks\//, '');
      return `from '@/hooks/${newPath}'`;
    } else if (importPath.includes('stores/')) {
      const newPath = importPath.replace(/.*stores\//, '');
      return `from '@/stores/${newPath}'`;
    } else if (importPath.includes('utils/')) {
      const newPath = importPath.replace(/.*utils\//, '');
      return `from '@/utils/${newPath}'`;
    } else if (importPath.includes('blocks/')) {
      const newPath = importPath.replace(/.*blocks\//, '');
      return `from '@/blocks/${newPath}'`;
    } else if (importPath.includes('types/')) {
      const newPath = importPath.replace(/.*types\//, '');
      return `from '@/types/${newPath}'`;
    }

    // Default: try to extract the meaningful part
    const parts = importPath.split('/');
    const meaningfulPart = parts[parts.length - 1];
    return `from '@/components/${meaningfulPart}'`;
  });

  if (appImportRegex.test(originalContent)) {
    stats.importsFixed++;
    modified = true;
  }

  // 6. Replace next/image with standard img tags
  if (content.includes("from 'next/image'") || content.includes('from "next/image"')) {
    content = content.replace(/import\s+Image\s+from\s+['"]next\/image['"]\s*\n/g, '');
    content = content.replace(/<Image\s+src=/g, '<img src=');
    content = content.replace(/\s+width=\{[^}]+\}/g, '');
    content = content.replace(/\s+height=\{[^}]+\}/g, '');
    content = content.replace(/\s+alt=/g, ' alt=');
    stats.imageReplaced++;
    modified = true;
  }

  // 7. Replace next/link with react-router-dom Link
  if (content.includes("from 'next/link'") || content.includes('from "next/link"')) {
    content = content.replace(/import\s+Link\s+from\s+['"]next\/link['"]/g, "import { Link } from 'react-router-dom'");
    // Next.js Link uses href, react-router uses to
    content = content.replace(/<Link\s+href=/g, '<Link to=');
    stats.linkReplaced++;
    modified = true;
  }

  // 8. Replace process.env with import.meta.env
  if (content.includes('process.env.')) {
    content = content.replace(/process\.env\.(NEXT_PUBLIC_[A-Z_]+)/g, 'import.meta.env.VITE_$1');
    content = content.replace(/process\.env\.([A-Z_]+)/g, 'import.meta.env.VITE_$1');
    stats.envFixed++;
    modified = true;
  }

  // 9. Fix getEnv calls to use import.meta.env
  if (content.includes('getEnv(')) {
    // Replace getEnv('KEY') with import.meta.env.VITE_KEY
    content = content.replace(/getEnv\(['"]([^'"]+)['"]\)/g, 'import.meta.env.VITE_$1');
    modified = true;
  }

  // 10. Remove Next.js specific API imports
  const nextJsAPIs = ['cookies', 'headers', 'notFound', 'redirect', 'permanentRedirect'];
  nextJsAPIs.forEach(api => {
    if (content.includes(`from 'next/${api}'`)) {
      content = content.replace(new RegExp(`import\\s+{[^}]*}\\s+from\\s+['"]next\\/${api}['"]\\s*\\n`, 'g'), '');
      modified = true;
    }
  });

  // Write back if modified
  if (modified) {
    fs.writeFileSync(filePath, content, 'utf8');
    stats.filesModified++;
  }
}

/**
 * Recursively process all files in directory
 */
function processDirectory(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // Skip node_modules
      if (entry.name === 'node_modules') continue;
      processDirectory(fullPath);
    } else if (entry.isFile()) {
      processFile(fullPath);
    }
  }
}

// Main execution
console.log('🔧 Starting import fixes for Sim → Services migration...\n');
console.log(`📂 Processing directory: ${FRONTEND_DIR}\n`);

processDirectory(FRONTEND_DIR);

console.log('\n✅ Import fixes completed!\n');
console.log('📊 Statistics:');
console.log(`   Files processed: ${stats.filesProcessed}`);
console.log(`   Files modified: ${stats.filesModified}`);
console.log(`   'use client' removed: ${stats.useClientRemoved}`);
console.log(`   Router imports replaced: ${stats.routerReplaced}`);
console.log(`   @/app imports fixed: ${stats.importsFixed}`);
console.log(`   next/image replaced: ${stats.imageReplaced}`);
console.log(`   next/link replaced: ${stats.linkReplaced}`);
console.log(`   process.env fixed: ${stats.envFixed}`);
console.log('\n');
