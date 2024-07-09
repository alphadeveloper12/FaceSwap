import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  # Import the settings module
from .forms import ImageUploadForm
from .models import ImageUpload
from dofaker import FaceSwapper


@csrf_exempt
def swap_faces(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save()
            input_path = image_upload.input_image.path
            dst_path = image_upload.dst_image.path
            src_path = image_upload.src_image.path
            use_enhancer = False
            use_sr = False
            scale = 1
            face_sim_thre = 0.6

            # Perform face swap
            faker = FaceSwapper(use_enhancer=use_enhancer,
                                use_sr=use_sr,
                                scale=scale,
                                face_sim_thre=face_sim_thre)

            # Ensure the output directory exists
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
            os.makedirs(output_dir, exist_ok=True)

            # Set the output path
            output_path = faker.run(input_path, dst_path, src_path)
            output_filename = os.path.basename(output_path)
            final_output_path = os.path.join(output_dir, output_filename)
            os.rename(output_path, final_output_path)

            # Save the output path in the model
            image_upload.output_image.name = os.path.relpath(final_output_path, settings.MEDIA_ROOT)
            image_upload.save()

            return JsonResponse({'output_image_url': image_upload.output_image.url})
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
