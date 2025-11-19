from django.shortcuts import render
"""
QuickBite Connect - Review Views
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import StoreReview, ProductReview, ReviewHelpful, ReviewReport
from .serializers import (
    StoreReviewSerializer,
    StoreReviewCreateSerializer,
    ProductReviewSerializer,
    ProductReviewCreateSerializer,
    ReviewReportSerializer
)


class StoreReviewListView(generics.ListAPIView):
    """API endpoint to list store reviews"""
    serializer_class = StoreReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        return StoreReview.objects.filter(
            store_id=store_id,
            is_approved=True
        )


class StoreReviewCreateView(generics.CreateAPIView):
    """API endpoint to create store review"""
    serializer_class = StoreReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        
        return Response({
            'review': StoreReviewSerializer(review).data,
            'message': 'Review submitted successfully!'
        }, status=status.HTTP_201_CREATED)


class ProductReviewListView(generics.ListAPIView):
    """API endpoint to list product reviews"""
    serializer_class = ProductReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(
            product_id=product_id,
            is_approved=True
        )


class ProductReviewCreateView(generics.CreateAPIView):
    """API endpoint to create product review"""
    serializer_class = ProductReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        
        return Response({
            'review': ProductReviewSerializer(review).data,
            'message': 'Review submitted successfully!'
        }, status=status.HTTP_201_CREATED)


class MyReviewsView(generics.ListAPIView):
    """API endpoint to list user's reviews"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all reviews by user"""
        store_reviews = StoreReview.objects.filter(user=request.user)
        product_reviews = ProductReview.objects.filter(user=request.user)
        
        return Response({
            'store_reviews': StoreReviewSerializer(store_reviews, many=True).data,
            'product_reviews': ProductReviewSerializer(product_reviews, many=True).data
        })


class ReviewHelpfulView(APIView):
    """API endpoint to mark review as helpful"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Mark review as helpful or not helpful"""
        review_type = request.data.get('review_type')  # 'store' or 'product'
        review_id = request.data.get('review_id')
        vote = request.data.get('vote')  # 'helpful' or 'not_helpful'
        
        if review_type not in ['store', 'product']:
            return Response(
                {'error': 'Invalid review type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if vote not in ['helpful', 'not_helpful']:
            return Response(
                {'error': 'Invalid vote'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create vote
        if review_type == 'store':
            review = get_object_or_404(StoreReview, id=review_id)
            vote_obj, created = ReviewHelpful.objects.get_or_create(
                user=request.user,
                store_review=review,
                defaults={'vote': vote}
            )
        else:
            review = get_object_or_404(ProductReview, id=review_id)
            vote_obj, created = ReviewHelpful.objects.get_or_create(
                user=request.user,
                product_review=review,
                defaults={'vote': vote}
            )
        
        # Update vote if exists
        if not created and vote_obj.vote != vote:
            # Update counts
            if vote_obj.vote == 'helpful':
                review.helpful_count -= 1
            else:
                review.not_helpful_count -= 1
            
            vote_obj.vote = vote
            vote_obj.save()
        
        # Update review counts
        if vote == 'helpful':
            review.helpful_count += 1
        else:
            review.not_helpful_count += 1
        review.save()
        
        return Response({'message': 'Vote recorded'})


class ReviewReportView(generics.CreateAPIView):
    """API endpoint to report inappropriate review"""
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set reported_by
        report = serializer.save(reported_by=request.user)
        
        return Response({
            'message': 'Report submitted successfully. Our team will review it.',
            'report': ReviewReportSerializer(report).data
        }, status=status.HTTP_201_CREATED)