from rest_framework import serializers
from fighters.models import Fighter
from fighters.models import Weightclass
from django.contrib.auth.models import User
import fighters.views

class UserFighterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fighter
        fields = (
            'url',
            'name'
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    fighters = UserFighterSerializer(many=True, read_only=True)

    class Meta:
        model = User
        field = (
            'url',
            'pk',
            'username',
            'fighters'
        )

class WeightclassSerializer(serializers.HyperlinkedModelSerializer):
    fighters = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='fighter-detail'
    )

    class Meta:
        model = Weightclass
        exclude = ('')
        field = (
            'url',
            'pk',
            'name',
            'fighters'
        )

class FighterSerializer(serializers.HyperlinkedModelSerializer):
    # We just want to display the owner username (read-only)
    owner = serializers.ReadOnlyField(source='owner.username')
    
    weightclass = serializers.SlugRelatedField(queryset=Weightclass.objects.all(), slug_field='name')
    class Meta:
        model = Fighter
        exclude = ('')
        fields = (
            'url',
            'name',
            'birthplace',
            'age',
            'height',
            'weight',
            'reach',
            'wins',
            'losses',
            'draws',
            'weightclass',
            'latitude',
            'longitude',
            'owner'
        )