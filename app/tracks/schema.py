import graphene
from graphene_django import DjangoObjectType

from .models import Track

class TrackType(DjangoObjectType):
    class Meta:
        model=Track

class Query(graphene.ObjectType):
    tracks =graphene.List(TrackType)

    def resolve_tracks(self ,info):
        return Track.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title=graphene.String()
        description = graphene.String()
        url =graphene.String()
        
    def mutate(self,info,title,description,url):
        user=info.context.user
        if user.is_anonymous:
            raise Exception('Log in to add a trak ')
        track =Track(title=title,description=description,url=url,posted_by=user)
        track.save()
        return CreateTrack(track=track)    
    
class DeleteTrack(graphene.Mutation):
    track_id = graphene.Field(TrackType)
    class Arguments:
        track_id=graphene.Int(required=True)
        
    def mutate(self,info,track_id):
        # user= info.context.user
        track =Track.objects.get(id=track_id)
        track.delete()
        return DeleteTrack(track_id=track_id)



class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    # update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()