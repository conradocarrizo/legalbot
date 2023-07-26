from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from societies.filters import SocietyFilter
from societies.models import Person, Society, SocietyAdmin, SocietyMember
from societies.serializers import (
    CreateSocietyMemberSerializer,
    CreateSocietyAdminSerializer,
    SocietyListPersonSerializer,
    SocietySerializer,
    RetrieveSocietySerializer,
)
from django.db import transaction
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F


class SocietyViewSet(viewsets.ModelViewSet):
    queryset = Society.objects.all().prefetch_related(
        "societymember_set", "societyadmin_set"
    )
    serializer_class = RetrieveSocietySerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SocietyFilter

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = SocietySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def create_member(self, request, pk=None):
        try:
            society = self.get_object()
            serializer = CreateSocietyMemberSerializer(
                data=request.data, context={"society": society}
            )
            serializer.is_valid(raise_exception=True)
            member = serializer.save()

            return Response(
                {"message": "Miembro agregado exitosamente", "member_id": member.id},
                status=status.HTTP_201_CREATED,
            )
        except Society.DoesNotExist:
            return Response(
                data={"Sociedad no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def create_admin(self, request, pk=None):
        try:
            society = self.get_object()
            serializer = CreateSocietyAdminSerializer(
                data=request.data, context={"society": society}
            )
            serializer.is_valid(raise_exception=True)
            admin = serializer.save()

            return Response(
                {"message": "Admin agregado exitosamente", "admin_id": admin.id},
                status=status.HTTP_201_CREATED,
            )
        except Society.DoesNotExist:
            return Response(
                data={"Sociedad no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"])
    def list_by_person_rut(self, request):
        rut = request.query_params.get("rut")
        if not rut:
            return Response(
                data={"message": "debe enviar el rut"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            person = Person.objects.get(rut__code=rut)

            admin_societies = (
                SocietyAdmin.objects.filter(admin=person)
                .annotate(name=F("society__rut__name"), rut=F("society__rut__code"))
                .values("name", "rut", "faculties")
            )
            member_societies = (
                SocietyMember.objects.filter(member=person)
                .annotate(
                    name=F("society__rut__name"),
                    rut=F("society__rut__code"),
                    porcentage=F("actions") / F("society__actions"),
                )
                .values(
                    "name",
                    "rut",
                    "porcentage",
                )
            )

            serializer = SocietyListPersonSerializer(
                instance=person,
                context={
                    "admin_societies": admin_societies,
                    "member_societies": member_societies,
                },
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response(
                data={"persona no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
