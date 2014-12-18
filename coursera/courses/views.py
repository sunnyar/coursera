from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from .models import Course, University, Category, Instructor, Session
from dict import course_dict, university_dict, instructor_dict, categories_dict, sessions_dict
import requests, os

LANGUAGE_CHOICES = (('all', 'All Languages'), ('en', 'English'), ('zh-cn', 'Chinese'),
                    ('es', 'Spainish'), ('fr', 'French'), ('ru', 'Russian'),
                    ('tr', 'Turkish'), ('it', 'Italian'), ('ar', 'Arabic'))


def search(request):
    get_query = request.GET['q']
    get_query = get_query.split().replace(' ', '+')
    search_query= os.popen('https://api.coursera.org/api/catalog.v1/courses?q=search&query=%s' % get_query)
    return render_to_response('landing_page.html', locals(), context_instance=RequestContext(request))

class CourseAPI(object):

    COURSERA_CATALOG_API_ENDPOINT_COURSES = 'https://api.coursera.org/api/catalog.v1/courses?fields=name,shortDescription,language,photo,video,faq,aboutTheCourse,courseSyllabus,recommendedBackground,aboutTheInstructor&includes=instructors,categories,universities,sessions'
    COURSERA_CATALOG_API_ENDPOINT_UNIVERSITIES = 'https://api.coursera.org/api/catalog.v1/universities?fields=name,banner,homeLink'
    COURSERA_CATALOG_API_ENDPOINT_CATEGORIES = 'https://api.coursera.org/api/catalog.v1/categories?fields=name,shortName'
    COURSERA_CATALOG_API_ENDPOINT_INSTRUCTORS = 'https://api.coursera.org/api/catalog.v1/instructors?fields=firstName,lastName,suffixName'
    COURSERA_CATALOG_API_ENDPOINT_SESSIONS = 'https://api.coursera.org/api/catalog.v1/sessions?fields=homeLink,status,durationString,startDay,startMonth,startYear'

    def __init__(self):
        self.response_courses = course_dict #requests.get(CourseAPI.COURSERA_CATALOG_API_ENDPOINT_COURSES)
        self.response_universities = university_dict#requests.get(CourseAPI.COURSERA_CATALOG_API_ENDPOINT_UNIVERSITIES)
        self.response_categories = categories_dict#requests.get(CourseAPI.COURSERA_CATALOG_API_ENDPOINT_CATEGORIES)
        self.response_instructors = instructor_dict#requests.get(CourseAPI.COURSERA_CATALOG_API_ENDPOINT_INSTRUCTORS)
        self.response_sessions  = sessions_dict#requests.get(CourseAPI.COURSERA_CATALOG_API_ENDPOINT_SESSIONS)

    def update_courses_database(self):

        result = []
        for item in self.response_courses['elements']:
            course = {}
            course['id'] = item['id']
            course['key'] = item['shortName']
            course['title'] = item['name']
            course['language'] = item['language']
            course['photo'] = item['photo']
            course['trailer'] = item['video']
            course['short_summary'] = item['shortDescription']
            course['summary'] = item['aboutTheCourse']
            course['recommended_background'] = item['recommendedBackground']
            course['syllabus'] = item['courseSyllabus']
            course['faq'] = item['faq']

            links = item['links']
            if 'instructors' in links:
                instructors = []
                for item_x in links['instructors']:
                    for item_y in self.response_instructors['elements']:
                        if item_x == item_y['id']:
                            instructors.append(item_y)
                course['instructors'] = instructors
            else:
                course['instructors'] = []

            if 'categories' in links:
                categories = []
                for item_x in links['categories']:
                    for item_y in self.response_categories['elements']:
                        if item_x == item_y['id']:
                            categories.append(item_y)
                course['categories'] = categories
            else:
                course['categories'] = []

            if 'universities' in links:
                universities = []
                for item_x in links['universities']:
                    for item_y in self.response_universities['elements']:
                        if item_x == item_y['id']:
                            universities.append(item_y)
                course['universities'] = universities
            else:
                course['universities'] = []

            if 'sessions' in links:
                sessions = []
                for item_x in links['sessions']:
                    for item_y in self.response_sessions['elements']:
                        if item_x == item_y['id']:
                            sessions.append(item_y)
                course['sessions'] = sessions
            else:
                course['sessions'] = []

            result.append(course)

        # Now Update Database
        for course in result:
            if not Course.objects.filter(title=course['title']).exists():

                all_courses = Course(course['id'], course['key'],course['title'], course['language'],
                            course['photo'], course['trailer'], course['short_summary'],
                            course['summary'], course['recommended_background'],
                            course['syllabus'], course['faq'])

                all_courses.save()

                all_instructors = []
                if course['instructors'] == [] :
                    all_instructors.append('None')

                for item in course['instructors'] :
                    instructor_item = Instructor(id=item['id'], first_name=item['firstName'], last_name=item['lastName'], suffix_name=item['suffixName'])
                    instructor_item.save()
                    all_courses.instructors.add(instructor_item)


                all_categories = []
                if course['categories'] == [] :
                    all_categories.append('None')

                for item in course['categories'] :
                    category_item = Category(id=item['id'], name=item['name'], short_name=item['shortName'])
                    category_item.save()
                    all_courses.categories.add(category_item)

                all_universities= []
                if course['universities'] == [] :
                    all_universities.append('None')

                for item in course['universities'] :
                    for key in ['name', 'banner', 'homeLink'] :
                        if key not in item :
                            item[key] = 'None'
                    university_item = University(id=item['id'], name=item['name'], banner=item['banner'], home_link=item['homeLink'])
                    university_item.save()
                    all_courses.universities.add(university_item)

                all_sessions = []
                if course['sessions'] == [] :
                    all_sessions.append('None')

                for item in course['sessions'] :
                    for key in ['homeLink', 'active', 'durationString', 'startDay', 'startMonth', 'startYear'] :
                        if key not in item :
                            item[key] = 'None'

                    session_item = Session(id=item['id'], home_link=item['homeLink'], active=item['active'], duration_string=item['durationString'],
                                start_day=item['startDay'],start_month=item['startMonth'],start_year=item['startYear'])
                    session_item.save()
                    all_courses.sessions.add(session_item)


