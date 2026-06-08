-- Ban de usuarios (moderación). El admin lo togglea; la auth rechaza el login si está baneado.
ALTER TABLE "users" ADD COLUMN "baneado" BOOLEAN NOT NULL DEFAULT false;
