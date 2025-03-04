# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import viewsets
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import generics
# from rest_framework.generics import (
#     CreateAPIView,
#     ListAPIView,
#     RetrieveAPIView,
#     UpdateAPIView,
#     DestroyAPIView,
#     ListCreateAPIView,
# )
# from courses.filters import PaymentFilter
# from courses.models import Course, Lesson, Payment
# from courses.serializers import (
#     CourseSerializer,
#     LessonSerializer,
#     CourseDetailSerializer,
#     PaymentSerializer,
# )
# from rest_framework.filters import SearchFilter, OrderingFilter
#
# class CourseViewSet(ModelViewSet):
#     queryset = Course.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == "retrieve":
#             return CourseDetailSerializer
#         return CourseSerializer
#
#
# class LessonViewSet(ModelViewSet):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonCreateApiView(CreateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonListApiView(ListAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonRetrieveApiView(RetrieveAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonUpdateApiView(UpdateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonDestroyApiView(DestroyAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#
#
#
# class PaymentListView(generics.ListCreateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = PaymentFilter
#
#     search_fields = [
#        'payment_date',
#        'paid_course__name',
#        'payment_method',
#    ]
#
#
#     ordering_fields = [
#         'payment_date',
#         'payment_amount',
#         'payment_method',
#     ]
#


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from courses.filters import PaymentFilter
from courses.models import Course, Lesson, Payment
from courses.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
    PaymentSerializer,
)
from users.permissions import IsModer, IsOwner, IsOwnerAndNotModer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwnerAndNotModer,
            )

        return super().get_permissions()


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return Lesson.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)

        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        course = Course.objects.get(id=course_id)
        serializer.save(course=course)


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Lesson.objects.filter(course_id=course_id)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwnerAndNotModer)




class PaymentListView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    search_fields = [
       'payment_date',
       'paid_course__name',
       'payment_method',
   ]


    ordering_fields = [
        'payment_date',
        'payment_amount',
        'payment_method',
    ]

