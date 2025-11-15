import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useTemplateStore } from '@/stores/templateStore'
import {
  Search,
  Star,
  Eye,
  Users,
  Loader2,
  LayoutTemplate,
  Filter,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

const CATEGORIES = [
  { value: null, label: 'All Templates' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'sales', label: 'Sales' },
  { value: 'finance', label: 'Finance' },
  { value: 'support', label: 'Support' },
  { value: 'ai', label: 'AI & ML' },
  { value: 'other', label: 'Other' },
]

const SORT_OPTIONS = [
  { value: 'created_at', label: 'Recently Added' },
  { value: 'views', label: 'Most Viewed' },
  { value: 'uses', label: 'Most Used' },
  { value: 'name', label: 'Name' },
]

export default function TemplatesPage() {
  const { workspaceId } = useParams()
  const navigate = useNavigate()
  const [searchValue, setSearchValue] = useState('')

  const {
    templates,
    isLoading,
    error,
    total,
    page,
    totalPages,
    category,
    search,
    sortBy,
    myTemplatesOnly,
    fetchTemplates,
    setCategory,
    setSearch,
    setSortBy,
    setMyTemplatesOnly,
    setPage,
    starTemplate,
    unstarTemplate,
  } = useTemplateStore()

  useEffect(() => {
    fetchTemplates(true)
  }, [fetchTemplates])

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchValue !== search) {
        setSearch(searchValue)
        fetchTemplates(true)
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [searchValue, search, setSearch, fetchTemplates])

  const handleStar = async (e: React.MouseEvent, templateId: string, isStarred: boolean) => {
    e.stopPropagation()
    try {
      if (isStarred) {
        await unstarTemplate(templateId)
      } else {
        await starTemplate(templateId)
      }
    } catch (error) {
      console.error('Failed to star/unstar template:', error)
    }
  }

  const handleTemplateClick = (templateId: string) => {
    navigate(`/workspace/${workspaceId}/templates/${templateId}`)
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-6 fade-in">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h1 className="font-bold text-3xl text-white">Templates</h1>
              <p className="mt-2 text-white/70">
                Browse and use pre-built workflow templates
              </p>
            </div>
            <button
              onClick={() => setMyTemplatesOnly(!myTemplatesOnly)}
              className={cn(
                'glass-button px-4 py-2',
                myTemplatesOnly && 'bg-purple-500/30'
              )}
            >
              <Filter className="mr-2 h-4 w-4" />
              {myTemplatesOnly ? 'My Templates' : 'All Templates'}
            </button>
          </div>

          {/* Search and Filters */}
          <div className="flex items-center gap-3 fade-in" style={{ animationDelay: '0.1s' }}>
            <div className="relative flex-1">
              <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-white/40" />
              <input
                placeholder="Search templates..."
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                className="glass-input w-full pl-10"
              />
            </div>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="glass-input px-4 py-3 min-w-[180px]"
            >
              {SORT_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Category Tabs */}
        <div className="mb-6 fade-in" style={{ animationDelay: '0.2s' }}>
          <div className="glass-card p-2">
            <div className="flex gap-2 overflow-x-auto">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat.value || 'all'}
                  onClick={() => setCategory(cat.value)}
                  className={cn(
                    'whitespace-nowrap px-4 py-2 text-sm font-medium transition-all rounded-lg',
                    category === cat.value
                      ? 'bg-purple-500/30 text-white'
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  )}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div>
          {error && (
            <div className="glass-card mb-4 border-2 border-red-500/30 bg-red-500/10 p-4 fade-in">
              <p className="text-sm text-red-200">{error}</p>
            </div>
          )}

          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-white/40" />
            </div>
          ) : templates.length === 0 ? (
            <div className="glass-card flex flex-col items-center justify-center py-12 fade-in">
              <div className="mb-4 rounded-full bg-white/10 p-4">
                <LayoutTemplate className="h-8 w-8 text-white/40" />
              </div>
              <h3 className="font-semibold text-white">No templates found</h3>
              <p className="mt-2 text-center text-sm text-white/70">
                {search
                  ? 'Try adjusting your search or filters'
                  : 'Create your first template by saving a workflow'}
              </p>
            </div>
          ) : (
            <>
              {/* Template Grid */}
              <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {templates.map((template, index) => (
                  <div
                    key={template.id}
                    className="glass-card group cursor-pointer p-6 fade-in"
                    style={{ animationDelay: `${(index % 12) * 0.05}s` }}
                    onClick={() => handleTemplateClick(template.id)}
                  >
                    <div className="mb-4 flex items-start justify-between">
                      <div
                        className="flex h-10 w-10 items-center justify-center rounded-lg"
                        style={{
                          backgroundColor: template.color ? `${template.color}30` : 'rgba(255, 255, 255, 0.1)'
                        }}
                      >
                        <LayoutTemplate
                          className="h-5 w-5"
                          style={{ color: template.color || '#fff' }}
                        />
                      </div>
                      <button
                        onClick={(e) => handleStar(e, template.id, template.user_has_starred)}
                        className="rounded-lg p-1.5 transition-all hover:bg-white/10"
                      >
                        <Star
                          className={cn(
                            'h-4 w-4',
                            template.user_has_starred
                              ? 'fill-yellow-400 text-yellow-400'
                              : 'text-white/60'
                          )}
                        />
                      </button>
                    </div>

                    <h3 className="mb-2 line-clamp-1 font-semibold text-white">
                      {template.name}
                    </h3>
                    <p className="mb-4 line-clamp-2 min-h-[2.5rem] text-sm text-white/70">
                      {template.description || 'No description provided'}
                    </p>

                    <div className="flex items-center gap-3 text-xs text-white/60">
                      <div className="flex items-center gap-1">
                        <Eye className="h-3 w-3" />
                        {template.views}
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="h-3 w-3" />
                        {template.uses}
                      </div>
                      <div className="flex items-center gap-1">
                        <Star className="h-3 w-3" />
                        {template.star_count}
                      </div>
                    </div>

                    <div className="mt-3 flex items-center justify-between border-t border-white/10 pt-3 text-xs">
                      <span className="text-white/60">
                        by {template.author_name}
                      </span>
                      <span className="text-white/50">
                        {formatDistanceToNow(new Date(template.created_at), { addSuffix: true })}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-3 fade-in">
                  <button
                    className="glass-button px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={page === 1}
                    onClick={() => setPage(page - 1)}
                  >
                    <ChevronLeft className="mr-1 h-4 w-4" />
                    Previous
                  </button>
                  <span className="text-sm text-white/70">
                    Page {page} of {totalPages}
                  </span>
                  <button
                    className="glass-button px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={page === totalPages}
                    onClick={() => setPage(page + 1)}
                  >
                    Next
                    <ChevronRight className="ml-1 h-4 w-4" />
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}