from endless_pagination.views import AjaxListView
class CourseListView(FormMixin, AjaxListView) :

    model = Course
#    paginate_by = 20
    template_name = 'courses/courses_list.html'

    def get_queryset(self) :
        #course_object = CourseAPI()
        #course_object.update_courses_database()

        print 'Get', self.request.GET.get('cat')

        print 'Request', self.request.method, self.request.is_ajax(), self.request.POST.get('cat')
        if self.request.method == 'GET' :
            new_categories_selected = self.request.GET.getlist('cat')
            new_languages_selected = self.request.GET.getlist('lang')
            search_query           = self.request.GET.get('q')

            if new_categories_selected != [] and new_languages_selected != ['all'] and new_languages_selected != [] :
                queryset = \
                    Course.objects.filter(categories__short_name__in=new_categories_selected,
                        language__in=new_languages_selected).order_by('-id')
            elif new_categories_selected != [] :
                queryset = Course.objects.filter(categories__short_name__in=new_categories_selected).order_by('-id')
            elif new_languages_selected != [] and new_languages_selected != ['all']:
                queryset = Course.objects.filter(language__in=new_languages_selected).order_by('-id')
            elif search_query != None :
                queryset = Course.objects.filter(title__contains=search_query).order_by('-id')
            else :
                queryset = Course.objects.all().order_by('-id')

            return queryset


