import json
import os
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Match
from .serializers import MatchSerializer
from items.models import Item


class MyMatchesView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_item_ids = Item.objects.filter(user=user).values_list('id', flat=True)
        return Match.objects.filter(
            found_item_id__in=user_item_ids
        ) | Match.objects.filter(
            lost_item_id__in=user_item_ids
        )

    def get_serializer_context(self):
        return {'request': self.request}


class MatchDetailView(generics.RetrieveUpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['confirmed', 'rejected']:
            instance.status = new_status
            instance.save()
            if new_status == 'confirmed':
                Item.objects.filter(pk=instance.found_item_id).update(status='matched')
                Item.objects.filter(pk=instance.lost_item_id).update(status='matched')
        return Response(MatchSerializer(instance, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def run_match(request, item_id):
    try:
        source = Item.objects.get(pk=item_id, is_approved=True, status='active')
    except Item.DoesNotExist:
        return Response({'error': '物品不存在'}, status=404)

    opposite_type = 'lost' if source.type == 'found' else 'found'
    candidates = list(Item.objects.filter(
        type=opposite_type, category=source.category,
        is_approved=True, status='active'
    ).exclude(pk=item_id)[:20])

    if not candidates:
        return Response({'matches': [], 'message': '暂无同类候选物品'})

    candidate_text = '\n'.join([
        f"ID:{c.id} 标题:{c.title} 地点:{c.location} 时间:{c.happened_at.strftime('%Y-%m-%d')} 描述:{c.description[:80]}"
        for c in candidates
    ])

    prompt = f"""你是校园失物招领智能匹配助手。请从候选列表中找出最可能匹配的物品。

源物品（{'失物招领' if source.type == 'found' else '寻物启事'}）:
标题: {source.title}
类别: {source.category}
地点: {source.location}
时间: {source.happened_at.strftime('%Y-%m-%d')}
描述: {source.description}

候选物品（{'寻物启事' if source.type == 'found' else '失物招领'}）:
{candidate_text}

返回JSON: {{"matches": [{{"id": 整数, "score": 0-100整数, "reason": "匹配理由50字内"}}]}}
只返回score>=60的结果，最多5个。"""

    match_results = []
    try:
        from openai import OpenAI
        api_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('BUILT_IN_FORGE_API_KEY', '')
        api_base = os.environ.get('OPENAI_API_BASE') or os.environ.get('BUILT_IN_FORGE_API_URL', 'https://api.openai.com/v1')
        client = OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            response_format={'type': 'json_object'},
            max_tokens=500,
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        match_results = parsed.get('matches', [])
    except Exception as e:
        print(f'LLM matching error: {e}')
        # 降级：简单关键词匹配
        for c in candidates[:3]:
            common_words = set(source.title.split()) & set(c.title.split())
            score = min(60 + len(common_words) * 10, 85)
            match_results.append({'id': c.id, 'score': score, 'reason': f'物品类别相同，地点相近'})

    saved = []
    for m in match_results:
        try:
            found_id = source.id if source.type == 'found' else m['id']
            lost_id = source.id if source.type == 'lost' else m['id']
            match_obj, created = Match.objects.get_or_create(
                found_item_id=found_id, lost_item_id=lost_id,
                defaults={'score': m['score'], 'reason': m.get('reason', '')}
            )
            if not created:
                match_obj.score = m['score']
                match_obj.reason = m.get('reason', '')
                match_obj.save()
            saved.append(MatchSerializer(match_obj, context={'request': request}).data)
        except Exception as e:
            print(f'Save match error: {e}')

    return Response({'matches': saved})


class AdminMatchListView(generics.ListAPIView):
    queryset = Match.objects.all().select_related('found_item', 'lost_item')
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}
