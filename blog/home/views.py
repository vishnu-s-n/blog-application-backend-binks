from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer,LikeSerializer,CommentSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog,Like,Comment
from django.db.models import Q
from django.core.paginator import Paginator





# Every User can Read the blog without login

class PublicUserView(APIView):
    def get(self,request):

        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(description__icontains = search))

            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 3)


            serializer = BlogSerializer(paginator.page(page_number), many = True)

            return Response({
                'data' : serializer.data,
                'message' : 'blogs fetched successfully '
            }, status = status.HTTP_201_CREATED)
        

        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something wrong or invalid page'
            },status = status.HTTP_400_BAD_REQUEST)
         



# Only login user can create, read, patch,delete

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(description__icontains = search))


            serializer = BlogSerializer(blogs, many = True)

            return Response({
                'data' : serializer.data,
                'message' : 'blogs fetched successfully '
            }, status = status.HTTP_201_CREATED)
        

        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something wrong'
            },status = status.HTTP_400_BAD_REQUEST)



    def post(self,request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrongssssssss'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'data' : serializer.data,
                'message' : 'blog created'
            }, status = status.HTTP_201_CREATED)

    
        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something wrong'
            },status = status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request):
        try:
            data = request.data
            
            blog = Blog.objects.filter(id = data.get('id'))

            if not blog.exists():
                return Response({
                    'data' : {},
                    'message' : 'Invalid blog user'
                },status=status.HTTP_400_BAD_REQUEST)
            


            if request.user != blog[0].user:

                return Response({
                    'data' : {},
                    'message' : 'You are not authorized to this'
                },status=status.HTTP_400_BAD_REQUEST)
            

            serializer = BlogSerializer(blog[0], data=data, partial = True)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'Something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                    'data' : serializer.data,
                    'message' : 'Blog updated successfully'
                },status=status.HTTP_201_CREATED)
        

        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something wrong'
            },status = status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request):
        try:
            data = request.data
            
            blog = Blog.objects.filter(id = data.get('id'))

            if not blog.exists():
                return Response({
                    'data' : {},
                    'message' : 'Invalid blog user'
                },status=status.HTTP_400_BAD_REQUEST)
            


            if request.user != blog[0].user:

                return Response({
                    'data' : {},
                    'message' : 'You are not authorized to this'
                },status=status.HTTP_400_BAD_REQUEST)
            
            
            blog[0].delete()
            return Response({
                'data' : {},
                    'message' : 'Blog deleted successfully'
                },status=status.HTTP_201_CREATED)
        

        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something wrong'
            },status = status.HTTP_400_BAD_REQUEST)
        


# Like, Comment,ReplyComment

class BlogLikeView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        blog = Blog.objects.get(id=id)
        user = request.user
        try:
            like = Like.objects.get(blog=blog, user=user)
            like.delete()
            blog.likes -= 1
            blog.save()
            return Response({'message': 'Like removed.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            Like.objects.create(blog=blog, user=user)
            blog.likes += 1
            blog.save()
            return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)
        

class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        blog = Blog.objects.get(id=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReplyToCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, id):
        parent_comment = Comment.objects.get(id=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog=parent_comment.blog, parent_comment=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





            