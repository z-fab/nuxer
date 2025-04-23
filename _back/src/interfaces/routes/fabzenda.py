from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from PIL import Image

from shared.config.settings import ASSETS_DIR

router = APIRouter(
    prefix="/fz",
    tags=["Fabzenda"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_fabzenda_root():
    return {"message": "Bem-vindo ao Fabzenda API"}


@router.get(
    "/animals/{animal_id}/image",
    response_class=StreamingResponse,
    responses={404: {"description": "Imagem não encontrada"}},
)
async def get_animal_image(animal_id: int):
    # bg_path = ASSETS_DIR / "fabzenda" / "bg.png"
    # galinha_path = ASSETS_DIR / "fabzenda" / "galinha.png"
    teste_path = ASSETS_DIR / "fabzenda" / "teste.png"

    # if not os.path.isfile(bg_path) or not os.path.isfile(galinha_path):
    #     raise HTTPException(status_code=404, detail="Imagem não encontrada")

    # with Image.open(bg_path).convert("RGBA") as bg, Image.open(galinha_path).convert("RGBA") as galinha:
    #     # Redimensiona a galinha para 32x32
    #     galinha_resized = galinha.resize((384, 384), Image.LANCZOS)
    #     bg_resized = bg.resize((512, 512), Image.LANCZOS)
    #     # Centraliza a galinha no fundo
    #     bg_w, bg_h = bg_resized.size
    #     g_w, g_h = galinha_resized.size
    #     pos = ((bg_w - g_w) // 2, (bg_h - g_h) // 2)
    #     composed = bg_resized.copy()
    #     composed.paste(galinha_resized, pos, galinha_resized)

    #     # Salva em memória
    #     buf = BytesIO()
    #     composed.save(buf, format="PNG")
    #     buf.seek(0)

    with Image.open(teste_path).convert("RGBA") as bg:
        # renderiza a imagem teste
        bg_resized = bg.resize((512, 512), Image.LANCZOS)
        # Salva em memória
        buf = BytesIO()
        bg_resized.save(buf, format="PNG")
        buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
