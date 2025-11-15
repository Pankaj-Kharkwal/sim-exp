import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useTemplateStore } from '@/stores/templateStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Search,
  Star,
  Eye,
  Users,
  Loader2,
  LayoutTemplate,
  TrendingUp,
  Clock,
  Filter
} from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { cn } from '@/lib/utils'

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
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="border-b bg-white px-6 py-4">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h1 className="font-bold text-2xl">Templates</h1>
            <p className="text-gray-600 text-sm">
              Browse and use pre-built workflow templates
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setMyTemplatesOnly(!myTemplatesOnly)}
            className={cn(myTemplatesOnly && 'bg-blue-50 text-blue-600')}
          >
            <Filter className="mr-2 h-4 w-4" />
            {myTemplatesOnly ? 'My Templates' : 'All Templates'}
          </Button>
        </div>

        {/* Search and Filters */}
        <div className="flex items-center gap-3">
          <div className="relative flex-1">
            <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search templates..."
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              className="pl-10"
            />
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
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
      <div className="border-b bg-gray-50 px-6">
        <div className="flex gap-1 overflow-x-auto">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.value || 'all'}
              onClick={() => setCategory(cat.value)}
              className={cn(
                'whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium transition-colors',
                category === cat.value
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              )}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-6">
        {error && (
          <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-4">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          </div>
        ) : templates.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="rounded-full bg-gray-100 p-4">
              <LayoutTemplate className="h-8 w-8 text-gray-400" />
            </div>
            <h3 className="mt-4 font-semibold text-gray-900">No templates found</h3>
            <p className="mt-2 text-center text-gray-600 text-sm">
              {search
                ? 'Try adjusting your search or filters'
                : 'Create your first template by saving a workflow'}
            </p>
          </div>
        ) : (
          <>
            {/* Template Grid */}
            <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {templates.map((template) => (
                <Card
                  key={template.id}
                  className="group cursor-pointer transition-all hover:shadow-lg"
                  onClick={() => handleTemplateClick(template.id)}
                >
                  <CardHeader className="pb-3">
                    <div className="mb-2 flex items-start justify-between">
                      <div
                        className="flex h-10 w-10 items-center justify-center rounded-lg"
                        style={{ backgroundColor: template.color + '20' }}
                      >
                        <LayoutTemplate
                          className="h-5 w-5"
                          style={{ color: template.color }}
                        />
                      </div>
                      <button
                        onClick={(e) => handleStar(e, template.id, template.user_has_starred)}
                        className="rounded p-1 hover:bg-gray-100"
                      >
                        <Star
                          className={cn(
                            'h-4 w-4',
                            template.user_has_starred
                              ? 'fill-yellow-400 text-yellow-400'
                              : 'text-gray-400'
                          )}
                        />
                      </button>
                    </div>
                    <CardTitle className="line-clamp-1 text-base">
                      {template.name}
                    </CardTitle>
                    <CardDescription className="line-clamp-2 text-xs">
                      {template.description || 'No description provided'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="flex items-center gap-3 text-gray-600 text-xs">
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
                    <div className="mt-2 flex items-center justify-between">
                      <span className="text-gray-500 text-xs">
                        by {template.author_name}
                      </span>
                      <span className="text-gray-400 text-xs">
                        {formatDistanceToNow(new Date(template.created_at), { addSuffix: true })}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page === 1}
                  onClick={() => setPage(page - 1)}
                >
                  Previous
                </Button>
                <span className="text-gray-600 text-sm">
                  Page {page} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page === totalPages}
                  onClick={() => setPage(page + 1)}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
