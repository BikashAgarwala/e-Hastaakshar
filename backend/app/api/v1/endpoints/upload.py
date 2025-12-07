from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ipfs_service import ipfs_client

router = APIRouter()


@router.post("/upload-file")
async def upload_to_ipfs(file: UploadFile = File(...)):

    file_content = await file.read()
    cid = ipfs_client.upload_file(file_content, file.filename)

    if not cid:
        raise HTTPException(status_code=500, detail="Failed to upload to Pinata")

    public_url = ipfs_client.generate_public_url(cid)

    return {
        "status": "success",
        "filename": file.filename,
        "ipfs_cid": cid,
        "public_url": public_url,
        "message": "File is now permanently on the decentralized web!"
    }