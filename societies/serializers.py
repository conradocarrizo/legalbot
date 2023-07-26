from rest_framework import serializers
from societies.models import Rut, Society, Person, SocietyMember, SocietyAdmin


class RutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rut
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    rut = RutSerializer()

    class Meta:
        model = Person
        fields = "__all__"

    def create(self, validated_data):
        rut_data = validated_data.pop("rut")
        rut = Rut.objects.create(**rut_data)
        person = Person.objects.create(rut=rut, **validated_data)
        return person


class CreateSocietyMemberSerializer(serializers.Serializer):
    rut = RutSerializer()
    address = serializers.CharField(max_length=100)
    actions = serializers.IntegerField()

    def create(self, validated_data):
        rut_data = validated_data.pop("rut")
        address = validated_data.pop("address")
        rut, _ = Rut.objects.get_or_create(
            code=rut_data["code"], defaults={"name": rut_data["name"]}
        )
        member, _ = Person.objects.get_or_create(rut=rut, address=address)
        society = self.context.get("society")

        society_member = SocietyMember.objects.create(
            society=society, member=member, actions=validated_data["actions"]
        )
        return society_member.member


class CreateSocietyAdminSerializer(serializers.Serializer):
    rut = RutSerializer()
    address = serializers.CharField(max_length=100)
    faculties = serializers.ListField(child=serializers.CharField(max_length=50))

    def create(self, validated_data):
        rut_data = validated_data.pop("rut")
        address = validated_data.pop("address")

        rut, _ = Rut.objects.get_or_create(
            code=rut_data["code"], defaults={"name": rut_data["name"]}
        )
        admin, _ = Person.objects.get_or_create(rut=rut, address=address)
        society = self.context.get("society")

        society_admin = SocietyAdmin.objects.create(
            society=society, admin=admin, faculties=validated_data["faculties"]
        )
        return society_admin.admin


class SocietySerializer(serializers.ModelSerializer):
    rut = RutSerializer()

    class Meta:
        model = Society
        fields = "__all__"

    def create(self, validated_data):
        rut_data = validated_data.pop("rut")
        rut = Rut.objects.create(**rut_data)
        society = Society.objects.create(rut=rut, **validated_data)
        return society


class SocietyAdminSerializer(serializers.ModelSerializer):
    admin = PersonSerializer()

    class Meta:
        model = SocietyAdmin
        fields = "__all__"


class SocietyMemberSerializer(serializers.ModelSerializer):
    member = PersonSerializer()
    participation = serializers.SerializerMethodField()

    class Meta:
        model = SocietyMember
        fields = "__all__"

    def get_participation(self, instance):
        return f"{instance.participation * 100}%"


class RetrieveSocietySerializer(serializers.ModelSerializer):
    rut = RutSerializer()
    admins = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Society
        fields = "__all__"

    def get_admins(self, instance):
        admins = instance.societyadmin_set.all()
        serializer = SocietyAdminSerializer(admins, many=True)

        return serializer.data

    def get_members(self, instance):
        members = instance.societymember_set.all()
        serializer = SocietyMemberSerializer(members, many=True)

        return serializer.data


class AdminSocieties(serializers.Serializer):
    name = serializers.CharField()
    rut = serializers.CharField()
    faculties = serializers.ListField(child=serializers.CharField(max_length=50))


class MemberSocieties(serializers.Serializer):
    name = serializers.CharField()
    rut = serializers.CharField()
    porcentage = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        porcentage_value = float(representation["porcentage"])
        porcentage_str = f"{porcentage_value:.0%}"
        representation["porcentage"] = porcentage_str
        return representation


class SocietyListPersonSerializer(serializers.Serializer):
    rut = RutSerializer()
    admin_societies = serializers.SerializerMethodField()
    member_societies = serializers.SerializerMethodField()

    def get_admin_societies(self, obj):
        serialized_societies = []

        societies = self.context.get("admin_societies", [])
        for society in societies:
            ser = AdminSocieties(data=society)
            if ser.is_valid():
                serialized_societies.append(ser.data)

        return serialized_societies

    def get_member_societies(self, obj):
        serialized_societies = []

        societies = self.context.get("member_societies", [])
        for society in societies:
            ser = MemberSocieties(data=society)
            if ser.is_valid():
                serialized_societies.append(ser.data)

        return serialized_societies
