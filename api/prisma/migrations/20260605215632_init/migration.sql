-- CreateTable
CREATE TABLE "users" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "google_sub" TEXT,
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "progreso" (
    "user_id" TEXT NOT NULL,
    "estado" JSONB NOT NULL DEFAULT '{}',
    "actualizado" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "progreso_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "perfiles" (
    "user_id" TEXT NOT NULL,
    "handle" TEXT NOT NULL,
    "nombre" TEXT NOT NULL DEFAULT '',
    "avatar" INTEGER NOT NULL DEFAULT 0,
    "codigo_amigo" TEXT NOT NULL,
    "publico" JSONB NOT NULL DEFAULT '{}',
    "descripcion" TEXT NOT NULL DEFAULT '',
    "actualizado" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "perfiles_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "amistades" (
    "id" TEXT NOT NULL,
    "de_id" TEXT NOT NULL,
    "a_id" TEXT NOT NULL,
    "estado" TEXT NOT NULL DEFAULT 'pendiente',
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "amistades_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ofertas" (
    "id" TEXT NOT NULL,
    "de_id" TEXT NOT NULL,
    "a_id" TEXT NOT NULL,
    "doy" JSONB NOT NULL DEFAULT '[]',
    "pido" JSONB NOT NULL DEFAULT '[]',
    "estado" TEXT NOT NULL DEFAULT 'pendiente',
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "resuelto" TIMESTAMP(3),

    CONSTRAINT "ofertas_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "intercambios" (
    "id" TEXT NOT NULL,
    "codigo" TEXT NOT NULL,
    "creador_id" TEXT NOT NULL,
    "invitado_id" TEXT,
    "creador_nombre" TEXT NOT NULL DEFAULT '',
    "invitado_nombre" TEXT NOT NULL DEFAULT '',
    "creador_lote" JSONB NOT NULL DEFAULT '[]',
    "invitado_lote" JSONB NOT NULL DEFAULT '[]',
    "creador_pedido" JSONB NOT NULL DEFAULT '[]',
    "invitado_pedido" JSONB NOT NULL DEFAULT '[]',
    "creador_ok" BOOLEAN NOT NULL DEFAULT false,
    "invitado_ok" BOOLEAN NOT NULL DEFAULT false,
    "estado" TEXT NOT NULL DEFAULT 'abierta',
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "actualizado" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "intercambios_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "desafios" (
    "id" TEXT NOT NULL,
    "autor" TEXT NOT NULL,
    "titulo" TEXT NOT NULL,
    "consigna" TEXT NOT NULL DEFAULT '',
    "func" TEXT NOT NULL,
    "starter" TEXT NOT NULL DEFAULT '',
    "casos" JSONB NOT NULL DEFAULT '[]',
    "dificultad" INTEGER NOT NULL DEFAULT 3,
    "region" TEXT NOT NULL DEFAULT 'libre',
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "desafios_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "resoluciones" (
    "id" TEXT NOT NULL,
    "desafio_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "codigo" TEXT NOT NULL DEFAULT '',
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "resoluciones_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "votos" (
    "resolucion_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,

    CONSTRAINT "votos_pkey" PRIMARY KEY ("resolucion_id","user_id")
);

-- CreateTable
CREATE TABLE "reportes" (
    "desafio_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "motivo" TEXT NOT NULL DEFAULT '',
    "creado" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "reportes_pkey" PRIMARY KEY ("desafio_id","user_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE UNIQUE INDEX "users_google_sub_key" ON "users"("google_sub");

-- CreateIndex
CREATE UNIQUE INDEX "perfiles_handle_key" ON "perfiles"("handle");

-- CreateIndex
CREATE UNIQUE INDEX "perfiles_codigo_amigo_key" ON "perfiles"("codigo_amigo");

-- CreateIndex
CREATE UNIQUE INDEX "amistades_de_id_a_id_key" ON "amistades"("de_id", "a_id");

-- CreateIndex
CREATE UNIQUE INDEX "intercambios_codigo_key" ON "intercambios"("codigo");

-- CreateIndex
CREATE UNIQUE INDEX "resoluciones_desafio_id_user_id_key" ON "resoluciones"("desafio_id", "user_id");
