from dotenv import load_dotenv
load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

import pathlib
import os

config = cloudinary.config(secure=True)
supported_files = (".png", ".jpg", ".jpeg")

# uploading image function
def upload_image(filename, folder="my_photos"):
    stem = pathlib.Path(filename).stem
    res = cloudinary.uploader.upload(filename, public_id=stem, folder=folder)
    return res

def upload_and_tag_image(filename, folder="my_photos"):
    stem = pathlib.Path(filename).stem
    res = cloudinary.uploader.upload(filename, 
                                    public_id=stem, 
                                    folder=folder,
                                    detection="openimages",
                                    auto_tagging=0.25)
    return res



def upload_folder():
    n = 0
    for file in sorted(os.listdir("random_images")):
        if pathlib.Path(file).suffix.lower() in supported_files:
            try:
                print(file)
                upload_and_tag_image("random_images/" + file)
                n += 1
            except Exception as e:
                print("failed for ",file)
                print(e)
    print(n, " photos uploaded")

def get_all_tags():
    all_tags = []
    tags = cloudinary.api.tags(max_result=100)
    all_tags.extend(tags['tags'])
    next_cursor = tags.get('next_cursor')

    while next_cursor:
        tags = cloudinary.api.tags(max_result=100, next_cursor=next_cursor)
        all_tags.extend(tags['tags'])
        next_cursor = tags.get('next_cursor')

    return all_tags

#all_tags = get_all_tags()
#print(all_tags)

def search_img():
    result = cloudinary.Search().expression("resource_type:image AND tags=girl").sort_by("public_id", "desc").execute()
    return result

def get_all_images_with_tags():
    all_resources = []
    result = cloudinary.api.resources(
        type= "upload",
        resource_type="image",
        prefix="my_photos",
        tags = True,
        max_result=100
    )
    all_resources.extend(result['resources'])
    next_cursor = result.get("next_cursor")

    while next_cursor:
        result = cloudinary.api.resources(
            type= "upload",
            resource_type="image",
            prefix="my_photos",
            tags = True,
            max_result=100,
            next_cursor = next_cursor
        )
        all_resources.extend(result['resources'])
        next_cursor = result.get("next_cursor")        
    return all_resources

all_resources = get_all_images_with_tags()
#print(all_resources)
#print(len(all_resources))