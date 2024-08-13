from fastapi import FastAPI, Security, Depends, HTTPException, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from chess_pairings import GameId
from pushed_over import notify

def upload_message(tournId: str, group: str, round: str, board: str):
  return f'Game uploaded for {tournId}/{group}/{round}/{board}'

def authorize(token: str):
  def bound(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    if auth.credentials != token:
      raise HTTPException(status_code=401, detail='Unauthorized')
  return bound

def api(token: str):
  app = FastAPI()

  @app.post('/game-upload')
  async def authed(gameId: GameId, auth = Depends(authorize(token))):
    title = f'Game Upload {gameId["tournId"]}'
    (await notify(title=title, message=upload_message(**gameId))).unsafe()

  png1x1 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfeA^\xa6t\x00\x00\x00\x00IEND\xaeB`\x82'

  @app.get('/open/{id}.png')
  async def notify_open(id: str):
    (await notify(title='Open Email', message=f'Received ID: "{id}"')).unsafe()
    return Response(content=png1x1, media_type='image/png')

  return app
