from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stream


# Create your views here.
def index(request):
    streams = Stream.objects.all()
    return render(request, 'streams/index.html', {'streams': streams})


@login_required
def start_stream(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        stream = Stream(title=title, description=description, user=request.user)
        stream.start_stream()

        print(stream.id)

        return redirect('stream_detail', stream_id=stream.id)

    return render(request, 'streams/start_stream.html')


@login_required
def stop_stream(request, stream_id):
    stream = Stream.objects.get(id=stream_id)

    if stream.user == request.user:
        stream.stop_stream()

    return redirect('stream_detail', stream_id=stream.id)


def stream_detail(request, stream_id):
    # Retrieve the stream object or return a 404 error if it doesn't exist
    stream = get_object_or_404(Stream, id=stream_id)

    context = {
        'stream': stream,
        'websocket_url': f'wss://127.0.0.1:8000/stream/${stream_id}/'
    }

    return render(request, 'streams/stream_detail.html', context)