#        if self.request.method == "GET" :
#            queryset = Course.objects.filter(categories__in=self.request.GET('value'))
#            return queryset

        '''
        languages_selected = 'en'
        if languages_selected != 'All Languages' :
            queryset = Course.objects.filter(language__in=languages_selected)

        categories_selected = 'Arts'
        if categories_selected != 'All Categories' :
            queryset = Course.objects.filter(categories__in=categories_selected)

        if categories_selected != 'All Categories' and languages_selected != 'All Languages' :
            queryset = Course.objects.filter(categories__in=categories_selected, language__in=languages_selected)
        else :

        print 'Request', self.request.method, self.request.is_ajax(), self.request.POST.get('cat')
        if self.request.method == 'GET' : #and self.request.is_ajax() :

            new_categories_selected = []
            categories_selected = self.request.GET.get('cat')
            if categories_selected == None :
                categories_selected = 'undefined'

            for cat in categories_selected.split(',') :
                if cat.strip() != 'undefined' :
                    new_categories_selected.append(cat.replace('&amp;', '&'))

            new_languages_selected = self.

        '''

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')
        context['languages'] = LANGUAGE_CHOICES
        return context

class CourseDetailView(DetailView) :

    model = Course
    template_name = 'courses/course_detail.html'

    def get_success_url(self):
        #short_name    = self.kwargs['key']
        return reverse("course_detail", kwargs={"pk": self.kwargs['pk']})

    def get_queryset(self) :
        #short_name = self.kwargs['key']
        queryset = Course.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        course_sessions = Course.objects.get(id = self.kwargs['pk']).sessions.values_list()[0]
        context['session_weeks'] = course_sessions[3].strip()
        context['session_date'] = course_sessions[4].strip() + '-' + course_sessions[5].strip() + '-' + course_sessions[6].strip()

        course_instructors = Course.objects.get(id = self.kwargs['pk']).instructors.values_list()
        all_instructors = []
        for i in range(0, len(course_instructors)) :
            all_instructors.append(course_instructors[i][1].strip() + ' ' + course_instructors[i][2].strip())
        context['instructors'] = ', '.join(all_instructors)

        course_universities = Course.objects.get(id = self.kwargs['pk']).universities.values_list()[0]
        context['university_name'] = course_universities[1]
        context['university_logo'] = course_universities[2]
        context['university_link'] = course_universities[3]

        course_categories = Course.objects.get(id = self.kwargs['pk']).categories.values_list()
        all_categories = []
        for i in range(0, len(course_categories)) :
            all_categories.append(course_categories[i][1].strip() + ' ' + course_categories[i][2].strip())
        context['categories'] = ', '.join(all_categories)

        language = Course.objects.filter(pk = self.kwargs['pk']).values()[0]['language']
        context['language'] = language
        for lang in LANGUAGE_CHOICES :
            if language == lang[0] :
                context['language'] = lang[1]

        return context


class NewCourseListView(FormMixin, AjaxListView) :

    model = Course
    template_name = 'temp1.html'

    def get_queryset(self) :

        print 'GetList', self.request.GET.getlist('cat')
        print 'Get', self.request.GET.get('cat')

        print 'PostList', self.request.POST.getlist('cat')
        print 'Post', self.request.POST.get('cat')

        print 'Request', self.request.method, self.request.is_ajax(), self.request.POST.get('cat')

        '''
        if self.request.method == 'GET' :

            new_categories_selected = []
            categories_selected = self.request.GET.get('cat')
            if categories_selected == None :
                categories_selected = 'undefined'

            for cat in categories_selected.split(',') :
                if cat.strip() != 'undefined' :
                    new_categories_selected.append(cat.replace('&amp;', '&'))

            new_languages_selected = self.request.GET.getlist('lang')
            search_query           = self.request.GET.get('q')

            if new_categories_selected != [] and new_languages_selected != ['all'] and new_languages_selected != [] :
                queryset = \
                    Course.objects.filter(categories__short_name__in=new_categories_selected,
                        language__in=new_languages_selected).order_by('-id')
            elif new_categories_selected != [] :
                queryset = Course.objects.filter(categories__short_name__in=new_categories_selected).order_by('-id')
            elif new_languages_selected != [] and new_languages_selected != ['all']:
                queryset = Course.objects.filter(language__in=new_languages_selected).order_by('-id')
            elif search_query != None :
                queryset = Course.objects.filter(title__contains=search_query).order_by('-id')
            else :
        '''
        queryset = Course.objects.all().order_by('-id')
        return queryset


    def get_context_data(self, **kwargs):
        context = super(NewCourseListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')
        context['languages'] = LANGUAGE_CHOICES
        return context
