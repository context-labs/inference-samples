---
title: Servidor HTTP de Node.js
description: Aprende a utilizar el SDK de IA en un servidor HTTP de Node.js
tags: ['servidores de API', 'transmisión en streaming']
---

# Servidor HTTP de Node.js

Puedes utilizar el SDK de IA en un servidor HTTP de Node.js para generar texto y transmitirlo al cliente.

## Ejemplos

Los ejemplos arrancan un servidor HTTP simple que escucha en el puerto 8080. Puedes probarlo utilizando `curl`:

```bash
curl -X POST http://localhost:8080
```

<Nota>
  Los ejemplos utilizan el modelo de OpenAI `gpt-4o`. Asegúrate de que la clave de API de OpenAI esté configurada en la variable de entorno `OPENAI_API_KEY`.
</Nota>

**Ejemplo completo**: [github.com/vercel/ai/examples/node-http-server](https://github.com/vercel/ai/tree/main/examples/node-http-server)

### Transmisión de datos

Puedes utilizar el método `pipeDataStreamToResponse` para transmitir los datos de la transmisión al servidor de respuesta.

```ts filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { createServer } from 'http';

createServer(async (req, res) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  });

  result.pipeDataStreamToResponse(res);
}).listen(8080);
```

### Enviando datos personalizados

`pipeDataStreamToResponse` se puede utilizar para enviar datos personalizados al cliente.

```ts filename='index.ts' highlight="6-9,16"
import { openai } from '@ai-sdk/openai';
import { pipeDataStreamToResponse, streamText } from 'ai';
import { createServer } from 'http';

createServer(async (req, res) => {
  // inicia inmediatamente la transmisión de la respuesta
  pipeDataStreamToResponse(res, {
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('llamada inicializada');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: error => {
      // Los mensajes de error están ocultos por defecto por razones de seguridad.
      // Si deseas exponer el mensaje de error al cliente, puedes hacerlo aquí:
      return error instanceof Error ? error.message : String(error);
    },
  });
}).listen(8080);
```

### Flujo de texto

Puedes enviar un flujo de texto al cliente utilizando `pipeTextStreamToResponse`.

```ts filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { createServer } from 'http';

createServer(async (req, res) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  });

  result.pipeTextStreamToResponse(res);
}).listen(8080);
```

## Solución de Problemas

- No funciona el streaming cuando se utiliza [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
titulo: Express
descripcion: Aprende a utilizar la SDK de IA en un servidor Express
etiquetas: ['servidores de API', 'streaming']
---

# Express

Puedes utilizar la SDK de IA en un [Express](https://expressjs.com/) para generar y enviar flujos de texto y objetos al cliente.

## Ejemplos

Los ejemplos inician un servidor HTTP simple que escucha en el puerto 8080. Puedes probarlo utilizando `curl`:

```bash
curl -X POST http://localhost:8080
```

<Nota>
  Los ejemplos utilizan el modelo de OpenAI `gpt-4o`. Asegúrate de que la clave de la API de OpenAI esté configurada en la variable de entorno `OPENAI_API_KEY`.
</Nota>

**Ejemplo completo**: [github.com/vercel/ai/examples/express](https://github.com/vercel/ai/tree/main/examples/express)

### Flujo de Datos

Puedes utilizar el método `pipeDataStreamToResponse` para enviar el flujo de datos a la respuesta del servidor.

```typescript filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import express, { Request, Response } from 'express';

const app = express();

app.post('/', async (req: Request, res: Response) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  });

  result.pipeDataStreamToResponse(res);
});

app.listen(8080, () => {
  console.log(`El ejemplo del servidor está escuchando en el puerto ${8080}`);
});
```

### Enviar Datos Personalizados

`pipeDataStreamToResponse` se puede utilizar para enviar datos personalizados al cliente.

```ts filename='index.ts' highlight="8-11,18"
import { openai } from '@ai-sdk/openai';
import { pipeDataStreamToResponse, streamText } from 'ai';
import express, { Request, Response } from 'express';

const app = express();

app.post('/stream-data', async (req: Request, res: Response) => {
  // inicia inmediatamente la transmisión de la respuesta
  pipeDataStreamToResponse(res, {
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('llamada inicializada');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: error => {
      // Los mensajes de error están ocultos por motivos de seguridad.
      // Si deseas exponer el mensaje de error al cliente, puedes hacerlo aquí:
      return error instanceof Error ? error.message : String(error);
    },
  });
});

app.listen(8080, () => {
  console.log(`Ejemplo de aplicación escuchando en el puerto ${8080}`);
});
```

### Flujo de texto

Puedes enviar un flujo de texto al cliente utilizando `pipeTextStreamToResponse`.

```ts filename='index.ts' highlight="13"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import express, { Request, Response } from 'express';

const app = express();

app.post('/', async (req: Request, res: Response) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  });

  result.pipeTextStreamToResponse(res);
});

app.listen(8080, () => {
  console.log(`El ejemplo de aplicación está escuchando en el puerto ${8080}`);
});
```

## Solución de problemas

- El streaming no funciona cuando se utiliza [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
titulo: Hono
descripcion: Ejemplo de uso del SDK de IA en un servidor Hono.
etiquetas: ['servidores de API', 'streaming']
---

# Hono

Puedes utilizar el SDK de IA en un [Hono](https://hono.dev/) para generar y enviar flujos de texto y objetos al cliente.

## Ejemplos

Los ejemplos arrancan un servidor HTTP simple que escucha en el puerto 8080. Puedes probarlo utilizando `curl`:

```bash
curl -X POST http://localhost:8080
```

<Nota>
  Los ejemplos utilizan el modelo de OpenAI `gpt-4o`. Asegúrate de que la clave de API de OpenAI esté configurada en la variable de entorno `OPENAI_API_KEY`.
</Nota>

**Ejemplo completo**: [github.com/vercel/ai/examples/hono](https://github.com/vercel/ai/tree/main/examples/hono)

### Flujo de Datos

Puedes utilizar el método `toDataStream` para obtener un flujo de datos desde el resultado y luego enviarlo a la respuesta.

```ts filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { serve } from '@hono/node-server';
import { streamText } from 'ai';
import { Hono } from 'hono';
import { stream } from 'hono/streaming';

const app = new Hono();

app.post('/', async c => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  });

  // Marca la respuesta como un flujo de datos v1:
  c.header('X-Vercel-AI-Data-Stream', 'v1');
  c.header('Content-Type', 'text/plain; charset=utf-8');

  return stream(c, stream => stream.pipe(result.toDataStream()));
});

serve({ fetch: app.fetch, port: 8080 });
```

### Enviar Datos Personalizados

`createDataStream` se puede utilizar para enviar datos personalizados al cliente.

```ts filename='index.ts' highlight="10-13,20"
import { openai } from '@ai-sdk/openai';
import { serve } from '@hono/node-server';
import { createDataStream, streamText } from 'ai';
import { Hono } from 'hono';
import { stream } from 'hono/streaming';

const app = new Hono();

app.post('/stream-data', async c => {
  // inicia inmediatamente la transmisión de la respuesta
  const dataStream = createDataStream({
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('llamada inicializada');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: error => {
      // Los mensajes de error están ocultos por defecto por razones de seguridad.
      // Si deseas exponer el mensaje de error al cliente, puedes hacerlo aquí:
      return error instanceof Error ? error.message : String(error);
    },
  });

  // Marca la respuesta como un flujo de datos v1:
  c.header('X-Vercel-AI-Data-Stream', 'v1');
  c.header('Content-Type', 'text/plain; charset=utf-8');

  return stream(c, stream =>
    stream.pipe(dataStream.pipeThrough(new TextEncoderStream())),
  );
});

serve({ fetch: app.fetch, port: 8080 });
```

### Flujo de Texto

Puedes utilizar la propiedad `textStream` para obtener un flujo de texto desde el resultado y luego pipiarlo a la respuesta.

```ts filename='index.ts' highlight="17"
import { openai } from '@ai-sdk/openai';
import { serve } from '@hono/node-server';
import { streamText } from 'ai';
import { Hono } from 'hono';
import { stream } from 'hono/streaming';

const app = new Hono();

app.post('/', async c => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  });

  c.header('Content-Type', 'text/plain; charset=utf-8');

  return stream(c, stream => stream.pipe(result.textStream));
});

serve({ fetch: app.fetch, port: 8080 });
```

## Resolución de Problemas

- El streaming no funciona cuando se utiliza [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
titulo: Fastify
descripcion: Aprende a utilizar el SDK de IA en un servidor Fastify
etiquetas: ['servidores API', 'streaming']
---

# Fastify

Puedes utilizar el SDK de IA en un servidor [Fastify](https://fastify.dev/) para generar y enviar flujos de texto y objetos al cliente.

## Ejemplos

Los ejemplos inician un servidor HTTP simple que escucha en el puerto 8080. Puedes probarlo utilizando `curl`:

```bash
curl -X POST http://localhost:8080
```

<Nota>
  Los ejemplos utilizan el modelo de OpenAI `gpt-4o`. Asegúrate de que la clave de API de OpenAI esté configurada en la variable de entorno `OPENAI_API_KEY`.
</Nota>

**Ejemplo completo**: [github.com/vercel/ai/examples/fastify](https://github.com/vercel/ai/tree/main/examples/fastify)

### Flujo de Datos

Puedes utilizar el método `toDataStream` para obtener un flujo de datos desde el resultado y luego enviarlo a la respuesta.

```ts filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.post('/', async function (request, reply) {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo día festivo y describe sus tradiciones.',
  });

  // Marca la respuesta como un flujo de datos v1:
  reply.header('X-Vercel-AI-Data-Stream', 'v1');
  reply.header('Content-Type', 'text/plain; charset=utf-8');

  return reply.send(result.toDataStream({ data }));
});

fastify.listen({ port: 8080 });
```

### Enviar Datos Personalizados

`createDataStream` se puede utilizar para enviar datos personalizados al cliente.

```ts filename='index.ts' highlight="8-11,18"
import { openai } from '@ai-sdk/openai';
import { createDataStream, streamText } from 'ai';
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.post('/stream-data', async function (request, reply) {
  // inicia inmediatamente la transmisión de la respuesta
  const dataStream = createDataStream({
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('llamada inicializada');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: error => {
      // Los mensajes de error están ocultos por motivos de seguridad.
      // Si deseas exponer el mensaje de error al cliente, puedes hacerlo aquí:
      return error instanceof Error ? error.message : String(error);
    },
  });

  // Marca la respuesta como un flujo de datos v1:
  reply.header('X-Vercel-AI-Data-Stream', 'v1');
  reply.header('Content-Type', 'text/plain; charset=utf-8');

  return reply.send(dataStream);
});

fastify.listen({ port: 8080 });
```

### Flujo de Texto

Puedes utilizar la propiedad `textStream` para obtener un flujo de texto desde el resultado y luego enviarlo a la respuesta.

```ts filename='index.ts' highlight="15"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.post('/', async function (request, reply) {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventa un nuevo día festivo y describe sus tradiciones.',
  });

  reply.header('Content-Type', 'text/plain; charset=utf-8');

  return reply.send(result.textStream);
});

fastify.listen({ port: 8080 });
```

## Resolución de Problemas

- El streaming no funciona cuando se utiliza [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
title: Nest.js
description: Aprende a utilizar el SDK de IA en un servidor Nest.js
tags: ['servidores de API', 'streaming']
---

# Nest.js

Puedes utilizar el SDK de IA en un servidor [Nest.js](https://nestjs.com/) para generar y enviar flujos de texto y objetos al cliente.

## Ejemplos

Los ejemplos muestran cómo implementar un controlador de Nest.js que utiliza el SDK de IA para enviar flujos de texto y objetos al cliente.

**Ejemplo completo**: [github.com/vercel/ai/examples/nest](https://github.com/vercel/ai/tree/main/examples/nest)

### Flujo de Datos

Puedes utilizar el método `pipeDataStreamToResponse` para obtener un flujo de datos desde el resultado y luego enviarlo a la respuesta.

```ts filename='app.controller.ts'
import { Controller, Post, Res } from '@nestjs/common';
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { Response } from 'express';

@Controller()
export class AppController {
  @Post()
  async ejemplo(@Res() res: Response) {
    const resultado = streamText({
      model: openai('gpt-4o'),
      prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
    });

    resultado.pipeDataStreamToResponse(res);
  }
}
```

### Enviando Datos Personalizados

`pipeDataStreamToResponse` se puede utilizar para enviar datos personalizados al cliente.

```ts filename='app.controller.ts' highlight="10-12,19"
import { Controller, Post, Res } from '@nestjs/common';
import { openai } from '@ai-sdk/openai';
import { pipeDataStreamToResponse, streamText } from 'ai';
import { Response } from 'express';

@Controller()
export class AppController {
  @Post('/stream-data')
  async streamData(@Res() res: Response) {
    pipeDataStreamToResponse(res, {
      execute: async dataStreamWriter => {
        dataStreamWriter.writeData('llamada inicializada');

        const result = streamText({
          model: openai('gpt-4o'),
          prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
        });

        result.mergeIntoDataStream(dataStreamWriter);
      },
      onError: error => {
        // Los mensajes de error están ocultos por motivos de seguridad.
        // Si deseas exponer el mensaje de error al cliente, puedes hacerlo aquí:
        return error instanceof Error ? error.message : String(error);
      },
    });
  }
}
```

### Flujo de Texto

Puedes utilizar el método `pipeTextStreamToResponse` para obtener un flujo de texto del resultado y luego enviarlo a la respuesta.

```ts filename='app.controller.ts' highlight="15"
import { Controller, Post, Res } from '@nestjs/common';
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { Response } from 'express';

@Controller()
export class AppController {
  @Post()
  async ejemplo(@Res() res: Response) {
    const resultado = streamText({
      modelo: openai('gpt-4o'),
      prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
    });

    resultado.pipeTextStreamToResponse(res);
  }
}
```

## Solución de Problemas

- El streaming no funciona cuando se utiliza [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
title: SDK de IA por Vercel
description: El SDK de IA es la herramienta de TypeScript para construir aplicaciones y agentes de IA con React, Next.js, Vue, Svelte, Node.js, y más.
---

# SDK de IA

El SDK de IA es la herramienta de TypeScript diseñada para ayudar a los desarrolladores a construir aplicaciones y agentes de IA con React, Next.js, Vue, Svelte, Node.js, y más.

## ¿Por qué usar el SDK de IA?

Integrar modelos de lenguaje grande (LLM) en aplicaciones es complicado y depende mucho del proveedor de modelos específico que se utilice.

El SDK de IA estandariza la integración de modelos de inteligencia artificial (IA) a través de [proveedores admitidos](/docs/fundamentos/proveedores-y-modelos). Esto permite a los desarrolladores centrarse en crear aplicaciones de IA excelentes, en lugar de perder tiempo en detalles técnicos.

Por ejemplo, aquí está cómo se puede generar texto con varios modelos utilizando el SDK de IA:

<PreviewSwitchProviders />

El SDK de IA tiene dos bibliotecas principales:

- **[SDK de IA Core](/docs/sdk-de-ia-core):** Una API unificada para generar texto, objetos estructurados, llamadas a herramientas y construir agentes con LLM.
- **[SDK de IA UI](/docs/sdk-de-ia-ui):** Un conjunto de hooks inaceptables para frameworks para construir rápidamente interfaces de usuario de chat y generativas.

## Proveedores de Modelos

El SDK de IA admite [varios proveedores de modelos](/proveedores).

<OfficialModelCards />

## Plantillas

Hemos construido algunas [plantillas](https://vercel.com/templates?type=ai) que incluyen integraciones de SDK de IA para diferentes casos de uso, proveedores y frameworks. Puede utilizar estas plantillas para empezar con su aplicación con IA.

### Kits de inicio

<Templates type="starter-kits" />

### Exploración de características

<Templates type="feature-exploration" />

### Frameworks

<Templates type="frameworks" />

### UI Generativa

<Templates type="generative-ui" />

### Seguridad

<Templates type="security" />

## Únete a nuestra comunidad

Si tiene preguntas sobre cualquier cosa relacionada con el SDK de IA, siempre está bienvenido a preguntar a nuestra comunidad en [Discusiones de GitHub](https://github.com/vercel/ai/discussions).

## `llms.txt` (para Cursor, Windsurf, Copilot, Claude, etc.)

Puede acceder a la documentación completa del SDK de IA en formato Markdown en [ai-sdk.dev/llms.txt](/llms.txt). Esto se puede utilizar para preguntar a cualquier LLM (asumiendo que tiene una ventana de contexto lo suficientemente grande) sobre el SDK de IA con base en la documentación más actualizada.

### Ejemplo de Uso

Por ejemplo, para solicitar a un LLM preguntas sobre el SDK de AI:

1. Copie los contenidos de documentación desde [ai-sdk.dev/llms.txt](/llms.txt)
2. Utilice el siguiente formato de solicitud:

```prompt
Documentación:
{pasta documentación aquí}
---
Basado en la documentación anterior, responde a las siguientes preguntas:
{tu pregunta}
```

---
titulo: AI SDK 5 Alpha
descripcion: Comience a trabajar con la versión alfa del AI SDK 5.
---

# Anuncio del AI SDK 5 Alpha

<Nota tipo="advertencia">
  Esta es una vista previa temprana — el AI SDK 5 está en desarrollo activo. Las API pueden cambiar sin previo aviso. Pin a versiones específicas ya que pueden ocurrir cambios de ruptura incluso en versiones de parche. Para obtener más información, consulte los [docs de v5](https://v5.ai-sdk.dev)
</Nota>

## Orientación de la Versión Alfa

El AI SDK 5 Alfa está destinado a:

- Exploración y prototipos tempranos
- Proyectos de campo verde donde puede experimentar libremente
- Entornos de desarrollo donde puede tolerar cambios de ruptura

Esta versión alfa **no se recomienda** para:

- Aplicaciones de producción
- Proyectos que requieren APIs establecidas
- Aplicaciones existentes que necesitarían rutas de migración

Durante esta fase alfa, esperamos hacer cambios significativos y potencialmente de ruptura en la superficie de la API. Compartimos esto temprano para recopilar retroalimentación y mejorar el SDK antes de la estabilización. Su input es invaluable—por favor, comparta sus experiencias a través de problemas de GitHub o discusiones para ayudar a definir la versión final.

<Nota tipo="advertencia">
  Esperamos encontrar bugs en esta versión alfa. Para ayudarnos a mejorar el SDK, por favor [envíe informes de errores en GitHub](https://github.com/vercel/ai/issues/new/choose). Sus informes contribuyen directamente a hacer que la versión final sea más estable y confiable.
</Nota>

Para obtener más información, consulte los [docs de v5](https://v5.ai-sdk.dev).

## Instalación

Para instalar el AI SDK 5 - Alfa, ejecute el siguiente comando:

```bash
npm install @vercel/ai-sdk@alpha
```

# reemplaza con tu proveedor y framework
npm install ai@alpha @ai-sdk/[tu-proveedor]@alpha @ai-sdk/[tu-framework]@alpha

<Nota tipo="advertencia">
  Las APIs pueden cambiar sin previo aviso. Pinéal a versiones específicas ya que pueden ocurrir cambios de ruptura incluso en las versiones de parche.
</Nota>

## ¿Qué hay de nuevo en AI SDK 5?

AI SDK 5 es una completa redesign de la protocolo y la arquitectura de AI SDK basada en todo lo que hemos aprendido en los últimos dos años de uso en el mundo real. También hemos modernizado la interfaz de usuario y los protocolos que han permanecido en gran medida sin cambios desde AI SDK v2/3, creando una sólida base para el futuro.

### ¿Por qué AI SDK 5?

Cuando diseñamos originalmente el protocolo v1 hace más de un año, el patrón de interacción estándar con los modelos de lenguaje era simple: texto en, texto o llamada a herramienta fuera. Pero hoy en día, los LLMs van mucho más allá del texto y las llamadas a herramientas, generando razonamiento, fuentes, imágenes y más. Además, nuevos casos de uso como agentes de computadora introducen un enfoque fundamentalmente nuevo para interactuar con los modelos de lenguaje que hizo que fuera casi imposible apoyar en un enfoque unificado con nuestra arquitectura original.

Necesitábamos un protocolo diseñado para esta nueva realidad. Si bien esto es un cambio de ruptura que no tomamos a la ligera, ha proporcionado una oportunidad para reconstruir la base y agregar nuevas características poderosas.

Si bien hemos diseñado AI SDK 5 para ser una mejora sustancial sobre versiones anteriores, aún estamos en desarrollo activo. Es posible que encuentre bugs o comportamiento inesperado. Le agradeceríamos mucho que compartiera sus experiencias y sugerencias con nosotros a través de [issues de GitHub](https://github.com/vercel/ai/issues/new/choose) o [discusiones de GitHub](https://github.com/vercel/ai/discussions).

## Nuevas características

- [**LanguageModelV2**](#languagemodelv2) - nueva arquitectura rediseñada
- [**Message Overhaul**](#message-overhaul) - nuevos tipos `UIMessage` y `ModelMessage`
- [**ChatStore**](#chatstore) - nueva arquitectura `useChat`
- [**Server-Sent Events (SSE)**](

# Server-Sent Events (SSE) - nuevo protocolo estandarizado para enviar mensajes de interfaz a cliente
- [**Control Agente**](#control-agente) - nuevos primitivos para construir sistemas agentes

## LanguageModelV2

LanguageModelV2 representa un diseño completo de cómo el SDK de IA se comunica con modelos de lenguaje, adaptándose a los cada vez más complejos resultados que generan los sistemas de IA modernos. El nuevo LanguageModelV2 trata a todos los resultados de LLM como partes de contenido, lo que permite un manejo más consistente de texto, imágenes, razonamiento, fuentes y otros tipos de respuesta. Ahora cuenta con:

- **Diseño Primero del Contenido** - En lugar de separar texto, razonamiento y llamadas a herramientas, todo se representa ahora como partes de contenido ordenadas en un array unificado
- **Seguridad de Tipo Mejorada** - El nuevo LanguageModelV2 proporciona garantías de seguridad de tipo de TypeScript mejoradas, lo que facilita trabajar con diferentes tipos de contenido
- **Extensibilidad Simplificada** - Agregar soporte a nuevas capacidades de modelos ya no requiere cambios en la estructura básica

## Reformulación de Mensajes

La SDK de AI 5 introduce un sistema de mensajes completamente rediseñado con dos tipos de mensajes que abordan las necesidades dual de lo que renderizas en tu interfaz y lo que envías al modelo. El contexto es crucial para la generación efectiva de modelos de lenguaje, y estos dos tipos de mensajes cumplen fines distintos:

- **UIMensaje** representa la historia de conversación completa para tu interfaz, preservando todos los partes del mensaje (texto, imágenes, datos), metadatos (fechas de creación, tiempos de generación) y estado de la interfaz—sin importar la longitud.

- **ModeloMensaje** está optimizado para enviar a los modelos de lenguaje, considerando las restricciones de entrada de tokens. Elimina los metadatos específicos de la interfaz y contenido irrelevante.

Con este cambio, deberás convertir explícitamente tus `UIMensajes` a `ModeloMensajes` antes de enviarlos al modelo.

```ts highlight="9"
import { openai } from '@ai-sdk/openai';
import { convertToModelMessages, streamText, UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

<Nota>
Esta separación es esencial ya que no puedes utilizar un formato de mensaje único para ambos fines. El estado que guardes siempre debe ser el formato de `UIMensaje` para evitar la pérdida de información, con una conversión explícita a `ModeloMensaje` cuando se comunica con modelos de lenguaje.
</Nota>

El nuevo sistema de mensajes ha hecho posible varias características altamente solicitadas:

- **Metadatos de Mensajes Seguros de Tipo** - agrega información estructurada por mensaje
- **Nuevo Escritor de Flujo** - fluye cualquier parte tipo (razonamiento, fuentes, etc.) manteniendo el orden adecuado
- **Partes de Datos** - fluye partes de datos seguras de tipo para componentes de interfaz dinámicos

### Metadatos de mensaje

Los metadatos permiten adjuntar información estructurada a mensajes individuales, lo que facilita rastrear detalles importantes como el tiempo de respuesta, el uso de tokens o las especificaciones del modelo. Esta información puede mejorar la interfaz de usuario con datos contextuales sin incorporarlos en el contenido del mensaje mismo.

Para agregar metadatos a un mensaje, primero define el esquema de metadatos:

```ts filename="app/api/chat/ejemplo-esquema-de-metadatos.ts"
export const ejemploEsquemaDeMetadatos = z.object({
  duración: z.number().opcional(),
  modelo: z.string().opcional(),
  tokensTotales: z.number().opcional(),
});

export type EjemploDeMetadatos = z.infer<typeof ejemploEsquemaDeMetadatos>;
```

Luego agrega los metadatos utilizando la propiedad `message.metadata` en la utilidad `toUIMessageStreamResponse()`:

```ts filename="app/api/chat/ruta.ts"
import { openai } from '@ai-sdk/openai';
import { convertToModelMessages, streamText, UIMessage } from 'ai';
import { EjemploDeMetadatos } from './ejemplo-esquema-de-metadatos';

export async function POST(req: Request) {
  const { mensajes }: { mensajes: UIMessage[] } = await req.json();

  const startTime = Date.now();
  const resultado = streamText({
    modelo: openai('gpt-4o'),
    prompt: convertToModelMessages(mensajes),
  });

  return resultado.toUIMessageStreamResponse({
    messageMetadata: ({ parte }): EjemploDeMetadatos | undefined => {
      // envía información personalizada al cliente en el inicio:
      if (parte.tipo === 'inicio') {
        return {
          modelo: 'gpt-4o', // id del modelo inicial
        };
      }
```

// enviar información adicional del modelo en el paso de finalización:
      if (part.type === 'finish-step') {
        return {
          modelo: part.response.modelId, // actualizar con el id del modelo real
          duración: Date.now() - startTime,
        };
      }

      // cuando el mensaje está finalizado, enviar información adicional:
      if (part.type === 'finish') {
        return {
          tokensTotales: part.totalUsage.totalTokens,
        };
      }
    },
  });
}
```

Finalmente, especifique el esquema de metadatos del mensaje en el cliente y luego renderice (de forma segura) los metadatos en su interfaz de usuario:

```tsx filename="app/page.tsx"
import { zodSchema } from '@ai-sdk/provider-utils';
import { useChat } from '@ai-sdk/react';
import { defaultChatStore } from 'ai';
import { exampleMetadataSchema } from '@/api/chat/example-metadata-schema';

export default function Chat() {
  const { messages } = useChat({
    chatStore: defaultChatStore({
      api: '/api/use-chat',
      messageMetadataSchema: zodSchema(exampleMetadataSchema),
    }),
  });
```

```markdown
return (
  <div>
    {messages.map(message => {
      const { metadata } = message;
      return (
        <div key={message.id} className="whitespace-pre-wrap">
          {metadata?.duration && <div>Duración: {metadata.duration}ms</div>}
          {metadata?.model && <div>Modelo: {metadata.model}</div>}
          {metadata?.totalTokens && (
            <div>Token total: {metadata.totalTokens}</div>
          )}
        </div>
      );
    })}
  </div>
);


### Flujo de Mensajes de la Interfaz de Usuario

El Flujo de Mensajes de la Interfaz de Usuario permite transmitir cualquier parte del contenido desde el servidor al cliente. Con este flujo, puede enviar datos estructurados como fuentes personalizadas de su pipeline RAG directamente a su interfaz de usuario. El escritor de flujo es simplemente una utilidad que facilita escribir en este flujo de mensajes.

```ts
const stream = createUIMessageStream({
  execute: writer => {
    // transmitir fuentes personalizadas
    writer.write({
      type: 'fuente',
      value: {
        type: 'fuente',
        sourceType: 'url',
        id: 'fuente-1',
        url: 'https://example.com',
        title: 'Fuente de Ejemplo',
      },
    });
  },
});
```

En el cliente, estos se agregarán a la matriz ordenada `message.parts`.

### Partes de datos

El nuevo escritor de flujo también permite una forma segura de flujo de datos arbitrarios desde el servidor al cliente y mostrarlos en su interfaz de usuario.

Puedes crear y fluir partes de datos personalizadas en el servidor:

```tsx
// En el servidor
const stream = createUIMessageStream({
  execute: writer => {
    // Actualización inicial
    writer.write({
      type: 'data-weather', // Tipo personalizado
      id: toolCallId, // ID para actualizaciones
      data: { city, status: 'loading' }, // Sus datos
    });

    // Más tarde, actualiza la misma parte
    writer.write({
      type: 'data-weather',
      id: toolCallId,
      data: { city, weather, status: 'success' },
    });
  },
});
```

En el cliente, puedes renderizar estas partes con seguridad de tipo:

```tsx
{
  message.parts
    .filter(part => part.type === 'data-weather') // seguridad de tipo
    .map((part, index) => (
      <Weather
        key={index}
        city={part.data.city} // seguridad de tipo
        weather={part.data.weather} // seguridad de tipo
        status={part.data.status} // seguridad de tipo
      />
    ));
}
```

Las partes de datos aparecen en el array `message.parts` junto con otros contenidos, manteniendo el orden correcto de la conversación. Puedes actualizar partes haciendo referencia al mismo ID, lo que permite experiencias dinámicas como artefactos colaborativos.

## ChatStore

SDK AI 5 introduce una nueva arquitectura `useChat` con componentes ChatStore y ChatTransport. Estos dos bloques de construcción fundamentales hacen que la gestión de estado y la integración de API sean más flexibles, permitiendo componer ataduras de interfaz de usuario reactivas, compartir estado de chat entre múltiples instancias y cambiar el protocolo de servidor sin volver a escribir la lógica de la aplicación.

El `ChatStore` es responsable de:

- **Gestionar múltiples chats** – acceder y cambiar entre conversaciones de manera fluida.
- **Procesar streams de respuesta** – manejar streams del servidor y sincronizar estado (por ejemplo, cuando hay resultados de herramientas del lado del cliente concurrentes).
- **Cachear y sincronizar** – compartir estado (mensajes, estado, errores) entre hooks `useChat`.

Puedes crear un ChatStore básico con la función de ayuda:

```ts
import { defaultChatStore } from 'ai';

const chatStore = defaultChatStore({
  api: '/api/chat', // tu punto de conexión de chat
  maxSteps: 5, // opcional: limitar llamadas LLM en cadenas de herramientas
  chats: {}, // opcional: cargar sesiones de chat previas
});

import { useChat } from '@ai-sdk/react';
const { messages, input, handleSubmit } = useChat({ chatStore });
```

## Eventos Servidor-Sent (SSE)

SDK AI 5 utiliza ahora Eventos Servidor-Sent (SSE) en lugar de un protocolo de streaming personalizado. SSE es un estándar web común para enviar datos desde servidores a navegadores. Esta modificación tiene varias ventajas:

- **Funciona en todos lados** - Utiliza tecnología que funciona en todos los navegadores y plataformas importantes
- **Más fácil de depurar** - Puedes ver el flujo de datos en herramientas de desarrollador de navegador
- **Más fácil de agregar características** - Agregar nuevas características es más directo
- **Más estable** - Construido sobre tecnología probada que muchos desarrolladores ya utilizan

## Control Agente

SDK AI 5 introduce nuevas características para construir agentes que te permiten controlar el comportamiento del modelo de manera más precisa.

### prepareStep

La función `prepareStep` te da un control fino sobre cada paso en un agente de varios pasos. Se llama antes de que comience un paso y te permite:

- Cambiar dinámicamente el modelo utilizado para pasos específicos
- Forzar selecciones de herramientas específicas para pasos particulares
- Limitar las herramientas disponibles durante pasos específicos
- Examinar el contexto de los pasos anteriores antes de proceder

```ts
const resultado = await generarTexto({
  // ...
  experimental_prepareStep: async ({ modelo, pasoNumero, maxPaso, pasos }) => {
    if (pasoNumero === 0) {
      return {
        // utilice un modelo diferente para este paso:
        modelo: modeloParaEstePasoEnParticular,
        // fuerza una elección de herramienta para este paso:
        eleccionHerramienta: { tipo: 'herramienta', nombreHerramienta: 'herramienta1' },
        // limite las herramientas que están disponibles para este paso:
        experimental_herramientasActivas: ['herramienta1'],
      };
    }
    // cuando no se devuelve nada, se utilizan los ajustes por defecto
  },
});
```

Esto facilita la construcción de sistemas de inteligencia artificial que adapten sus capacidades en función del contexto actual y de las requisitos de la tarea.

### `stopWhen`

El parámetro `stopWhen` te permite definir condiciones de parada para tu agente. En lugar de ejecutarse de manera indefinida, puedes especificar exactamente cuándo el agente debería terminar en función de diversas condiciones:

- Al alcanzar un número máximo de pasos
- Al llamar a una herramienta específica
- Al satisfacer cualquier condición personalizada que definas

```ts
const resultado = generarTexto({
  // ...
  // detener el bucle en 5 pasos
  stopWhen: stepCountIs(5),
});

const resultado = generarTexto({
  // ...
  // detener el bucle cuando se llame a la herramienta de clima
  stopWhen: hasToolCall('weather'),
});

const resultado = generarTexto({
  // ...
  // detener el bucle en tu propia condición personalizada
  stopWhen: maxTotalTokens(20000),
});
```

Estos controles agénicos forman la base para construir sistemas de inteligencia artificial más confiables, controlables y que puedan abordar problemas complejos mientras se mantienen dentro de restricciones bien definidas.

---
titulo: Resumen
descripcion: Un resumen de AI SDK Core.
---

# AI SDK Core

Los Modelos de Lenguaje de Gran Escala (LLMs) son programas avanzados que pueden entender, crear y interactuar con el lenguaje humano a gran escala.
Están entrenados en vastas cantidades de material escrito para reconocer patrones en el lenguaje y predecir qué podría venir a continuación en un trozo de texto dado.

AI SDK Core **simplifica trabajar con LLMs ofreciendo una forma estandarizada de integrarlos en tu aplicación** - así que puedes enfocarte en construir aplicaciones de inteligencia artificial geniales para tus usuarios, no desperdiciar tiempo en detalles técnicos.

Por ejemplo, aquí está cómo puedes generar texto con varios modelos utilizando la AI SDK:

<PreviewSwitchProviders />

## Funciones de Núcleo del SDK de IA

El Núcleo del SDK de IA cuenta con varias funciones diseñadas para [generación de texto](./generación-de-texto), [generación de datos estructurados](./generación-de-datos-estructurados) y [uso de herramientas](./herramientas-y-llamadas-a-herramientas).
Estas funciones siguen un enfoque estandarizado para configurar [solicitudes](./solicitudes) y [configuraciones](./configuraciones), lo que facilita trabajar con diferentes modelos.

- [`generateText`](/docs/ai-sdk-core/generación-de-texto): Genera texto y [llamadas a herramientas](./herramientas-y-llamadas-a-herramientas).
  Esta función es ideal para casos de uso no interactivos como tareas de automatización donde se necesita escribir texto (por ejemplo, redactar correos electrónicos o resumir páginas web) y para agentes que utilizan herramientas.
- [`streamText`](/docs/ai-sdk-core/generación-de-texto): Transmite texto y llamadas a herramientas.
  Puedes utilizar la función `streamText` para casos de uso interactivos como [chatbots](/docs/ai-sdk-ui/chatbot) y [transmisión de contenido](/docs/ai-sdk-ui/completación).
- [`generateObject`](/docs/ai-sdk-core/generación-de-datos-estructurados): Genera un objeto estructurado y tipado que coincide con un [esquema de Zod](https://zod.dev/).
  Puedes utilizar esta función para obligar al modelo de lenguaje a devolver datos estructurados, por ejemplo, para la extracción de información, la generación de datos sintéticos o las tareas de clasificación.
- [`streamObject`](/docs/ai-sdk-core/generación-de-datos-estructurados): Transmite un objeto estructurado que coincide con un esquema de Zod.
  Puedes utilizar esta función para [transmitir UIs generadas](/docs/ai-sdk-ui/generación-de-objetos).

## Referencia de API

Por favor, consulta la [Referencia de API del Núcleo del SDK de IA](/docs/reference/ai-sdk-core) para obtener más detalles sobre cada función.

---
title: Generación de Texto
description: Aprende a generar texto con el SDK de IA.
---

# Generando y Transmitiendo Texto

Los modelos de lenguaje grande (LLM) pueden generar texto en respuesta a una solicitud, que puede contener instrucciones e información para procesar.
Por ejemplo, puedes pedirle a un modelo que cree una receta, redacte un correo electrónico o resuma un documento.

La biblioteca de SDK de IA Core proporciona dos funciones para generar texto y transmitirlo desde LLMs:

- [`generateText`](#generatetext): Genera texto para una solicitud dada y modelo.
- [`streamText`](#streamtext): Transmite texto desde una solicitud dada y modelo.

Características avanzadas de LLM como [llamadas a herramientas](./herramientas-y-llamadas-a-herramientas) y [generación de datos estructurados](./generación-de-datos-estructurados) se construyen sobre la generación de texto.

## `generarTexto`

Puedes generar texto utilizando la función `generarTexto` ([/docs/reference/ai-sdk-core/generar-texto](/docs/reference/ai-sdk-core/generar-texto)). Esta función es ideal para casos de uso no interactivos donde necesitas escribir texto (por ejemplo, redactar correos electrónicos o resumir páginas web) y para agentes que utilizan herramientas.

```tsx
import { generarTexto } from 'ai';

const { texto } = await generarTexto({
  modelo: tuModelo,
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Puedes utilizar [prompts más avanzados](./prompts) para generar texto con instrucciones y contenido más complejos:

```tsx
import { generarTexto } from 'ai';

const { texto } = await generarTexto({
  modelo: tuModelo,
  sistema:
    'Eres un escritor profesional. ' +
    'Escribes contenido sencillo, claro y conciso.',
  prompt: `Resumen del siguiente artículo en 3-5 oraciones: ${articulo}`,
});
```

El objeto de resultados de `generarTexto` contiene varias promesas que se resuelven cuando todos los datos requeridos están disponibles:

- `result.texto`: El texto generado.
- `result.razonamiento`: El texto de razonamiento del modelo (solo disponible para algunos modelos).
- `result.fuentes`: Fuentes que se han utilizado como entrada para generar la respuesta (solo disponible para algunos modelos).
- `result.finishReason`: La razón por la que el modelo terminó generando texto.
- `result.uso`: El uso del modelo durante la generación de texto.

### Acceder a encabezados y cuerpo de respuesta

A veces necesitas acceder al encabezado y cuerpo completos de la respuesta del proveedor del modelo,
por ejemplo, para acceder a algunos encabezados o contenido de cuerpo específicos del proveedor.

Puedes acceder a los encabezados y cuerpo de respuesta bruto utilizando la propiedad `response`:

```ts
import { generarTexto } from 'ai';

const resultado = await generarTexto({
  // ...
});

console.log(JSON.stringify(resultado.response.encabezados, null, 2));
console.log(JSON.stringify(resultado.response.cuerpo, null, 2));
```

## `streamText`

Dependiendo de tu modelo y solicitud, puede que un modelo de lenguaje grande (LLM) tarde hasta un minuto en completar la generación de su respuesta. Esta demora puede ser inaceptable para casos de uso interactivos como chatbots o aplicaciones en tiempo real, donde los usuarios esperan respuestas inmediatas.

El SDK de AI Core proporciona la función [`streamText`](/docs/reference/ai-sdk-core/stream-text) que simplifica la transmisión de texto de los LLMs:

```ts
import { streamText } from 'ai';

const result = streamText({
  model: tuModelo,
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
});

// ejemplo: usa textStream como un iterable asíncrono
for await (const textoParte of result.textStream) {
  console.log(textoParte);
}
```

<Nota>
  `result.textStream` es tanto un `ReadableStream` como un `AsyncIterable`.
</Nota>

<Nota tipo="advertencia">
  `streamText` comienza a transmitir inmediatamente y suprime errores para prevenir
  caídas del servidor. Utiliza el callback `onError` para registrar errores.
</Nota>

Puedes usar `streamText` por separado o en combinación con [AI SDK
UI](/examples/next-pages/basics/streaming-text-generation) y [AI SDK
RSC](/examples/next-app/basics/streaming-text-generation).

El objeto de resultado contiene varias funciones de ayuda para hacer que la integración en [AI SDK UI](/docs/ai-sdk-ui) sea más fácil:

- `result.toDataStreamResponse()`: Crea una respuesta de flujo de datos HTTP (con llamadas a herramientas, etc.) que se puede utilizar en una ruta de API de App Router de Next.js.
- `result.pipeDataStreamToResponse()`: Escribe la salida delta de flujo de datos en un objeto de respuesta como Node.js.
- `result.toTextStreamResponse()`: Crea una respuesta de flujo de texto HTTP simple.
- `result.pipeTextStreamToResponse()`: Escribe la salida delta de texto en un objeto de respuesta como Node.js.

<Nota>
  `streamText` utiliza backpressure y solo genera tokens a medida que se solicitan. Necesitas consumir el flujo para que termine.
</Nota>

También proporciona varias promesas que se resuelven cuando el flujo se ha terminado:

- `result.text`: El texto generado.
- `result.reasoning`: El texto de razonamiento del modelo (solo disponible para algunos modelos).
- `result.sources`: Las fuentes que se han utilizado como entrada para generar la respuesta (solo disponible para algunos modelos).
- `result.finishReason`: La razón por la que el modelo terminó de generar texto.
- `result.usage`: El uso del modelo durante la generación de texto.

### `onError` callback

`streamText` inmediatamente comienza a transmitir para habilitar la envío de datos sin esperar al modelo.
Los errores se convierten en parte de la transmisión y no se lanzan para evitar que los servidores se caigan.

Para registrar errores, puede proporcionar un callback `onError` que se activa cuando ocurre un error.

```tsx highlight="6-8"
import { streamText } from 'ai';

const resultado = streamText({
  modelo: tuModelo,
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  onError({ error }) {
    console.error(error); // tu lógica de registro de errores aquí
  },
});
```

### `onChunk` callback

Cuando se utiliza `streamText`, puede proporcionar un callback `onChunk` que se activa para cada trozo de la transmisión.

Recibe los siguientes tipos de trozos:

- `text-delta`
- `razonamiento`
- `fuente`
- `llamada-a-herramienta`
- `resultado-de-herramienta`
- `llamada-a-herramienta-streaming-start` (cuando `toolCallStreaming` está habilitado)
- `llamada-a-herramienta-delta` (cuando `toolCallStreaming` está habilitado)

```tsx highlight="6-11"
import { streamText } from 'ai';

const resultado = streamText({
  modelo: tuModelo,
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  onChunk({ chunk }) {
    // implementa tu propia lógica aquí, por ejemplo:
    if (chunk.type === 'text-delta') {
      console.log(chunk.text);
    }
  },
});
```

### `onFinish` callback

Cuando se utiliza `streamText`, puede proporcionar un callback `onFinish` que se activa cuando la transmisión está lista (
[Referencia de la API](/docs/reference/ai-sdk-core/stream-text)

# on-finish)
.
Contiene el texto, información de uso, razón de finalización, mensajes y más:

```tsx highlight="6-8"
import { streamText } from 'ai';

const result = streamText({
  model: tuModelo,
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  onFinish({ text, finishReason, usage, response }) {
    // tu propia lógica, por ejemplo, para guardar la historia de chat o registrar el uso

    const mensajes = response.messages; // mensajes que se generaron
  },
});
```

### Propiedad `fullStream`

Puedes leer un flujo con todos los eventos utilizando la propiedad `fullStream`.
Esto puede ser útil si deseas implementar tu propia interfaz o manejar el flujo de manera diferente.
Aquí hay un ejemplo de cómo utilizar la propiedad `fullStream`:

```tsx
import { streamText } from 'ai';
import { z } from 'zod';

const result = streamText({
  model: tuModelo,
  tools: {
    cityAttractions: {
      parameters: z.object({ ciudad: z.string() }),
      execute: async ({ ciudad }) => ({
        atractivos: ['atracción1', 'atracción2', 'atracción3'],
      }),
    },
  },
  prompt: '¿Cuáles son algunos atractivos turísticos de San Francisco?',
});
```

```markdown
# Manejo de Resultados Asincrónicos

```javascript
for await (const part of result.fullStream) {
  switch (part.type) {
    case 'text-delta': {
      // Manejar delta de texto aquí
      break;
    }
    case 'razonamiento': {
      // Manejar razonamiento aquí
      break;
    }
    case 'fuente': {
      // Manejar fuente aquí
      break;
    }
    case 'llamada-a-herramienta': {
      switch (part.toolName) {
        case 'atracciones-de-la-ciudad': {
          // Manejar llamada a herramienta aquí
          break;
        }
      }
      break;
    }
    case 'resultado-de-herramienta': {
      switch (part.toolName) {
        case 'atracciones-de-la-ciudad': {
          // Manejar resultado de herramienta aquí
          break;
        }
      }
      break;
    }
    case 'finalizar': {
      // Manejar finalización aquí
      break;
    }
    case 'error': {
      // Manejar error aquí
      break;
    }
  }
}
```

### Transformación de flujo

Puedes utilizar la opción `experimental_transform` para transformar el flujo.
Esto es útil, por ejemplo, para filtrar, cambiar o suavizar el flujo de texto.

Las transformaciones se aplican antes de que se invoquen los callbacks y se resuelvan las promesas.
Si, por ejemplo, tienes una transformación que cambia todo el texto a mayúsculas, el callback `onFinish` recibirá el texto transformado.

#### Suavizar flujos

El Core de SDK de Inteligencia Artificial proporciona una función [`smoothStream`](/docs/reference/ai-sdk-core/smooth-stream) que
puedes utilizar para suavizar el flujo de texto.

```tsx highlight="6"
import { smoothStream, streamText } from 'ai';

const result = streamText({
  model,
  prompt,
  experimental_transform: smoothStream(),
});
```

#### Transformaciones personalizadas

También puedes implementar tus propias transformaciones personalizadas.
La función de transformación recibe las herramientas disponibles para el modelo,
y devuelve una función que se utiliza para transformar el flujo.
Las herramientas pueden ser genéricas o limitadas a las herramientas que estás utilizando.

Aquí está un ejemplo de cómo implementar una transformación personalizada que convierte
todo el texto a mayúsculas:

```ts
const upperCaseTransform =
  <TOOLS extends ToolSet>() =>
  (options: { tools: TOOLS; stopStream: () => void }) =>
    new TransformStream<TextStreamPart<TOOLS>, TextStreamPart<TOOLS>>({
      transform(chunk, controller) {
        controller.enqueue(
          // para chunks de texto-delta, convierte el texto a mayúsculas:
          chunk.type === 'text-delta'
            ? { ...chunk, textDelta: chunk.textDelta.toUpperCase() }
            : chunk,
        );
      },
    });
```

También puedes detener el flujo utilizando la función `stopStream`.
Esto es útil, por ejemplo, si deseas detener el flujo cuando se violan las barreras de seguridad del modelo, por ejemplo, generando contenido inapropiado.

Cuando invoques `stopStream`, es importante simular los eventos `step-finish` y `finish` para garantizar que se devuelve un flujo bien formado
y se invocan todos los callbacks.

```ts
const transformaPalabraStop =
  <CONJUNTOS extends ConjuntoDeHerramientas>() =>
  ({ stopStream }: { stopStream: () => void }) =>
    new TransformStream<ParteDelFlujoDeTexto<TOOLS>, ParteDelFlujoDeTexto<TOOLS>>({
      // nota: esta es una transformación simplificada para pruebas;
      // en una versión real-world habría que tener en cuenta
      // la bufferización y el escaneo del flujo para emitir texto previo
      // y para detectar todas las ocurrencias de STOP.
      transform(chunk, controller) {
        if (chunk.tipo !== 'delta-de-texto') {
          controller.enqueue(chunk);
          return;
        }

        if (chunk.deltaDeTexto.includes('STOP')) {
          // detiene el flujo
          stopStream();
```

Nota: He utilizado el término "ConjuntoDeHerramientas" para traducir "ToolSet" y "ParteDelFlujoDeTexto" para traducir

// simular el evento step-finish
          controller.enqueue({
            tipo: 'step-finish',
            razónDeFinalización: 'stop',
            logprobs: undefined,
            uso: {
              tokensDeCompletación: NaN,
              tokensDePrompt: NaN,
              tokensTotales: NaN,
            },
            solicitud: {},
            respuesta: {
              id: 'response-id',
              modeloId: 'mock-model-id',
              timestamp: new Date(0),
            },
            advertencias: [],
            esContinuado: false,


// simular el evento de finalización
          controller.enqueue({
            tipo: 'finish',
            razónDeFinalización: 'stop',
            logprobs: undefined,
            uso: {
              tokensDeCompletación: NaN,
              tokensDeSolicitud: NaN,
              tokensTotales: NaN,
            },
            respuesta: {
              id: 'response-id',
              modeloId: 'mock-model-id',
              timestamp: new Date(0),
            },
          });

          return;
        }

        controller.enqueue(chunk);
      },
    });

#### Multiple Transformaciones

También puedes proporcionar múltiples transformaciones. Se aplican en el orden en que se proporcionan.

```tsx highlight="4"
const result = streamText({
  model,
  prompt,
  experimental_transform: [firstTransform, secondTransform],
});
```

## Fuentes

Algunos proveedores como [Perplexity](/providers/ai-sdk-providers/perplexity#fuentes) y
[Google Generative AI](/providers/ai-sdk-providers/google-generative-ai)

# fuentes) incluir fuentes en la respuesta.

Actualmente, las fuentes están limitadas a páginas web que respaldan la respuesta.
Puedes acceder a ellas utilizando la propiedad `sources` del resultado.

Cada fuente `url` contiene las siguientes propiedades:

- `id`: El ID de la fuente.
- `url`: La URL de la fuente.
- `title`: El título opcional de la fuente.
- `providerMetadata`: Metadatos del proveedor de la fuente.

Cuando utilices `generateText`, puedes acceder a las fuentes utilizando la propiedad `sources`:

```ts
const result = await generateText({
  model: google('gemini-2.0-flash-exp', { useSearchGrounding: true }),
  prompt: 'List the top 5 San Francisco news from the past week.',
});

for (const source of result.sources) {
  if (source.sourceType === 'url') {
    console.log('ID:', source.id);
    console.log('Título:', source.title);
    console.log('URL:', source.url);
    console.log('Metadatos del proveedor:', source.providerMetadata);
    console.log();
  }
}
```

Cuando utilices `streamText`, puedes acceder a las fuentes utilizando la propiedad `fullStream`:

```tsx
const result = streamText({
  model: google('gemini-2.0-flash-exp', { useSearchGrounding: true }),
  prompt: 'List the top 5 San Francisco news from the past week.',
});

for await (const part of result.fullStream) {
  if (part.type === 'source' && part.source.sourceType === 'url') {
    console.log('ID:', part.source.id);
    console.log('Título:', part.source.title);
    console.log('URL:', part.source.url);
    console.log('Metadatos del proveedor:', part.source.providerMetadata);
    console.log();
  }
}
```

Las fuentes también están disponibles en la promesa `result.sources`.

## Generación de Texto Largo

La mayoría de los modelos de lenguaje tienen un límite de salida mucho más corto que su ventana de contexto.
Esto significa que no puedes generar texto largo de una sola vez,
pero es posible agregar respuestas al input y continuar generando
para crear texto más largo.

`generateText` y `streamText` admiten tales continuaciones para la generación de texto largo utilizando la configuración experimental `continueSteps`:

```tsx highlight="5-6,9-10"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const {
  text, // texto combinado
  usage, // uso combinado de todos los pasos
} = await generateText({
  model: openai('gpt-4o'), // 4096 tokens de salida
  maxSteps: 5, // habilitar llamadas de varios pasos
  experimental_continueSteps: true,
  prompt:
    'Escribe un libro sobre la historia de Roma, ' +
    'desde la fundación de la ciudad de Roma ' +
    'hasta la caída del Imperio Romano Occidental. ' +
    'Cada capítulo DEBE TENER al menos 1000 palabras.',
});
```

<Nota>
  Cuando `experimental_continueSteps` está habilitado, solo se transmiten palabras completas en `streamText`, y tanto `generateText` como `streamText` pueden eliminar los tokens finales de algunas llamadas para prevenir problemas de espacios en blanco.
</Nota>

<Nota tipo="advertencia">
  Algunos modelos no paran correctamente por sí mismos y siguen generando
  hasta que se alcanza `maxSteps`. Puedes sugerirle al modelo que pare usando un mensaje de sistema como "Pare cuando se haya proporcionado suficiente información."
</Nota>

## Ejemplos

Puedes ver `generateText` y `streamText` en acción utilizando diversas frameworks en los siguientes ejemplos:

### `generateText`

<ExampleLinks
  examples={[
    {
      title: 'Aprende a generar texto en Node.js',
      link: '/examples/node/generating-text/generate-text',
    },
    {
      title:
        'Aprende a generar texto en Next.js con Manejadores de Rutas (SDK de IA UI)',
      link: '/examples/next-pages/basics/generating-text',
    },
    {
      title:
        'Aprende a generar texto en Next.js con Acciones de Servidor (SDK de IA RSC)',
      link: '/examples/next-app/basics/generating-text',
    },
  ]}
/>

### `streamText`

<ExampleLinks
  examples={[
    {
      title: 'Aprende a generar texto en flujo en Node.js',
      link: '/examples/node/generating-text/stream-text',
    },
    {
      title: 'Aprende a generar texto en flujo en Next.js con Manejadores de Rutas (SDK de IA UI)',
      link: '/examples/next-pages/basics/streaming-text-generation',
    },
    {
      title: 'Aprende a generar texto en flujo en Next.js con Acciones de Servidor (SDK de IA RSC)',
      link: '/examples/next-app/basics/streaming-text-generation',
    },
  ]}
/>

---
title: Generación de datos estructurados
description: Aprende a generar datos estructurados con el SDK de IA.
---

# Generando Datos Estructurados

Mientras que la generación de texto puede ser útil, es probable que su caso de uso requiera generar datos estructurados.
Por ejemplo, podría querer extraer información de texto, clasificar datos o generar datos sintéticos.

Muchos modelos de lenguaje son capaces de generar datos estructurados, a menudo definidos como utilizando "modos JSON" o "herramientas".
Sin embargo, necesita proporcionar esquemas manualmente y luego validar los datos generados, ya que los LLM pueden producir datos estructurados incorrectos o incompletos.

La SDK de Inteligencia Artificial estandariza la generación de objetos estructurados a través de proveedores de modelos
con las funciones [`generateObject`](/docs/reference/ai-sdk-core/generate-object) y [`streamObject`](/docs/reference/ai-sdk-core/stream-object).
Puede utilizar ambas funciones con diferentes estrategias de salida, por ejemplo `array`, `object`, o `no-schema`,
y con diferentes modos de generación, por ejemplo `auto`, `tool`, o `json`.
Puede utilizar [esquemas Zod](/docs/reference/ai-sdk-core/zod-schema), [Valibot](/docs/reference/ai-sdk-core/valibot-schema) o [esquemas JSON](/docs/reference/ai-sdk-core/json-schema) para especificar la forma de los datos que desea,
y el modelo de inteligencia artificial generará datos que se ajusten a esa estructura.

<Nota>
  Puede pasar objetos Zod directamente a las funciones de la SDK de Inteligencia Artificial o utilizar la función de ayuda `zodSchema`.
</Nota>

## Generar Objeto

El `generateObject` genera datos estructurados a partir de una solicitud.
El esquema también se utiliza para validar los datos generados, asegurando la seguridad de tipo y la corrección.

```ts
import { generateObject } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: tuModelo,
  schema: z.object({
    receta: z.object({
      nombre: z.string(),
      ingredientes: z.array(z.object({ nombre: z.string(), cantidad: z.string() })),
      pasos: z.array(z.string()),
    }),
  }),
  prompt: 'Genera una receta de lasaña.',
});
```

<Nota>
  Consulta `generateObject` en acción con [estos ejemplos](#más-ejemplos)
</Nota>

### Accediendo a encabezados y cuerpo de la respuesta

A veces necesitas acceso al respuesta completa del proveedor de modelos,
p. ej. para acceder a algunos encabezados o contenido de cuerpo específicos del proveedor.

Puedes acceder a los encabezados y cuerpo de la respuesta bruta utilizando la propiedad `response`:

```ts
import { generateText } from 'ai';

const resultado = await generateText({
  // ...
});

console.log(JSON.stringify(resultado.response.headers, null, 2));
console.log(JSON.stringify(resultado.response.body, null, 2));
```

## Objeto de Flujo

Dado la complejidad añadida de devolver datos estructurados, el tiempo de respuesta del modelo puede ser inaceptable para tu caso de uso interactivo.
Con la función [`streamObject`](/docs/reference/ai-sdk-core/stream-object) puedes hacer fluir la respuesta del modelo a medida que se genera.

```ts
import { streamObject } from 'ai';

const { partialObjectStream } = streamObject({
  // ...
});

// usa partialObjectStream como un iterable asíncrono
for await (const partialObject of partialObjectStream) {
  console.log(partialObject);
}
```

Puedes usar `streamObject` para hacer fluir interfaces generadas en combinación con React Server Components (ver [Generative UI](../ai-sdk-rsc))) o el hook [`useObject`](/docs/reference/ai-sdk-ui/use-object).

<Nota>Ver `streamObject` en acción con [estos ejemplos](#more-examples)</Nota>

### Callback `onError`

`streamObject` inicia inmediatamente la transmisión.
Los errores se convierten en parte del flujo y no se lanzan para evitar que los servidores se caigan.

Para registrar errores, puedes proporcionar un callback `onError` que se desencadena cuando ocurre un error.

```tsx highlight="5-7"
import { streamObject } from 'ai';

const result = streamObject({
  // ...
  onError({ error }) {
    console.error(error); // tu lógica de registro de errores aquí
  },
});
```

## Estrategia de Salida

Puedes usar ambas funciones con diferentes estrategias de salida, por ejemplo `array`, `object` o `no-schema`.

### Objeto

La estrategia de salida por defecto es `object`, que devuelve los datos generados como un objeto.
No necesitas especificar la estrategia de salida si deseas usar la predeterminada.

### Array

Si deseas generar un arreglo de objetos, puedes configurar la estrategia de salida a `array`.
Cuando usas la estrategia de salida `array`, el esquema especifica la forma de un elemento del arreglo.
Con `streamObject`, también puedes enviar en streaming los elementos del arreglo generado usando `elementStream`.

```ts highlight="7,18"
import { openai } from '@ai-sdk/openai';
import { streamObject } from 'ai';
import { z } from 'zod';

const { elementStream } = streamObject({
  model: openai('gpt-4-turbo'),
  output: 'array',
  schema: z.object({
    name: z.string(),
    class: z
      .string()
      .describe('Clase de personaje, por ejemplo guerrero, mago o ladrón.'),
    description: z.string(),
  }),
  prompt: 'Genera 3 descripciones de héroes para un juego de rol de fantasía.',
});

for await (const héroe of elementStream) {
  console.log(héroe);
}
```

### Enum

Si deseas generar un valor enum específico, por ejemplo para tareas de clasificación,
puedes configurar la estrategia de salida a `enum`
y proporcionar una lista de valores posibles en el parámetro `enum`.

<Nota>La salida enum solo está disponible con `generateObject`.</Nota>

```ts highlight="5-6"
import { generateObject } from 'ai';

const { objeto } = await generateObject({
  model: tuModelo,
  output: 'enum',
  enum: ['acción', 'comedia', 'drama', 'terror', 'ciencia ficción'],
  prompt:
    'Clasifica el género de este guion de película: ' +
    '"Un grupo de astronautas viaja a través de un agujero de gusano en busca de un ' +
    'planeta habitable para la humanidad."',
});
```

### Sin Esquema

En algunos casos, puede que no desee utilizar un esquema,
por ejemplo cuando los datos son una solicitud de usuario dinámica.
Puede utilizar la configuración `output` para establecer el formato de salida a `no-schema` en esos casos
y omitir el parámetro de esquema.

```ts highlight="6"
import { openai } from '@ai-sdk/openai';
import { generateObject } from 'ai';

const { object } = await generateObject({
  model: openai('gpt-4-turbo'),
  output: 'no-schema',
  prompt: 'Genera una receta de lasaña.',
});
```

## Modo de Generación

Mientras que algunos modelos (como OpenAI) admiten nativamente la generación de objetos, otros requieren métodos alternativos, como llamadas a herramientas modificadas ([llamadas a herramientas](/docs/ai-sdk-core/tools-y-llamadas-a-herramientas)). La función `generateObject` permite especificar el método que utilizará para devolver datos estructurados.

- `auto`: El proveedor elegirá el mejor modo para el modelo. Este modo recomendado se utiliza por defecto.
- `tool`: Se proporciona una herramienta con el esquema JSON como parámetros y se instruye al proveedor para que la utilice.
- `json`: Se establece el formato de respuesta a JSON cuando lo admite el proveedor, por ejemplo, mediante modos JSON o generación guiada por gramática. Si la generación guiada por gramática no es compatible, se inyectan en el sistema el esquema JSON y las instrucciones para generar JSON que se ajuste al esquema.

<Nota>
  Por favor tenga en cuenta que no todos los proveedores admiten todos los modos de generación. Algunos proveedores no admiten la generación de objetos en absoluto.
</Nota>

## Nombre del Esquema y Descripción

Puedes especificar opcionalmente un nombre y descripción para el esquema. Estos se utilizan por algunos proveedores para orientación adicional del LLM, por ejemplo, a través del nombre del esquema o herramienta.

```ts highlight="6-7"
import { generateObject } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: yourModel,
  schemaName: 'Receta',
  schemaDescription: 'Una receta para un plato.',
  schema: z.object({
    name: z.string(),
    ingredients: z.array(z.object({ name: z.string(), amount: z.string() })),
    steps: z.array(z.string()),
  }),
  prompt: 'Genera una receta de lasaña.',
});
```

## Manejo de Errores

Cuando `generateObject` no puede generar un objeto válido, lanza un [`AI_NoObjectGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-object-generated-error).

Este error se produce cuando el proveedor de inteligencia artificial falla en generar un objeto que se pueda parsear y que cumpla con el esquema.
Puede surgir debido a las siguientes razones:

- El modelo falló en generar una respuesta.
- El modelo generó una respuesta que no se pudo parsear.
- El modelo generó una respuesta que no se pudo validar contra el esquema.

El error conserva la siguiente información para ayudarte a registrar el problema:

- `text`: El texto que se generó por el modelo. Esto puede ser el texto bruto o el texto de llamada de herramientas, dependiendo del modo de generación de objetos.
- `response`: Información de metadatos sobre la respuesta del modelo de lenguaje, incluyendo el identificador de respuesta, el timestamp y el modelo.
- `usage`: Uso del token de solicitud.
- `cause`: La causa del error (por ejemplo, un error de parsing de JSON). Puedes utilizar esto para un manejo de errores más detallado.

```ts
import { generateObject, NoObjectGeneratedError } from 'ai';

try {
  await generateObject({ model, schema, prompt });
} catch (error) {
  if (NoObjectGeneratedError.isInstance(error)) {
    console.log('AI_NoObjectGeneratedError');
    console.log('Causa:', error.cause);
    console.log('Texto:', error.text);
    console.log('Respuesta:', error.response);
    console.log('Uso:', error.usage);
  }
}
```

## Reparando JSON Inválido o Malformado

<Nota tipo="advertencia">
  La función `repairText` es experimental y puede cambiar en el futuro.
</Nota>

A veces el modelo generará JSON inválido o malformado.
Puedes utilizar la función `repairText` para intentar reparar el JSON.

Recibe el error, ya sea un `JSONParseError` o un `TypeValidationError`,
y el texto que fue generado por el modelo.
Puedes entonces intentar reparar el texto y devolver el texto reparado.

```ts highlight="7-10"
import { generateObject } from 'ai';

const { object } = await generateObject({
  model,
  schema,
  prompt,
  experimental_repairText: async ({ text, error }) => {
    // ejemplo: agregar una llave de cierre al texto
    return text + '}';
  },
});
```

## Salidas estructuradas con `generateText` y `streamText`

Puedes generar datos estructurados con `generateText` y `streamText` utilizando la configuración `experimental_output`.

<Nota>
  Algunos modelos, por ejemplo, aquellos de OpenAI, admiten salidas estructuradas y llamadas a herramientas
  al mismo tiempo. Esto solo es posible con `generateText` y `streamText`.
</Nota>

<Nota tipo="advertencia">
  La generación de salidas estructuradas con `generateText` y `streamText` es
  experimental y puede cambiar en el futuro.
</Nota>

### `generateText`

```ts highlight="2,4-18"
// `experimental_output` es un objeto estructurado que coincide con el esquema:
const { experimental_output } = await generateText({
  // ...
  experimental_output: Output.object({
    schema: z.object({
      nombre: z.string(),
      edad: z.number().nullable().describe('Edad de la persona.'),
      contacto: z.object({
        tipo: z.literal('email'),
        valor: z.string(),
      }),
      ocupación: z.object({
        tipo: z.literal('empleado'),
        empresa: z.string(),
        posición: z.string(),
      }),
    }),
  }),
  prompt: 'Generar un ejemplo de persona para la prueba.',
});
```

### `streamText`

```ts highlight="2,4-18"
// `experimental_partialOutputStream` contiene objetos generados parciales:
const { experimental_partialOutputStream } = await streamText({
  // ...
  experimental_output: Output.object({
    schema: z.object({
      nombre: z.string(),
      edad: z.number().nullable().describe('Edad de la persona.'),
      contacto: z.object({
        tipo: z.literal('email'),
        valor: z.string(),
      }),
      ocupación: z.object({
        tipo: z.literal('empleado'),
        empresa: z.string(),
        posición: z.string(),
      }),
    }),
  }),
  prompt: 'Generar un ejemplo de persona para la prueba.',
});
```

## Ejemplos Adicionales

Puede ver `generateObject` y `streamObject` en acción utilizando varias frameworks en los siguientes ejemplos:

### `generateObject`

<ExampleLinks
  examples={[
    {
      title: 'Aprende a generar objetos en Node.js',
      link: '/examples/node/generando-datos-estructurados/generate-object',
    },
    {
      title:
        'Aprende a generar objetos en Next.js con Manejadores de Rutas (SDK UI de Inteligencia Artificial)',
      link: '/examples/next-páginas/básicos/generando-objeto',
    },
    {
      title:
        'Aprende a generar objetos en Next.js con Acciones de Servidor (SDK RSC de Inteligencia Artificial)',
      link: '/examples/next-aplicación/básicos/generando-objeto',
    },
  ]}
/>

### `streamObject`

<ExampleLinks
  examples={[
    {
      title: 'Aprende a generar objetos en Node.js',
      link: '/examples/node/streaming-datos-estructurados/stream-object',
    },
    {
      title:
        'Aprende a generar objetos en Next.js con Manejadores de Rutas (SDK UI de Inteligencia Artificial)',
      link: '/examples/next-páginas/básicos/generación-de-objetos-en-Streaming',
    },
    {
      title:
        'Aprende a generar objetos en Next.js con Acciones de Servidor (SDK RSC de Inteligencia Artificial)',
      link: '/examples/next-aplicación/básicos/generación-de-objetos-en-Streaming',
    },
  ]}
/>

---
title: Llamada a Herramienta
description: Aprende sobre llamadas a herramientas y llamadas multi-paso (utilizando maxSteps) con el Core de SDK de Inteligencia Artificial.
---

# Llamada a Herramientas

Como se cubrió bajo Fundamentos, [herramientas](/docs/fundamentos/herramientas) son objetos que pueden ser llamados por el modelo para realizar una tarea específica.
Las herramientas del núcleo SDK de IA contienen tres elementos:

- **`description`**: Una descripción opcional de la herramienta que puede influir en cuándo se selecciona la herramienta.
- **`parameters`**: Un [esquema de Zod](/docs/fundamentos/herramientas)

# Esquemas) o un [esquema JSON](/docs/reference/ai-sdk-core/json-schema) que define los parámetros. El esquema se consume por el LLM y también se utiliza para validar las llamadas a herramientas del LLM.
- **`execute`**: Una función asíncrona opcional que se llama con los argumentos de la llamada a la herramienta. Produce un valor del tipo `RESULT` (tipo genérico). Es opcional porque quizás desee enviar las llamadas a herramientas al cliente o a una cola en lugar de ejecutarlas en el mismo proceso.

<Nota className="mb-2">
  Puede utilizar la función de ayuda [`tool`](/docs/reference/ai-sdk-core/tool) para
  inferir los tipos de los parámetros de `execute`.
</Nota>

El parámetro `tools` de `generateText` y `streamText` es un objeto que tiene los nombres de las herramientas como claves y las herramientas como valores:

```ts highlight="6-17"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const result = await generateText({
  model: yourModel,
  tools: {
    weather: tool({
      description: 'Obtener el clima en una ubicación',
      parameters: z.object({
        location: z.string().describe('La ubicación para obtener el clima'),
      }),
      execute: async ({ location }) => ({
        location,
        temperatura: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  prompt: '¿Cuál es el clima en San Francisco?',
});
```

<Nota>
  Cuando un modelo utiliza una herramienta, se llama una "llamada a herramienta" y el resultado de la herramienta se llama un "resultado de herramienta".
</Nota>

La llamada a herramientas no está restringida solo a la generación de texto.
También puede utilizarlo para renderizar interfaces de usuario (Generative UI).

## Llamadas Multi-Pasos (utilizando maxSteps)

Con la configuración `maxSteps`, puedes habilitar llamadas multi-pasos en `generateText` y `streamText`. Cuando `maxSteps` se establece en un número mayor que 1 y el modelo genera una llamada a herramienta, el SDK de IA desencadenará una nueva generación pasando el resultado de la herramienta hasta que no haya más llamadas a herramientas o se alcance el número máximo de pasos de herramientas.

<Nota>
  Para decidir qué valor establecer para `maxSteps`, considera la tarea más compleja que la llamada pueda manejar y el número de pasos secuenciales necesarios para su completación, más que el número de herramientas disponibles.
</Nota>

Por defecto, cuando utilizas `generateText` o `streamText`, se desencadena una sola generación (`maxSteps: 1`). Esto funciona bien para muchos casos de uso en los que puedes confiar en los datos de entrenamiento del modelo para generar una respuesta. Sin embargo, cuando proporcionas herramientas, el modelo ahora tiene la elección de generar una respuesta de texto normal o generar una llamada a herramienta. Si el modelo genera una llamada a herramienta, su generación está completa y ese paso está terminado.

Es posible que desees que el modelo genere texto después de que se haya ejecutado la herramienta, ya sea para resumir los resultados de la herramienta en el contexto de la consulta del usuario. En muchos casos, también podrías desear que el modelo utilice varias herramientas en una sola respuesta. Esto es donde entran en juego las llamadas multi-pasos.

Puedes pensar en las llamadas multi-pasos de manera similar a una conversación con una persona. Cuando haces una pregunta, si la persona no tiene el conocimiento requerido en su conocimiento común (los datos de entrenamiento del modelo), la persona puede necesitar buscar información (utilizar una herramienta) antes de poder proporcionarte una respuesta. De manera similar, el modelo puede necesitar llamar a una herramienta para obtener la información que necesita para responder a tu pregunta, donde cada generación (llamada a herramienta o generación de texto) es un paso.

### Ejemplo de código

```python
import ai

# Configura maxSteps para habilitar llamadas multi-pasos
ai.config.maxSteps = 3

# Llama a generateText con maxSteps configurado
response = ai.generateText(query, maxSteps=3)
```

### Ejemplo

En el siguiente ejemplo, hay dos pasos:

1. **Paso 1**
   1. Se envía la solicitud `'¿Cuál es el clima en San Francisco?'` al modelo.
   1. El modelo genera una llamada a herramienta.
   1. La llamada a herramienta se ejecuta.
1. **Paso 2**
   1. El resultado de la herramienta se envía al modelo.
   1. El modelo genera una respuesta considerando el resultado de la herramienta.

```ts highlight="18"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const { text, steps } = await generateText({
  model: tuModelo,
  tools: {
    weather: tool({
      description: 'Obtén el clima en una ubicación',
      parameters: z.object({
        location: z.string().describe('La ubicación para obtener el clima'),
      }),
      execute: async ({ location }) => ({
        location,
        temperatura: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  maxSteps: 5, // permite hasta 5 pasos
  prompt: '¿Cuál es el clima en San Francisco?',
});
```

<Nota> Puedes usar `streamText` de manera similar.</Nota>

### Pasos

Para acceder a las llamadas a herramientas intermedias y resultados, puedes usar la propiedad `steps` en el objeto de resultado
o el callback `onFinish` de `streamText`.
Contiene todo el texto, llamadas a herramientas, resultados de herramientas, y más de cada paso.

#### Ejemplo: Extraer resultados de herramientas de todos los pasos

```ts highlight="3,9-10"
import { generateText } from 'ai';

const { steps } = await generateText({
  model: openai('gpt-4-turbo'),
  maxSteps: 10,
  // ...
});

// extraer todas las llamadas a herramientas de los pasos:
const todasLasLlamadasA Herramientas = steps.flatMap(paso => paso.toolCalls);
```

### `onStepFinish` callback

Cuando se utiliza `generateText` o `streamText`, se puede proporcionar un callback `onStepFinish` que se activa cuando un paso está terminado,
es decir, cuando están disponibles todos los deltas de texto, las llamadas a herramientas y los resultados de herramientas para el paso.
Cuando se tienen múltiples pasos, el callback se activa para cada paso.

```tsx highlight="5-7"
import { generateText } from 'ai';

const resultado = await generateText({
  // ...
  onStepFinish({ texto, toolCalls, toolResults, finishReason, usage }) {
    // su propia lógica, por ejemplo, para guardar la historia de la conversación o registrar el uso
  },
});
```

### `experimental_prepareStep` callback

<Nota type="warning">
  El callback `experimental_prepareStep` es experimental y puede cambiar en el futuro. Está disponible solo en la función `generateText`.
</Nota>

El callback `experimental_prepareStep` se llama antes de que comience una etapa.

Se llama con los siguientes parámetros:

- `model`: El modelo que se pasó a `generateText`.
- `maxSteps`: El número máximo de pasos que se pasó a `generateText`.
- `stepNumber`: El número de la etapa que se está ejecutando.
- `steps`: Las etapas que se han ejecutado hasta ahora.

Puedes utilizarlo para proporcionar diferentes configuraciones para una etapa.

```tsx highlight="5-7"
import { generateText } from 'ai';

const result = await generateText({
  // ...
  experimental_prepareStep: async ({ model, stepNumber, maxSteps, steps }) => {
    if (stepNumber === 0) {
      return {
        // utilice un modelo diferente para esta etapa:
        model: modelForThisParticularStep,
        // fuerce una elección de herramienta para esta etapa:
        toolChoice: { type: 'tool', toolName: 'tool1' },
        // limite las herramientas disponibles para esta etapa:
        experimental_activeTools: ['tool1'],
      };
    }

    // cuando no se devuelve nada, se utilizan las configuraciones predeterminadas
  },
});
```

## Mensajes de Respuesta

Agregar los mensajes generados del asistente y la herramienta a tu historial de conversación es una tarea común,
especialmente si estás utilizando llamadas de herramientas de varios pasos.

Ambos `generateText` y `streamText` tienen una propiedad `response.messages` que puedes utilizar para agregar los mensajes del asistente y la herramienta a tu historial de conversación.
También está disponible en el callback `onFinish` de `streamText`.

La propiedad `response.messages` contiene un arreglo de objetos `CoreMessage` que puedes agregar a tu historial de conversación:

```ts
import { generateText } from 'ai';

const mensajes: CoreMessage[] = [
  // ...
];

const { response } = await generateText({
  // ...
  mensajes,
});

// agregar los mensajes de respuesta a tu historial de conversación:
mensajes.push(...response.mensajes); // streamText: ...((await response).mensajes)
```

## Elección de Herramienta

Puedes utilizar la configuración `toolChoice` para influir en cuándo se selecciona una herramienta.
Soporta las siguientes configuraciones:

- `auto` (por defecto): el modelo puede decidir si y qué herramientas llamar.
- `required`: el modelo debe llamar a una herramienta. Puede decidir qué herramienta llamar.
- `none`: el modelo no debe llamar herramientas
- `{ type: 'tool', toolName: string (typed) }`: el modelo debe llamar a la herramienta especificada

```ts highlight="18"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const result = await generateText({
  model: yourModel,
  tools: {
    weather: tool({
      description: 'Obtener el clima en una ubicación',
      parameters: z.object({
        location: z.string().describe('La ubicación para obtener el clima'),
      }),
      execute: async ({ location }) => ({
        location,
        temperatura: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  toolChoice: 'required', // fuerza al modelo a llamar a una herramienta
  prompt: '¿Cuál es el clima en San Francisco?',
});
```

## Opciones de Ejecución de Herramientas

Cuando se llaman herramientas, reciben opciones adicionales como un segundo parámetro.

### Identificador de Llamada de Herramienta

El identificador de la llamada de herramienta se transfiere a la ejecución de la herramienta.
Puedes utilizarlo, por ejemplo, cuando se envían información relacionada con la llamada de herramienta junto con los datos de flujo.

```ts highlight="14-20"
import { StreamData, streamText, tool } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const data = new StreamData();

  const result = streamText({
    // ...
    messages,
    tools: {
      miHerramienta: tool({
        // ...
        execute: async (args, { toolCallId }) => {
          // devuelve e.g. estado personalizado para la llamada de herramienta
          data.appendMessageAnnotation({
            type: 'estado-de-herramienta',
            toolCallId,
            status: 'en-proceso',
          });
          // ...
        },
      }),
    },
    onFinish() {
      data.close();
    },
  });

  return result.toDataStreamResponse({ data });
}
```

### Mensajes

Los mensajes que se enviaron al modelo de lenguaje para iniciar la respuesta que contenía la llamada a la herramienta se envían al ejecución de la herramienta.
Puedes acceder a ellos en el segundo parámetro de la función `execute`.
En llamadas multi-pasos, los mensajes contienen el texto, las llamadas a herramientas y los resultados de herramientas de todos los pasos anteriores.

```ts highlight="8-9"
import { generateText, tool } from 'ai';

const result = await generateText({
  // ...
  tools: {
    miHerramienta: tool({
      // ...
      execute: async (args, { mensajes }) => {
        // usa la historia de mensajes en llamadas a otros modelos de lenguaje
        return algo;
      },
    }),
  },
});
```

### Señales de Aborto

Las señales de aborto de `generateText` y `streamText` se transmiten a la ejecución de la herramienta.
Puedes acceder a ellas en el segundo parámetro de la función `execute` y, por ejemplo, abortar cálculos largos en ejecución o transmitirlas a llamadas de fetch dentro de herramientas.

```ts highlight="6,11,14"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const resultado = await generateText({
  modelo: tuModelo,
  abortSignal: miAbortSignal, // señal que se transmitirá a herramientas
  herramientas: {
    weather: tool({
      descripción: 'Obtener el clima en una ubicación',
      parámetros: z.object({ ubicación: z.string() }),
      execute: async ({ ubicación }, { abortSignal }) => {
        return fetch(
          `https://api.weatherapi.com/v1/current.json?q=${ubicación}`,
          { signal: abortSignal }, // transmitir la señal de aborto a fetch
        );
      },
    }),
  },
  prompt: '¿Cuál es el clima en San Francisco?',
});
```

## Tipos

La modularización de tu código a menudo requiere definir tipos para garantizar la seguridad de tipos y la reutilización.
Para habilitar esto, el SDK de IA proporciona varios tipos auxiliares para herramientas, llamadas a herramientas y resultados de herramientas.

Puedes usarlos para tipar fuertemente tus variables, parámetros de funciones y tipos de retorno
en partes del código que no están directamente relacionadas con `streamText` o `generateText`.

Cada llamada a herramienta se tipa con `ToolCall<NAME extends string, ARGS>`, dependiendo
de la herramienta que se ha invocado.
De manera similar, los resultados de herramientas se tipan con `ToolResult<NAME extends string, ARGS, RESULT>`.

Las herramientas en `streamText` y `generateText` se definen como un conjunto de herramientas.
Los ayudantes de inferencia de tipos `ToolCallUnion<TOOLS extends ToolSet>`
y `ToolResultUnion<TOOLS extends ToolSet>` se pueden usar para
extraer los tipos de llamada a herramienta y resultados de herramienta de las herramientas.

```ts highlight="18-19,23-24"
import { openai } from '@ai-sdk/openai';
import { ToolCallUnion, ToolResultUnion, generateText, tool } from 'ai';
import { z } from 'zod';

const miConjuntoDeHerramientas = {
  primeraHerramienta: tool({
    descripcion: 'Saluda al usuario',
    parámetros: z.object({ nombre: z.string() }),
    ejecutar: async ({ nombre }) => `Hola, ${nombre}!`,
  }),
  segundaHerramienta: tool({
    descripcion: 'Le dice al usuario su edad',
    parámetros: z.object({ edad: z.number() }),
    ejecutar: async ({ edad }) => `Tienes ${edad} años!`,
  }),
};

type MiLlamadaATool = ToolCallUnion<typeof miConjuntoDeHerramientas>;
type MiResultadoDeTool = ToolResultUnion<typeof miConjuntoDeHerramientas>;
```

```markdown
async function generarAlgo(prompt: string): Promise<{
  texto: string;
  llamadasHerramientas: Array<MiLlamadaHerramienta>; // llamadas de herramientas tipadas
  resultadosHerramientas: Array<MiResultadoHerramienta>; // resultados de herramientas tipados
}> {
  return generarTexto({
    modelo: openai('gpt-4o'),
    herramientas

## Manejo de Errores

El SDK de IA tiene tres errores relacionados con llamadas a herramientas:

- [`NoSuchToolError`](/docs/reference/ai-sdk-errors/ai-no-such-tool-error): el modelo intenta llamar a una herramienta que no está definida en el objeto de herramientas
- [`InvalidToolArgumentsError`](/docs/reference/ai-sdk-errors/ai-invalid-tool-arguments-error): el modelo llama a una herramienta con argumentos que no coinciden con los parámetros de la herramienta
- [`ToolExecutionError`](/docs/reference/ai-sdk-errors/ai-tool-execution-error): un error que ocurrió durante la ejecución de la herramienta
- [`ToolCallRepairError`](/docs/reference/ai-sdk-errors/ai-tool-call-repair-error): un error que ocurrió durante la reparación de la llamada a la herramienta

### `generateText`

`generateText` lanza errores y se pueden manejar utilizando un bloque `try`/`catch`:

```ts
try {
  const resultado = await generateText({
    //...
  });
} catch (error) {
  if (NoSuchToolError.isInstance(error)) {
    // manejar el error de herramienta no encontrada
  } else if (InvalidToolArgumentsError.isInstance(error)) {
    // manejar el error de argumentos de herramienta inválidos
  } else if (ToolExecutionError.isInstance(error)) {
    // manejar el error de ejecución de herramienta
  } else {
    // manejar otros errores
  }
}
```

### `streamText`

`streamText` envía los errores como parte del flujo completo. Las partes de error contienen el objeto de error.

Al utilizar `toDataStreamResponse`, puedes pasar una función `getErrorMessage` para extraer el mensaje de error de la parte de error y enviarlo como parte de la respuesta del flujo de datos:

```ts
const result = streamText({
  // ...
});

return result.toDataStreamResponse({
  getErrorMessage: error => {
    if (NoSuchToolError.isInstance(error)) {
      return 'El modelo intentó llamar a una herramienta desconocida.';
    } else if (InvalidToolArgumentsError.isInstance(error)) {
      return 'El modelo llamó a una herramienta con argumentos inválidos.';
    } else if (ToolExecutionError.isInstance(error)) {
      return 'Ocurrió un error durante la ejecución de la herramienta.';
    } else {
      return 'Ocurrió un error desconocido.';
    }
  },
});
```

## Reparación de llamadas a herramientas

<Nota tipo="advertencia">
  La función de reparación de llamadas a herramientas es experimental y puede cambiar en el futuro.
</Nota>

Los modelos de lenguaje a veces fallan al generar llamadas a herramientas válidas,
especialmente cuando los parámetros son complejos o el modelo es más pequeño.

Puedes usar la función `experimental_repairToolCall` para intentar reparar la llamada a herramientas con una función personalizada.

Puedes utilizar diferentes estrategias para reparar la llamada a herramientas:

- Utiliza un modelo con salidas estructuradas para generar los argumentos.
- Envía los mensajes, el prompt del sistema y el esquema de herramienta a un modelo más fuerte para generar los argumentos.
- Proporciona instrucciones de reparación más específicas basadas en la herramienta que se llamó.

### Ejemplo: Usar un modelo con salidas estructuradas para la reparación

```ts
import { openai } from '@ai-sdk/openai';
import { generateObject, generateText, NoSuchToolError, tool } from 'ai';

const result = await generateText({
  model,
  tools,
  prompt,

  experimental_repairToolCall: async ({
    toolCall,
    tools,
    parameterSchema,
    error,
  }) => {
    if (NoSuchToolError.isInstance(error)) {
      return null; // no intentar reparar nombres de herramientas inválidos
    }

    const tool = tools[toolCall.toolName as keyof typeof tools];

    const { object: reparadosArgs } = await generateObject({
      model: openai('gpt-4o', { salidasEstructuradas: true }),
      schema: tool.parameters,
      prompt: [
        `El modelo intentó llamar a la herramienta "${toolCall.toolName}"` +
          ` con los siguientes argumentos:`,
        JSON.stringify(toolCall.args),
        `La herramienta acepta el siguiente esquema:`,
        JSON.stringify(parameterSchema(toolCall)),
        'Por favor, corregir los argumentos.',
      ].join('\n'),
    });

    return { ...toolCall, args: JSON.stringify(reparadosArgs) };
  },
});
```

### Ejemplo: Usar la estrategia de re-preguntar para reparación

```ts
import { openai } from '@ai-sdk/openai';
import { generateObject, generateText, NoSuchToolError, tool } from 'ai';

const resultado = await generateText({
  modelo,
  herramientas,
  prompt,
```

### Nota: 
Si el modelo o la herramienta no están disponibles, se lanzará un error `NoSuchTool

`experimental_repairToolCall`: `async` ({
    `toolCall`,
    `tools`,
    `error`,
    `messages`,
    `system`,
  }) => {
    const resultado = await generarTexto({
      modelo,
      sistema,
      mensajes: [
        ...mensajes,
        {
          papel: 'asistente',
          contenido: [
            {
              tipo: 'llamada-a-herramienta',
              idDeLlamadaAHerramienta: `toolCall.toolCallId`,
              nombreDeHerramienta: `toolCall.toolName`,
              argumentos: `toolCall.args`,
            },
          ],
        },
        {
          papel: 'herramienta' as const,
          contenido: [
            {
              tipo: 'resultado-de-herramienta',
              idDeLlamadaAHerramienta: `toolCall.toolCallId`,
              nombreDeHerramienta: `toolCall.toolName`,
              resultado: `error.message`,
            },
          ],
       

`return newToolCall != null
      ? {
          tipoDeLlamadaHerramienta: 'function' as const,
          idDeLlamadaHerramienta: newToolCall.toolCallId,
          nombreDeHerramienta: newToolCall.toolName,
          args: JSON.stringify(new

## Herramientas Activas

<Nota tipo="advertencia">
  La propiedad `activeTools` es experimental y puede cambiar en el futuro.
</Nota>

Los modelos de lenguaje solo pueden manejar un número limitado de herramientas a la vez, dependiendo del modelo.
Para permitir el tipado estático utilizando un gran número de herramientas y limitar las herramientas disponibles al modelo al mismo tiempo,
el SDK de IA proporciona la propiedad `experimental_activeTools`.

Es una matriz de nombres de herramientas que están actualmente activas.
Por defecto, el valor es `undefined` y todas las herramientas están activas.

```ts highlight="7"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: openai('gpt-4o'),
  tools: miConjuntoDeHerramientas,
  experimental_activeTools: ['primeraHerramienta'],
});
```

## Resultados de Herramientas Multi-modal

<Nota tipo="advertencia">
  Los resultados de herramientas multi-modal son experimentales y solo están soportados por Anthropic.
</Nota>

Para enviar resultados de herramientas multi-modal, por ejemplo, capturas de pantalla, de vuelta al modelo, deben ser convertidos en un formato específico.

Las herramientas de Core SDK de AI tienen una función `experimental_toToolResultContent` opcional que convierte el resultado de la herramienta en una parte de contenido.

Aquí hay un ejemplo para convertir una captura de pantalla en una parte de contenido:

```ts highlight="22-27"
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  tools: {
    computer: anthropic.tools.computer_20241022({
      // ...
      async execute({ action, coordinate, text }) {
        switch (action) {
          case 'screenshot': {
            return {
              type: 'image',
              data: fs
                .readFileSync('./data/screenshot-editor.png')
                .toString('base64'),
            };
          }
          default: {
            return `executed ${action}`;
          }
        }
      },
```

// mapa a contenido de resultado de herramienta para consumo de LLM:
      experimental_toToolResultContent(result) {
        return typeof result === 'string'
          ? [{ type: 'text', text: result }]
          : [{ type: 'image', data: result.data, mimeType: 'image/png' }];
      },
    }),
  },
  // ...
});

## Extractando Herramientas

Una vez que tengas muchas herramientas, podrías querer extraerlas en archivos separados.
La función auxiliar `tool` es crucial para esto, ya que garantiza la inferencia de tipos correcta.

Aquí está un ejemplo de una herramienta extraída:

```ts filename="tools/weather-tool.ts" highlight="1,4-5"
import { tool } from 'ai';
import { z } from 'zod';

// la función auxiliar `tool` garantiza la inferencia de tipos correcta:
export const weatherTool = tool({
  description: 'Obtener el clima en una ubicación',
  parameters: z.object({
    location: z.string().describe('La ubicación para obtener el clima'),
  }),
  execute: async ({ location }) => ({
    location,
    temperatura: 72 + Math.floor(Math.random() * 21) - 10,
  }),
});
```

## Herramientas de MCP

<Nota tipo="advertencia">
  Las herramientas de MCP están en versión experimental y pueden cambiar en el futuro.
</Nota>

El SDK de AI admite conectar a servidores de [Protocolo de Contexto de Modelo (MCP)](https://modelcontextprotocol.io/) para acceder a sus herramientas.
Esto permite que las aplicaciones de inteligencia artificial descubran y utilicen herramientas a través de servicios variados a través de una interfaz estándar.

### Inicializando un cliente de MCP

Crea un cliente de MCP utilizando:

- `SSE` (Eventos de Servidor-Servidor): Utiliza la comunicación en tiempo real basada en HTTP, más adecuada para servidores remotos que necesitan enviar datos a través de la red
- `stdio`: Utiliza los flujos de entrada y salida estándar para la comunicación, ideal para servidores de herramientas locales que se ejecutan en la misma máquina (como herramientas de línea de comandos o servicios locales)
- Transporte personalizado: Trae tu propio transporte implementando la interfaz `MCPTransport`, ideal cuando se implementan transportes desde el SDK oficial de TypeScript de MCP (por ejemplo, `StreamableHTTPClientTransport`)

#### Transporte SSE

El SSE se puede configurar utilizando un objeto simple con una propiedad `type` y `url`:

```typescript
import { experimental_createMCPClient as createMCPClient } from 'ai';

const mcpClient = await createMCPClient({
  transport: {
    type: 'sse',
    url: 'https://mi-servidor.com/sse',

    // opcional: configura encabezados HTTP, por ejemplo, para la autenticación
    headers: {
      Authorization: 'Bearer mi-api-key',
    },
  },
});
```

#### Transporte Stdio

El transporte Stdio requiere importar la clase `StdioMCPTransport` desde el paquete `ai/mcp-stdio`:

```typescript
import { experimental_createMCPClient as createMCPClient } from 'ai';
import { Experimental_StdioMCPTransport as StdioMCPTransport } from 'ai/mcp-stdio';

const mcpClient = await createMCPClient({
  transport: new StdioMCPTransport({
    command: 'node',
    args: ['src/stdio/dist/server.js'],
  }),
});
```

#### Transporto Personalizado

También puedes traer tu propio transporte, siempre y cuando implemente la interfaz `MCPTransport`. A continuación, se muestra un ejemplo de uso del nuevo `StreamableHTTPClientTransport` desde el SDK de Typescript oficial de MCP:

```typescript
import {
  MCPTransport,
  experimental_createMCPClient as createMCPClient,
} from 'ai';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp';

const url = new URL('http://localhost:3000/mcp');
const mcpClient = await createMCPClient({
  transport: new StreamableHTTPClientTransport(url, {
    sessionId: 'session_123',
  }),
});
```

<Nota>
  El cliente devuelto por la función `experimental_createMCPClient` es un cliente ligero destinado para uso en la conversión de herramientas. Actualmente no admite todas las características del cliente de MCP completo, como: autorización, gestión de sesión, streams reanudables y recepción de notificaciones.
</Nota>

#### Cerrando el Cliente MCP

Después de la inicialización, debes cerrar el cliente MCP según el patrón de uso:

- Para usos de corta duración (por ejemplo, solicitudes únicas), cierra el cliente cuando la respuesta está lista
- Para clientes de larga duración (por ejemplo, aplicaciones de línea de comandos), mantén el cliente abierto pero asegúrate de cerrarlo cuando la aplicación se termine

Cuando se están transmitiendo respuestas, puedes cerrar el cliente cuando la respuesta del LLM ha terminado. Por ejemplo, al usar `streamText`, debes utilizar el callback `onFinish`:

```typescript
const mcpClient = await experimental_createMCPClient({
  // ...
});

const tools = await mcpClient.tools();

const result = await streamText({
  model: openai('gpt-4o'),
  tools,
  prompt: '¿Cuál es el tiempo en Brooklyn, Nueva York?',
  onFinish: async () => {
    await mcpClient.close();
  },
});
```

Cuando se están generando respuestas sin transmisión, puedes utilizar try/finally o funciones de limpieza en tu marco de trabajo:

```typescript
let mcpClient: MCPClient | undefined;

try {
  mcpClient = await experimental_createMCPClient({
    // ...
  });
} finally {
  await mcpClient?.close();
}
```

### Utilizando Herramientas MCP

El método `tools` del cliente actúa como un adaptador entre herramientas MCP y herramientas de SDK de IA. Soporta dos enfoques para trabajar con esquemas de herramientas:

#### Descubrimiento de Esquemas

El enfoque más simple donde todas las herramientas ofrecidas por el servidor se enumeran, y los tipos de parámetros de entrada se infieren basándose en los esquemas proporcionados por el servidor:

```typescript
const tools = await mcpClient.tools();
```

**Ventajas:**

- Más sencillo de implementar
- Se mantiene automáticamente sincronizado con cambios del servidor

**Desventajas:**

- No hay seguridad de tipos de TypeScript durante el desarrollo
- No hay autocompletado de IDE para parámetros de herramientas
- Los errores solo se surfican en tiempo de ejecución
- Se cargan todas las herramientas del servidor

#### Definición de Esquema

También puedes definir explícitamente los esquemas de herramientas y sus parámetros de entrada en tu código cliente:

```typescript
import { z } from 'zod';

const tools = await mcpClient.tools({
  schemas: {
    'obtener-datos': {
      parameters: z.object({
        query: z.string().describe('La consulta de datos'),
        format: z.enum(['json', 'text']).optional(),
      }),
    },
    // Para herramientas con cero argumentos, debes utilizar un objeto vacío:
    'herramienta-con-no-argumentos': {
      parameters: z.object({}),
    },
  },
});
```

**Ventajas:**

- Control sobre las herramientas que se cargan
- Tipo de seguridad de TypeScript completo
- Mejor soporte de IDE con autocompletar
- Captura de coincidencias de parámetros durante el desarrollo

**Desventajas:**

- Necesidad de mantener manualmente los esquemas en sincronía con el servidor
- Más código para mantener

Cuando defines `schemas`, el cliente solo descargará las herramientas definidas explícitamente, incluso si el servidor ofrece herramientas adicionales. Esto puede ser beneficioso para:

- Mantener tu aplicación enfocada en las herramientas que necesita
- Reducir la carga innecesaria de herramientas
- Hacer explícitas las dependencias de herramientas

## Ejemplos

Puede ver herramientas en acción utilizando diferentes marcos en los siguientes ejemplos:

<ExampleLinks
  examples={[
    {
      title: 'Aprende a utilizar herramientas en Node.js',
      link: '/cookbook/node/call-tools',
    },
    {
      title: 'Aprende a utilizar herramientas en Next.js con Manejadores de Rutas',
      link: '/cookbook/next/call-tools',
    },
    {
      title: 'Aprende a utilizar herramientas MCP en Node.js',
      link: '/cookbook/node/mcp-tools',
    },
  ]}
/>

---
titulo: Ingeniería de Prompts
descripcion: Aprende a desarrollar prompts con SDK Core de IA.
---

# Ingeniería de Prompts

## Consejos

### Instrucciones para Herramientas

Cuando creas instrucciones que incluyen herramientas, obtener buenos resultados puede ser complicado a medida que aumenta el número y la complejidad de tus herramientas.

Aquí hay algunas pautas para ayudarte a obtener los mejores resultados:

1. Utiliza un modelo que sea fuerte en llamadas a herramientas, como `gpt-4` o `gpt-4-turbo`. Los modelos más débiles a menudo luchan por llamar herramientas de manera efectiva y sin errores.
1. Mantén el número de herramientas bajo, por ejemplo, a 5 o menos.
1. Mantén la complejidad de los parámetros de la herramienta baja. Esquemas Zod complejos con muchos elementos anidados y opcionales, uniones, etc. pueden ser desafiantes para el modelo de trabajar con ellos.
1. Utiliza nombres semánticamente significativos para tus herramientas, parámetros, propiedades de parámetros, etc. Cuanta más información pasas al modelo, mejor puede entender lo que quieres.
1. Agrega `.describe("...")` a las propiedades de esquema Zod para dar al modelo pistas sobre qué es un propiedad particular para.
1. Cuando el resultado de una herramienta puede ser confuso para el modelo y existen dependencias entre herramientas, utiliza el campo `description` de una herramienta para proporcionar información sobre el resultado de la ejecución de la herramienta.
1. Puedes incluir ejemplos de entrada/salida de llamadas a herramientas en tu instrucción para ayudar al modelo a entender cómo utilizar las herramientas. Ten en cuenta que las herramientas trabajan con objetos JSON, por lo que los ejemplos deben utilizar JSON.

En general, el objetivo debe ser proporcionar al modelo toda la información que necesita de manera clara.

### Herramientas y Esquemas de Datos Estructurados

La mapeación de esquemas Zod a entradas de LLM (normalmente esquema de JSON) no es siempre directa, ya que la mapeación no es uno a uno.

#### Fechas de Zod

Zod espera objetos de fecha JavaScript, pero los modelos devuelven fechas como cadenas de texto.
Puedes especificar y validar el formato de fecha utilizando `z.string().datetime()` o `z.string().date()`,
y luego utilizar un transformador de Zod para convertir la cadena a un objeto de fecha.

```ts highlight="7-10"
const result = await generateObject({
  model: openai('gpt-4-turbo'),
  schema: z.object({
    eventos: z.array(
      z.object({
        evento: z.string(),
        fecha: z
          .string()
          .date()
          .transform(value => new Date(value)),
      }),
    ),
  }),
  prompt: 'Lista 5 eventos importantes del año 2000.',
});
```

## Depuración

### Inspeccionando advertencias

No todos los proveedores admiten todas las características de la SDK de IA.
Los proveedores lanzan excepciones o devuelven advertencias cuando no admiten una característica.
Para verificar si su solicitud, herramientas y ajustes se manejan correctamente por el proveedor, puedes verificar las advertencias de llamada:

```ts
const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Hola, mundo!',
});

console.log(result.advertencias);
```

### Cuerpos de Solicitud HTTP

Puedes inspeccionar los cuerpos de solicitud HTTP crudos para modelos que los expone, por ejemplo [OpenAI](/providers/ai-sdk-providers/openai).
Esto te permite inspeccionar el payload exacto que se envía al proveedor del modelo de manera específica del proveedor.

Los cuerpos de solicitud están disponibles a través de la propiedad `request.body` de la respuesta:

```ts highlight="6"
const resultado = await generarTexto({
  modelo: openai('gpt-4o'),
  prompt: 'Hola, mundo!',
});

console.log(resultado.request.body);
```

---
titulo: Configuración
descripcion: Aprende a configurar el SDK de IA.
---

# Configuración

Los modelos de lenguaje grande (LLMs) suelen proporcionar configuraciones para aumentar su salida.

Todas las funciones del SDK de IA admiten las siguientes configuraciones comunes, además del modelo, la [solicitud](./solicitudes), y configuraciones adicionales específicas del proveedor:

```ts highlight="3-5"
const resultado = await generarTexto({
  modelo: tuModelo,
  maxTokens: 512,
  temperatura: 0.3,
  maxRetries: 5,
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
});
```

<Nota>
  Algunos proveedores no admiten todas las configuraciones comunes. Si utilizas una configuración con un proveedor que no la admite, se generará una advertencia. Puedes verificar la propiedad `warnings` del objeto de resultado para ver si se generaron advertencias.
</Nota>

### `maxTokens`

Número máximo de tokens para generar.

### `temperatura`

Configuración de temperatura.

El valor se pasa directamente al proveedor. El rango depende del proveedor y del modelo.
Para la mayoría de los proveedores, `0` significa resultados casi deterministas, y valores más altos significan más aleatoriedad.

Se recomienda establecer o `temperatura` o `topP`, pero no ambos.

### `topP`

Muestreo de núcleo.

El valor se pasa directamente al proveedor. El rango depende del proveedor y del modelo.
Para la mayoría de los proveedores, el muestreo de núcleo es un número entre 0 y 1.
Por ejemplo, 0.1 significa que solo se consideran tokens con el 10% de la masa de probabilidad.

Se recomienda establecer o `temperature` o `topP`, pero no ambos.

### `topK`

Solo muestra desde las opciones top K para cada token sucesivo.

Usado para eliminar respuestas de "cola larga" de baja probabilidad.
Recomendado para casos de uso avanzados solo. Normalmente solo se necesita usar `temperature`.

### `presencePenalty`

La penalización de presencia afecta la probabilidad del modelo para repetir información que ya está en la solicitud.

El valor se pasa directamente al proveedor. El rango depende del proveedor y del modelo.
Para la mayoría de los proveedores, `0` significa sin penalización.

### `frequencyPenalty`

La penalización de frecuencia afecta la probabilidad del modelo para usar repetidamente las mismas palabras o frases.

El valor se pasa directamente al proveedor. El rango depende del proveedor y del modelo.
Para la mayoría de los proveedores, `0` significa sin penalización.

### `stopSequences`

Las secuencias de parada para usar para detener la generación de texto.

Si se establece, el modelo detendrá la generación de texto cuando se genere una de las secuencias de parada.
Los proveedores pueden tener límites en el número de secuencias de parada.

### `seed`

Es la semilla (entero) para usar para la muestreo aleatorio.
Si se establece y está soportado por el modelo, las llamadas generarán resultados determinísticos.

### `maxRetries`

Número máximo de intentos. Establezca a 0 para deshabilitar los intentos. Por defecto: `2`.

### `abortSignal`

Un señal de abort opcional que se puede usar para cancelar la llamada.

La señal de abort se puede enviar desde una interfaz de usuario para cancelar la llamada,
o para definir un tiempo límite.

#### Ejemplo: Tiempo límite

```ts
const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  abortSignal: AbortSignal.timeout(5000), // 5 segundos
});
```

### Encabezados

Encabezados adicionales HTTP para enviar con la solicitud. Solo aplicable para proveedores basados en HTTP.

Puedes utilizar los encabezados de solicitud para proporcionar información adicional al proveedor,
dependiendo de lo que el proveedor soporte. Por ejemplo, algunos proveedores de observabilidad soportan
encabezados como `Prompt-Id`.

```ts
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  headers: {
    'Prompt-Id': 'mi-prompt-id',
  },
});
```

<Nota>
  La configuración `headers` es para encabezados específicos de solicitud. También puedes establecer
  `headers` en la configuración del proveedor. Estos encabezados se enviarán con cada solicitud realizada por el proveedor.
</Nota>

---
titulo: Embebedores
descripcion: Aprende a embeber valores con el SDK de IA.
---

# Embebedores

Los embebedores son una forma de representar palabras, frases o imágenes como vectores en un espacio de alta dimensionalidad.
En este espacio, las palabras similares están cerca una de otra, y la distancia entre palabras se puede utilizar para medir su similitud.

## Embeber un Valor Único

El SDK de IA proporciona la función [`embed`](/docs/reference/ai-sdk-core/embed) para embeber valores únicos, lo cual es útil para tareas como encontrar palabras o frases similares
o agrupar texto.
Puedes utilizarlo con modelos de embebedores, por ejemplo `openai.embedding('text-embedding-3-large')` o `mistral.embedding('mistral-embed')`.

```tsx
import { embed } from 'ai';
import { openai } from '@ai-sdk/openai';

// 'embedding' es un objeto de embebedor único (number[])
const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-pequeño'),
  value: 'día soleado en la playa',
});
```

## Incorporando Muchos Valores

Al cargar datos, por ejemplo, al preparar un almacén de datos para la generación reforzada con datos (RAG),
a menudo es útil incorporar muchos valores al mismo tiempo (incorporación en lote).

El SDK de IA proporciona la función `embedMany` para este fin.
De manera similar a `embed`, puede utilizarla con modelos de incorporación,
por ejemplo `openai.embedding('text-embedding-3-large')` o `mistral.embedding('mistral-embed')`.

```tsx
import { openai } from '@ai-sdk/openai';
import { embedMany } from 'ai';

// 'embeddings' es un array de objetos de incorporación (number[][]).
// Está ordenado en el mismo orden que los valores de entrada.
const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-pequeño'),
  values: [
    'día soleado en la playa',
    'tarde lluviosa en la ciudad',
    'noche nevada en las montañas',
  ],
});
```

## Similaridad de Incorporación

Después de incorporar valores, puede calcular la similaridad entre ellos utilizando la función `cosineSimilarity`.
Esto es útil para encontrar palabras o frases similares en un conjunto de datos.
También puede ordenar y filtrar elementos relacionados según su similaridad.

```ts highlight={"2,10"}
import { openai } from '@ai-sdk/openai';
import { cosineSimilarity, embedMany } from 'ai';

const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-pequeño'),
  values: ['día soleado en la playa', 'tarde lluviosa en la ciudad'],
});

console.log(
  `similaridad coseno: ${cosineSimilarity(embeddings[0], embeddings[1])}`,
);
```

## Uso de Tokens

Muchos proveedores cobran basados en el número de tokens utilizados para generar embebedores.
Ambos `embed` y `embedMany` proporcionan información de uso de tokens en la propiedad `usage` del objeto de resultados:

```ts highlight={"4,9"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding, usage } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'día soleado en la playa',
});

console.log(usage); // { tokens: 10 }
```

## Configuración

### Retrasos

Ambos `embed` y `embedMany` aceptan un parámetro `maxRetries` opcional de tipo `number`
que puedes utilizar para establecer el número máximo de reintentos para el proceso de embebedor.
Por defecto, es de `2` reintentos (3 intentos en total). Puedes establecerlo en `0` para deshabilitar los reintentos.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'día soleado en la playa',
  maxRetries: 0, // Deshabilitar reintentos
});
```

### Señales de aborto y tiempos de espera

Ambos `embed` y `embedMany` aceptan un parámetro `abortSignal` opcional de
tipo [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
que puedes utilizar para abortar el proceso de embebedor o establecer un tiempo de espera.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'día soleado en la playa',
  abortSignal: AbortSignal.timeout(1000), // Abortar después de 1 segundo
});

### Encabezados Personalizados

Ambos `embed` y `embedMany` aceptan un parámetro `headers` opcional de tipo `Record<string, string>`
que puedes utilizar para agregar encabezados personalizados a la solicitud de inserción.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'día soleado en la playa',
  headers: { 'X-Custom-Header': 'custom-value' },
});
```

## Proveedores y Modelos de Inserción

Several varios proveedores ofrecen modelos de inserción:

| Proveedor                                                                                  | Modelo                           | Dimensiones de Inserción |
| ----------------------------------------------------------------------------------------- | ------------------------------- | -------------------- |
| [OpenAI](/providers/ai-sdk-providers/openai#embedding-models)                             | `text-embedding-3-large`        | 3072                 |
| [OpenAI](/providers/ai-sdk-providers/openai#embedding-models)                             | `text-embedding-3-small`        | 1536                 |
| [OpenAI](/providers/ai-sdk-providers/openai#embedding-models)                             | `text-embedding-3-medium`        | 2048                 |
| [Hugging Face](/providers/ai-sdk-providers/hugging-face#embedding-models)                  | `sentence-transformers/all

# Modelos de Inmersión
| Proveedor | Modelo | Dimensiones |
| --- | --- | --- |
| [Google Generative AI](/providers/ai-sdk-providers/google-generative-ai#modelos-de-inmersión) | `text-embedding-004` | 768 |
| [Mistral](/providers/ai-sdk-providers/mistral#modelos-de-inmersión) | `mistral-embed` | 1024 |
| [Cohere](/providers/ai-sdk-providers/cohere

# Modelos de embebiendo
| [Cohere](/proveedores/sdk-ai-proveedores/cohere#modelos-de-embebiendo)                             | `embed-english-light-v3.0`      | 384                  |
| [Cohere](/proveedores/sdk-ai-proveedores/cohere#modelos-de-embebiendo)                             | `embed-multilingual-light-v3.0` | 384                  |
| [Cohere](/proveedores/sdk-ai-proveedores

# (Modelos de Inmersión)             | `amazon.titan-embed-text-v1`    | 1024                 |
| [Amazon Bedrock](/providers/ai-sdk-providers/amazon-bedrock#modelos-de-inmersión)             | `amazon.titan-embed-text-v2:0`  | 1024                 |

---
título: Generación de Imágenes
descripción: Aprende a generar imágenes con el SDK de Inteligencia Artificial.
---

# Generación de Imágenes

<Nota tipo="advertencia">La generación de imágenes es una característica experimental.</Nota>

El SDK de Inteligencia Artificial proporciona la función [`generateImage`](/docs/reference/ai-sdk-core/generate-image)
para generar imágenes basadas en una solicitud dada utilizando un modelo de imagen.

```tsx
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduciendo un Cadillac',
});
```

Puedes acceder a los datos de la imagen utilizando las propiedades `base64` o `uint8Array`:

```tsx
const base64 = image.base64; // datos de imagen en base64
const uint8Array = image.uint8Array; // Uint8Array de datos de imagen
```

## Configuración

### Tamaño y Relación de Aspecto

Según el modelo, puedes especificar el tamaño o la relación de aspecto.

##### Tamaño

El tamaño se especifica como una cadena en el formato `{ancho}x{alto}`.
Los modelos solo admiten unos pocos tamaños, y los tamaños admitidos son diferentes para cada modelo y proveedor.

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduciendo un Cadillac',
  size: '1024x1024',
});
```

##### Relación de aspecto

La relación de aspecto se especifica como una cadena en el formato `{ancho}:{alto}`.
Los modelos solo admiten unas pocas relaciones de aspecto, y las relaciones de aspecto admitidas son diferentes para cada modelo y proveedor.

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { vertex } from '@ai-sdk/google-vertex';

const { image } = await generateImage({
  model: vertex.image('imagen-3.0-generate-002'),
  prompt: 'Santa Claus conduciendo un Cadillac',
  aspectRatio: '16:9',
});
```

### Generación de Múltiples Imágenes

`generateImage` también admite la generación de múltiples imágenes al mismo tiempo:

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { images } = await generateImage({
  model: openai.image('dall-e-2'),
  prompt: 'Santa Claus driving a Cadillac',
  n: 4, // Número de imágenes a generar
});
```

<Nota>
  `generateImage` llamará automáticamente al modelo tantas veces como sea necesario (en paralelo) para generar el número de imágenes solicitadas.
</Nota>

Cada modelo de imagen tiene un límite interno sobre cuántas imágenes puede generar en una sola llamada a la API. El SDK de AI gestiona esto automáticamente al batchear las solicitudes de manera adecuada cuando solicites múltiples imágenes utilizando el parámetro `n`. Por defecto, el SDK utiliza los límites documentados por el proveedor (por ejemplo, DALL-E 3 solo puede generar 1 imagen por llamada, mientras que DALL-E 2 admite hasta 10).

Si es necesario, puedes sobrescribir este comportamiento utilizando la configuración `maxImagesPerCall` cuando configures tu modelo. Esto es especialmente útil cuando trabajas con modelos nuevos o personalizados donde el tamaño de la caché por defecto podría no ser óptimo:

```tsx
const model = openai.image('dall-e-2', {
  maxImagesPerCall: 5, // Sobrescribir el tamaño de la caché por defecto
});

const { images } = await generateImage({
  model,
  prompt: 'Santa Claus driving a Cadillac',
  n: 10, // Hacer 2 llamadas de 5 imágenes cada una
});
```

### Propor una Semilla

Puedes proporcionar una semilla a la función `generateImage` para controlar el resultado del proceso de generación de imágenes.
Si está soportado por el modelo, la misma semilla siempre producirá la misma imagen.

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduciendo un Cadillac',
  seed: 1234567890,
});
```

### Configuraciones específicas del proveedor

Los modelos de imágenes a menudo tienen configuraciones específicas del proveedor o incluso del modelo.
Puedes pasar tales configuraciones a la función `generateImage` utilizando el parámetro `providerOptions`.
Las opciones del proveedor (`openai` en el ejemplo a continuación) se convierten en propiedades del cuerpo de la solicitud.

```tsx highlight={"9"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduciendo un Cadillac',
  size: '1024x1024',
  providerOptions: {
    openai: { estilo: 'vivid', calidad: 'hd' },
  },
});
```

### Señales de Aborto y Tiempos de espera

`generateImage` acepta un parámetro `abortSignal` opcional de tipo [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
que puedes usar para abortar el proceso de generación de imágenes o establecer un tiempo de espera.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
  abortSignal: AbortSignal.timeout(1000), // Abortar después de 1 segundo
});
```

### Encabezados Personalizados

`generateImage` acepta un parámetro `headers` opcional de tipo `Record<string, string>`
que puedes usar para agregar encabezados personalizados a la solicitud de generación de imágenes.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  value: 'sunny day at the beach',
  headers: { 'X-Custom-Header': 'custom-value' },
});
```

### Advertencias

Si el modelo devuelve advertencias, por ejemplo, por parámetros no soportados, estarán disponibles en la propiedad `warnings` de la respuesta.

```tsx
const { image, warnings } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
});
```

### Manejo de Errores

Cuando `generateImage` no puede generar una imagen válida, lanza un error de tipo [`AI_NoImageGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-image-generated-error).

Este error ocurre cuando el proveedor de inteligencia artificial falla en generar una imagen. Puede surgir debido a las siguientes razones:

- El modelo falló en generar una respuesta
- El modelo generó una respuesta que no pudo ser parseada

El error preserva la siguiente información para ayudarlo a registrar el problema:

- `responses`: Información de metadatos sobre las respuestas del modelo de imagen, incluyendo el timestamp, el modelo y los encabezados.
- `cause`: La causa del error. Puede utilizar esto para un manejo de errores más detallado

```typescript
import { generateImage, NoImageGeneratedError } from 'ai';

try {
  await generateImage({ model, prompt });
} catch (error) {
  if (NoImageGeneratedError.isInstance(error)) {
    console.log('NoImageGeneratedError');
    console.log('Causa:', error.cause);
    console.log('Respuestas:', error.responses);
  }
}
```

## Generación de Imágenes con Modelos de Lenguaje

Algunos modelos de lenguaje, como Google `gemini-2.0-flash-exp`, admiten salidas multi-modales, incluyendo imágenes.
Con tales modelos, puedes acceder a las imágenes generadas utilizando la propiedad `files` de la respuesta.

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const result = await generateText({
  model: google('gemini-2.0-flash-exp'),
  providerOptions: {
    google: { responseModalities: ['TEXTO', 'IMAGEN'] },
  },
  prompt: 'Genera una imagen de un gato cómico',
});

for (const file of result.files) {
  if (file.mimeType.startsWith('image/')) {
    // El objeto de archivo proporciona múltiples formatos de datos:
    // Accede a las imágenes como cadena de base64, Uint8Array de datos binarios o comprueba el tipo
    // - file.base64: string (formato de URL de datos)
    // - file.uint8Array: Uint8Array (datos binarios)
    // - file.mimeType: string (por ejemplo, "image/png")
  }
}
```

## Modelos de Imágenes

| Proveedor                                                                  | Modelo                                                        | Soporte de tamaños (`ancho x alto`) o ratios de aspecto (`ancho : alto`)                                                                                                |
| ------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [xAI Grok](/providers/ai-sdk-providers/xai-grok)                          | [xAI Grok Model](/models/ai-sdk-models/xai-grok)            

# modelos-de-imágenes)
                  | `grok-2-image`                                               | 1024x768 (por defecto)                                                                                                                                                  |
| [OpenAI](/proveedores/sdk-de-ai-proveedores/openai#modelos-de-imágenes)

# modelos-de-imágenes
| `dall-e-3`                                                   | 1024x1024, 1792x1024, 1024x1792                                                                                                                                     |
| [OpenAI](/providers/ai-sdk-providers/openai#modelos-de-imágenes)

# modelos-de-imagenes) | `amazon.nova-canvas-v1:0`                                    | 320-4096 (multiplos de 16), 1:4 a 4:1, max 4.2M pixeles                                                                                                             |
| [Fal](/providers/ai-sdk-providers/fal#modelos-de-imagenes)                       | `fal-ai/flux/dev`                                            | 1

# modelos-de-imagenes)                       | `fal-ai/flux-lora`                                           | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Fal](/proveedores/sdk-ai-proveedores/fal#modelos-de-imagenes)                      

# modelos-de-imágenes
| [Fal](/proveedores/sdk-de-inteligencia-artificial/fal#modelos-de-imágenes) | `fal-ai/flux-pro/v1.1-ultra`                                 | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                

# modelos-de-imagenes)                       | `fal-ai/recraft-v3`                                          | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Fal](/proveedores/sdk-de-ia/fal#modelos-de-imagenes)                       | `

# modelos-de-imagenes
| `fal-ai/hyper-sdxl`                                          | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [DeepInfra](/providers/ai-sdk-providers/deepinfra#modelos-de-imagenes)           | `stabilityai

# modelos-de-imagenes
| `black-forest-labs/FLUX-1.1-pro`                             | 256-1440 (multiplos de 32)                                                                                                                                          |
| [DeepInfra](/providers/ai-sdk-providers/deepinfra#modelos-de-imagenes

# modelos-de-imagenes
| `black-forest-labs/FLUX-1-dev`                               | 256-1440 (multiplos de 32)                                                                                                                                          |
| [DeepInfra](/providers/ai-sdk-providers/deepinfra#modelos-de-imagenes)          

# modelos-de-imagenes)           | `stabilityai/sd3.5-medium`                                   | 1:1, 16:9, 1:9, 3:2, 2:3, 

# modelos-de-imagenes)           | `stabilityai/sdxl-turbo`                                     | 1:1, 16:9, 1:9, 3:2, 2:3, 4:5, 5:4, 9:16, 9:21                                                                                                                      |
| [Replicar](/proveedores/sdk-ai/replicate)                        |

| [Replicar](/providers/ai-sdk-providers/replicate)                        | `recraft-ai/recraft-v3`                                      | 1024x1024, 1365x1024, 1024x1365, 1536x1024, 1024x1536, 1820x1024

# modelos-de-imagenes)   | `imagen-3.0-generate-002`                                    | 1:1, 3:4, 4:3, 9:16, 16:9                                                                                                                                           |
| [Google Vertex](/providers/ai-sdk-providers/google-vertex#modelos-de-imagenes)

# modelos-de-imágenes)           | `accounts/fireworks/models/flux-1-dev-fp8`                   | 1:1, 2:3, 3:2, 4:5, 5:4, 16:9, 9:16, 9:21, 21:9                                                                                                                     |
| [Fireworks](/providers/ai-sdk-providers/fireworks#modelos-de-imágenes)          

# modelos-de-imágenes)
           | `accounts/fireworks/models/playground-v2-5-1024px-aesthetic` | 640x1536, 768x1344, 832x1216, 896x1152, 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640                                                                           |
| [Fireworks](/providers/ai-sdk

# modelos-de-imágenes
| [Fireworks](/proveedores/sdk-ai-proveedores/fireworks#modelos-de-imágenes)           | `cuentas/fireworks/modelos/playground-v2-1024px-aestético`   | 640x1536, 768x1344, 832x1216, 896x1152, 1024x1024, 1152x896, 1216

# modelos-de-imagenes
| `accounts/fireworks/models/stable-diffusion-xl-1024-v1-0`    | 640x1536, 768x1344, 832x1216, 896x1152, 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640                                                                           |
| [

# modelos-de-imagenes)                     | `photon-flash-1`                                             | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Together.ai](/providers/ai-sdk-providers/together

# modelos-de-imagenes)
        | `black-forest-labs/FLUX.1-dev`                               | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/together

# modelos-de-imágenes)
        | `black-forest-labs/FLUX.1-schnell`                           | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/to

# modelos-de-imagenes
| `black-forest-labs/FLUX.1-depth`                             | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/togetherai

# modelos-de-imágenes)
        | `black-forest-labs/FLUX.1.1-pro`                             | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/to

# modelos-de-imágenes)
        | `black-forest-labs/FLUX.1-schnell-Free`                      | 512x512, 768x768, 1024x1024                                                                                                                                         |

A continuación, se muestra un pequeño conjunto de modelos de imágenes admitidos por los proveedores de SDK de IA. Para obtener más información, consulte la documentación del proveedor correspondiente.

---
title: Transcripción
description: Aprenda a transcribir audio con el SDK de IA.
---

# Transcripción

<Nota tipo="advertencia">La transcripción es una función experimental.</Nota>

El SDK de IA proporciona la función `transcribe` para transcribir audio utilizando un modelo de transcripción.

```ts
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  modelo: openai.transcripcion('whisper-1'),
  audio: await readFile('audio.mp3'),
});
```

La propiedad `audio` puede ser un `Uint8Array`, `ArrayBuffer`, `Buffer`, `string` (datos de audio base64 codificados) o una `URL`.

Para acceder al transcripto generado:

```ts
const texto = transcript.text; // texto del transcripto e.g. "Hola, mundo!"
const segmentos = transcript.segmentos; // array de segmentos con tiempos de inicio y fin, si están disponibles
const idioma = transcript.idioma; // idioma del transcripto e.g. "es", si está disponible
const duracionEnSegundos = transcript.duracionEnSegundos; // duración del transcripto en segundos, si está disponible
```

## Configuración

### Configuración específica del proveedor

Los modelos de transcripción a menudo tienen configuraciones específicas del proveedor o modelo que se pueden establecer utilizando el parámetro `providerOptions`.

```ts highlight="8-12"
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  modelo: openai.transcripcion('whisper-1'),
  audio: await readFile('audio.mp3'),
  providerOptions: {
    openai: {
      timestampGranularidades: ['palabra'],
    },
  },
});
```

### Señales de Aborto y Tiempos de Espera

`transcribe` acepta un parámetro `abortSignal` opcional de tipo [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
que puedes utilizar para abortar el proceso de transcripción o establecer un tiempo de espera.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_transcribe as transcribe } from 'ai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
  abortSignal: AbortSignal.timeout(1000), // Abortar después de 1 segundo
});
```

### Encabezados Personalizados

`transcribe` acepta un parámetro `headers` opcional de tipo `Record<string, string>`
que puedes utilizar para agregar encabezados personalizados a la solicitud de transcripción.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_transcribe as transcribe } from 'ai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
  headers: { 'X-Custom-Header': 'custom-value' },
});
```

### Advertencias

Las advertencias (por ejemplo, parámetros no soportados) están disponibles en la propiedad `warnings`.

```ts
import { openai } from '@ai-sdk/openai';
import { experimental_transcribe as transcribe } from 'ai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
});

const warnings = transcript.warnings;
```

### Manejo de Errores

Cuando `transcribe` no puede generar un transcripto válido, lanza un error de tipo [`AI_NoTranscriptGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-transcript-generated-error).

Este error puede surgir por cualquiera de las siguientes razones:

- El modelo falló en generar una respuesta
- El modelo generó una respuesta que no pudo ser parseada

El error conserva la siguiente información para ayudarte a registrar el problema:

- `responses`: Información sobre los metadatos de las respuestas del modelo de transcripción, incluyendo el timestamp, el modelo y los encabezados.
- `cause`: La causa del error. Puedes utilizar esto para un manejo de errores más detallado.

```ts
import {
  experimental_transcribe as transcribe,
  NoTranscriptGeneratedError,
} from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

try {
  await transcribe({
    model: openai.transcription('whisper-1'),
    audio: await readFile('audio.mp3'),
  });
} catch (error) {
  if (NoTranscriptGeneratedError.isInstance(error)) {
    console.log('NoTranscriptGeneratedError');
    console.log('Causa:', error.cause);
    console.log('Respuestas:', error.responses);
  }
}
```

## Modelos de Transcripción

| Proveedor                                                                 | Modelo                        |
| ------------------------------------------------------------------------- | ---------------------------- |
| [OpenAI](/providers/ai-sdk-providers/openai)

# modelos-de-transcripción
| [OpenAI](/proveedores/sdk-ai-proveedores/openai#modelos-de-transcripción) | `gpt-4o-transcribe`          |
| [OpenAI](/proveedores/sdk-ai-proveedores/openai#modelos-de-transcripción) | `gpt-4o-mini-transcribe`     |
| [ElevenLabs](/proveedores/sdk-ai-proveedores/elevenlabs#modelos-de-transcripción) | `scribe_v1`                  |
| [ElevenLabs](/proveedores/sdk-ai-proveedores/elevenlabs#modelos-de-transcripción)

# modelos-de-transcripción)    | `gpt-4o-transcribe`          |
| [Azure OpenAI](/providers/ai-sdk-providers/azure#modelos-de-transcripción)    | `gpt-4o-mini-transcribe`     |
| [Rev.ai](/providers/ai-sdk-providers/revai#modelos-de-transcripción)          | `machine`                    |
| [Rev.ai](/providers/ai-sdk-providers/revai#modelos-de-transcripción)          | `low_cost`                   |
| [Rev.ai](/providers/ai-sdk-providers/revai#modelos-de-transcripción)          | `fusion`                     |
| [Deepgram](/providers/ai-sdk-providers/deepgram#model

# modelos-de-transcripción)     | `nova-3` (+ variantes)        |
| [Gladia](/proveedores/sdk-ai-proveedores/gladia#modelos-de-transcripción)         | `default`                    |
| [AssemblyAI](/proveedores/sdk-ai-proveedores/assemblyai#modelos-de-transcripción) | `best`                       |
| [AssemblyAI](/proveedores/sdk-ai-proveedores/assemblyai#modelos-de-transcripción) | `nano`                       |
| [Fal](/proveedores/sdk-ai-proveedores/fal#modelos-de-transcripción)               | `whisper`                    |
| [Fal](/proveedores/sdk-ai-proveedores/fal#modelos-de-transcripción)               | `wizper`                     |

Arriba se muestran un pequeño conjunto de modelos de transcripción admitidos por los proveedores del SDK de IA. Para más

# Discurso

<Nota tipo="advertencia">Discurso es una característica experimental.</Nota>

El SDK de IA proporciona la función [`generateSpeech`](/docs/reference/ai-sdk-core/generate-speech)
para generar discurso a partir de texto utilizando un modelo de discurso.

```ts
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  modelo: openai.speech('tts-1'),
  texto: 'Hola, mundo!',
  voz: 'alloy',
});
```

Para acceder al audio generado:

```ts
const audio = audio.audioData; // datos de audio e.g. Uint8Array
```

## Configuración

### Configuración específica del proveedor

Puedes establecer configuraciones específicas del modelo con el parámetro `providerOptions`.

```ts highlight="8-12"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  modelo: openai.speech('tts-1'),
  texto: 'Hola, mundo!',
  providerOptions: {
    openai: {
      // ...
    },
  },
});
```

### Señales de Aborto y Tiempos de espera

`generateSpeech` acepta un parámetro `abortSignal` opcional de tipo [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
que puedes utilizar para abortar el proceso de generación de habla o establecer un tiempo de espera.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Hola, mundo!',
  abortSignal: AbortSignal.timeout(1000), // Abortar después de 1 segundo
});
```

### Encabezados personalizados

`generateSpeech` acepta un parámetro `headers` opcional de tipo `Record<string, string>`
que puedes utilizar para agregar encabezados personalizados a la solicitud de generación de habla.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Hola, mundo!',
  headers: { 'X-Encabezado-Custom': 'valor-custom' },
});
```

### Advertencias

Las advertencias (por ejemplo, parámetros no soportados) están disponibles en la propiedad `warnings`.

```ts
import { openai } from '@ai-sdk/openai';
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Hola, mundo!',
});

const advertencias = audio.warnings;
```

### Manejo de Errores

Cuando `generateSpeech` no puede generar un audio válido, lanza una excepción de tipo [`AI_NoAudioGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-audio-generated-error).

Este error puede surgir por cualquiera de las siguientes razones:

- El modelo falló en generar una respuesta
- El modelo generó una respuesta que no pudo ser parseada

La excepción preserva la siguiente información para ayudarte a registrar el problema:

- `responses`: Metadatos sobre las respuestas del modelo de habla, incluyendo el timestamp, el modelo y los encabezados.
- `cause`: La causa del error. Puedes utilizar esto para un manejo de errores más detallado.

```ts
import {
  experimental_generateSpeech as generateSpeech,
  AI_NoAudioGeneratedError,
} from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

try {
  await generateSpeech({
    model: openai.speech('tts-1'),
    text: 'Hola, mundo!',
  });
} catch (error) {
  if (AI_NoAudioGeneratedError.isInstance(error)) {
    console.log('AI_NoAudioGeneratedError');
    console.log('Causa:', error.cause);
    console.log('Respuestas:', error.responses);
  }
}
```

## Modelos de Habla

| Proveedor                                                  | Modelo             |
| ---------------------------------------------------------- | ----------------- |
| [OpenAI](/providers/ai-sdk-providers/openai#modelos-de-habla) | `tts-1`           |
| [OpenAI](/providers/ai-sdk-providers/openai

# (Modelos-de-habla) | `tts-1-hd`        |
| [OpenAI](/proveedores/sdk-de-ia/openai#modelos-de-habla) | `gpt-4o-mini-tts` |
| [LMNT](/proveedores/sdk-de-ia/lmnt#modelos-de-habla)     | `aurora`          |
| [LMNT](/proveedores/sdk-de-ia/lmnt#modelos-de-habla)     | `blizzard`        |
| [Hume](/proveedores/sdk-de-ia/hume#modelos-de-habla)     | `default`         |

Arriba se muestran un pequeño conjunto de los modelos de habla soportados por los proveedores del SDK de IA. Para más información, consulte la documentación del proveedor correspondiente.

---
titulo: Middleware de Modelo de Lenguaje
descripcion: Aprende a utilizar middleware para mejorar el comportamiento de los modelos de lenguaje
---

# Middleware de Modelo de Lenguaje

El middleware de modelo de lenguaje es una forma de mejorar el comportamiento de los modelos de lenguaje
interceptando y modificando las llamadas a los modelos de lenguaje.

Puede usarse para agregar características como guardrails, RAG, caché y registro
de manera independiente de los modelos de lenguaje. Tales middleware pueden desarrollarse y distribuirse de manera independiente de los modelos de lenguaje a los que se aplican.

## Utilizando Middleware de Modelo de Lenguaje

Puede utilizar middleware de modelo de lenguaje con la función `wrapLanguageModel`. 
Esta función toma un modelo de lenguaje y un middleware de modelo de lenguaje y devuelve un nuevo
modelo de lenguaje que incorpora el middleware.

```ts
import { wrapLanguageModel } from 'ai';

const modeloDeLenguajeAgrupado = wrapLanguageModel({
  model: suModelo,
  middleware: suMiddlewareDeModeloDeLenguaje,
});
```

El modelo de lenguaje agrupado se puede utilizar de la misma manera que cualquier otro modelo de lenguaje, por ejemplo, en `streamText`:

```ts highlight="2"
const resultado = streamText({
  model: modeloDeLenguajeAgrupado,
  prompt: '¿Cuáles son las ciudades de los Estados Unidos?',
});
```

## Multiple middlewares

Puedes proporcionar múltiples middlewares a la función `wrapLanguageModel`.
Los middlewares se aplicarán en el orden en que se proporcionan.

```ts
const wrappedLanguageModel = wrapLanguageModel({
  model: tuModelo,
  middleware: [primerMiddleware, segundoMiddleware],
});

// aplicado como: primerMiddleware(segundoMiddleware(tuModelo))
```

## Middleware integrado

La SDK de IA viene con varios middlewares integrados que puedes utilizar para configurar modelos de lenguaje:

- `extractReasoningMiddleware`: Extrae información de razonamiento de los textos generados y la expone como una propiedad `reasoning` en el resultado.
- `simulateStreamingMiddleware`: Simula el comportamiento de streaming con respuestas de modelos de lenguaje no de streaming.
- `defaultSettingsMiddleware`: Aplica configuraciones predeterminadas a un modelo de lenguaje.

### Extraer razonamiento

Algunos proveedores y modelos expenden información de razonamiento en los textos generados utilizando etiquetas especiales,
e.g. &lt;think&gt; y &lt;/think&gt;.

La función `extractReasoningMiddleware` se puede utilizar para extraer esta información de razonamiento y exponerla como una propiedad `reasoning` en el resultado.

```ts
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: tuModelo,
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Puedes utilizar ese modelo mejorado en funciones como `generateText` y `streamText`.

La función `extractReasoningMiddleware` también incluye una opción `startWithReasoning`.
Cuando se establece en `true`, la etiqueta de razonamiento se agregará al principio del texto generado.
Esto es útil para modelos que no incluyen la etiqueta de razonamiento al principio de la respuesta.
Para obtener más detalles, consulta la [Guía de DeepSeek R1](/docs/guides/r1#deepseek-r1-middleware).

### Simular Streaming

La función `simulateStreamingMiddleware` se puede utilizar para simular el comportamiento de streaming con respuestas de modelos de lenguaje que no proporcionan streaming.
Esto es útil cuando deseas mantener una interfaz de streaming consistente incluso cuando se utilizan modelos que solo proporcionan respuestas completas.

```ts
import { wrapLanguageModel, simulateStreamingMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: tuModelo,
  middleware: simulateStreamingMiddleware(),
});
```

### Configuraciones Predeterminadas

La función `defaultSettingsMiddleware` se puede utilizar para aplicar configuraciones predeterminadas a un modelo de lenguaje.

```ts
import { wrapLanguageModel, defaultSettingsMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: tuModelo,
  middleware: defaultSettingsMiddleware({
    settings: {
      temperatura: 0.5,
      maxTokens: 800,
      // nota: utiliza providerMetadata en lugar de providerOptions aquí:
      providerMetadata: { openai: { store: false } },
    },
  }),
});
```

## Implementando Middleware de Modelo de Lenguaje

<Nota>
  Implementar middleware de modelo de lenguaje es una función avanzada que requiere
  una sólida comprensión de la [especificación del modelo de lenguaje](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
</Nota>

Puedes implementar cualquiera de las siguientes tres funciones para modificar el comportamiento del modelo de lenguaje:

1. `transformParams`: Transforma los parámetros antes de que se pasen al modelo de lenguaje, tanto para `doGenerate` como para `doStream`.
2. `wrapGenerate`: Envuelve el método `doGenerate` del [modelo de lenguaje](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
   Puedes modificar los parámetros, llamar al modelo de lenguaje y modificar el resultado.
3. `wrapStream`: Envuelve el método `doStream` del [modelo de lenguaje](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
   Puedes modificar los parámetros, llamar al modelo de lenguaje y modificar el resultado.

Aquí hay algunos ejemplos de cómo implementar middleware de modelo de lenguaje:

## Ejemplos

<Nota>
  Estos ejemplos no están destinados a usarse en producción. Solo se muestran
  cómo puedes usar middleware para mejorar el comportamiento de los modelos de lenguaje.
</Nota>

### Inicio de Sesión

Este ejemplo muestra cómo loguear los parámetros y el texto generado de una llamada a un modelo de lenguaje.

```ts
import type { LanguageModelV1Middleware, LanguageModelV1StreamPart } from 'ai';

export const tuMiddlewareDeLog: LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    console.log('doGenerate llamado');
    console.log(`parámetros: ${JSON.stringify(params, null, 2)}`);

    const resultado = await doGenerate();

    console.log('doGenerate finalizado');
    console.log(`texto generado: ${resultado.text}`);

    return resultado;
  },

  wrapStream: async ({ doStream, params }) => {
    console.log('doStream llamado');
    console.log(`parámetros: ${JSON.stringify(params, null, 2)}`);

    const { stream, ...rest } = await doStream();

    let textoGenerado = '';

    const transformStream = new TransformStream<
      LanguageModelV1StreamPart,
      LanguageModelV1StreamPart
    >({
      transform(chunk, controller) {
        if (chunk.type === 'text-delta') {
          textoGenerado += chunk.textDelta;
        }

        controller.enqueue(chunk);
      },

      flush() {
        console.log('doStream finalizado');
        console.log(`texto generado: ${textoGenerado}`);
      },
    });

    return {
      stream: stream.pipeThrough(transformStream),
      ...rest,
    };
  },
};
```

### Caching

Este ejemplo muestra cómo construir un caché simple para el texto generado de una llamada al modelo de lenguaje.

```ts
import type { LanguageModelV1Middleware } from 'ai';

const cache = new Map<string, any>();

export const suMiddlewareDeCaching: LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    const claveDeCaching = JSON.stringify(params);

    if (cache.has(claveDeCaching)) {
      return cache.get(claveDeCaching);
    }

    const resultado = await doGenerate();

    cache.set(claveDeCaching, resultado);

    return resultado;
  },

  // aquí implementarías la lógica de caché para streaming
};
```

### Generación Augmentada de Recuperación (RAG)

Este ejemplo muestra cómo utilizar RAG como middleware.

<Nota>
  Las funciones auxiliares como `getLastUserMessageText` y `findSources` no forman parte de la SDK de AI. Se utilizan en este ejemplo para ilustrar el concepto de RAG.
</Nota>

```ts
import type { LanguageModelV1Middleware } from 'ai';

export const suMiddlewareDeRag: LanguageModelV1Middleware = {
  transformParams: async ({ params }) => {
    const textoDelUltimoMensajeDelUsuario = getLastUserMessageText({
      prompt: params.prompt,
    });

    if (textoDelUltimoMensajeDelUsuario == null) {
      return params; // no utilizar RAG (enviar parámetros sin modificar)
    }

    const instrucción =
      'Utilice la siguiente información para responder a la pregunta:\n' +
      findSources({ text: textoDelUltimoMensajeDelUsuario })
        .map(chunk => JSON.stringify(chunk))
        .join('\n');

    return addToLastUserMessage({ params, text: instrucción });
  },
};
```

### Guardrails

Los guardabarros son una forma de asegurarse de que el texto generado de una llamada a un modelo de lenguaje sea seguro y apropiado. Este ejemplo muestra cómo utilizar guardabarros como middleware.

```ts
import type { LanguageModelV1Middleware } from 'ai';

export const suGuardrailMiddleware: LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate }) => {
    const { texto, ...rest } = await doGenerate();

    // enfoque de filtrado, por ejemplo, para información personal sensible (PII) o información sensible:
    const textoLimpiado = texto?.replace(/palabraofensiva/g, '<REDACTED>');

    return { texto: textoLimpiado, ...rest };
  },

  // aquí implementarías la lógica del guardabarros para streaming
  // Nota: los guardabarros de streaming son difíciles de implementar, porque
  // no sabes el contenido completo del flujo hasta que se ha terminado.
};
```

## Configurando Metadatos Personalizados por Solicitud

Para enviar y acceder a metadatos personalizados en Middleware, puedes utilizar `providerOptions`. Esto es útil cuando estás construyendo middleware de registro donde deseas pasar contexto adicional como IDs de usuarios, fechas y horas, o otros datos de contexto que pueden ayudar con el seguimiento y depuración.

```ts
import { openai } from '@ai-sdk/openai';
import { generateText, wrapLanguageModel, LanguageModelV1Middleware } from 'ai';

export const tuMiddlewareDeRegistro: LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    console.log('METADATOS', params?.providerMetadata?.tuMiddlewareDeRegistro);
    const resultado = await doGenerate();
    return resultado;
  },
};

const { texto } = await generateText({
  modelo: wrapLanguageModel({
    modelo: openai('gpt-4o'),
    middleware: tuMiddlewareDeRegistro,
  }),
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  providerOptions: {
    tuMiddlewareDeRegistro: {
      hello: 'mundo',
    },
  },
});

console.log(texto);
```

---
title: Gestión de Proveedores y Modelos
description: Aprende a trabajar con múltiples proveedores y modelos
---

# Gestión de Proveedores y Modelos

Cuando trabajas con múltiples proveedores y modelos, a menudo es deseable gestionarlos en un lugar central y acceder a los modelos a través de simples identificadores de cadena.

El SDK de IA ofrece [proveedores personalizados](/docs/reference/ai-sdk-core/proveedor-personalizado) y
un [registro de proveedores](/docs/reference/ai-sdk-core/registro-de-proveedores) para este propósito:

- Con **proveedores personalizados**, puedes configurar previamente las configuraciones de modelo, proporcionar alias de nombres de modelo,
  y limitar los modelos disponibles.
- El **registro de proveedores** te permite combinar múltiples proveedores y acceder a ellos a través de simples identificadores de cadena.

Puedes combinar y mezclar proveedores personalizados, el registro de proveedores y [middleware](/docs/ai-sdk-core/middleware) en tu aplicación.

## Proveedores Personalizados

Puedes crear un [proveedor personalizado](/docs/reference/ai-sdk-core/proveedor-personalizado) utilizando `customProvider`.

### Ejemplo: configuraciones de modelo personalizadas

Puedes querer sobreescribir las configuraciones de modelo predeterminadas para un proveedor o proporcionar alias de nombres de modelo
con configuraciones preconfiguradas.

```ts
import { openai as originalOpenAI } from '@ai-sdk/openai';
import { customProvider } from 'ai';

// proveedor personalizado con configuraciones de modelo diferentes:
export const openai = customProvider({
  languageModels: {
    // modelo de reemplazo con configuraciones personalizadas:
    'gpt-4o': originalOpenAI('gpt-4o', { estructurasDeSalida: true }),
    // alias de modelo con configuraciones personalizadas:
    'gpt-4o-mini-estructurado': originalOpenAI('gpt-4o-mini', {
      estructurasDeSalida: true,
    }),
  },
  fallbackProvider: originalOpenAI,
});
```

### Ejemplo: nombre de modelo alias

También puedes proporcionar nombres de modelos alias, para que puedas actualizar la versión del modelo en un solo lugar en el futuro:

```ts
import { anthropic as originalAnthropic } from '@ai-sdk/anthropic';
import { customProvider } from 'ai';

// proveedor personalizado con nombres de alias:
export const anthropic = customProvider({
  languageModels: {
    opus: originalAnthropic('claude-3-opus-20240229'),
    sonnet: originalAnthropic('claude-3-5-sonnet-20240620'),
    haiku: originalAnthropic('claude-3-haiku-20240307'),
  },
  fallbackProvider: originalAnthropic,
});
```

### Ejemplo: limitar modelos disponibles

Puedes limitar los modelos disponibles en el sistema, incluso si tienes múltiples proveedores.

```ts
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';
import { customProvider } from 'ai';

export const myProvider = customProvider({
  languageModels: {
    'text-medium': anthropic('claude-3-5-sonnet-20240620'),
    'text-small': openai('gpt-4o-mini'),
    'structure-medium': openai('gpt-4o', { structuredOutputs: true }),
    'structure-fast': openai('gpt-4o-mini', { structuredOutputs: true }),
  },
  embeddingModels: {
    emdedding: openai.textEmbeddingModel('text-embedding-3-small'),
  },
  // no proveedor de fallback
});
```

## Registro de Proveedores

Puedes crear un [registro de proveedores](/docs/reference/ai-sdk-core/provider-registry) con múltiples proveedores y modelos utilizando `createProviderRegistry`.

### Configuración

```ts filename={"registro.ts"}
import { anthropic } desde '@ai-sdk/anthropic';
import { crearOpenAI } desde '@ai-sdk/openai';
import { crearRegistroProveedor } desde 'ai';

export const registro = crearRegistroProveedor({
  // registrar proveedor con prefijo y configuración por defecto:
  anthropic,

  // registrar proveedor con prefijo y configuración personalizada:
  openai: crearOpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  }),
});
```

### Configuración con Separador Personalizado

Por defecto, el registro utiliza `:` como separador entre el ID del proveedor y el ID del modelo. Puede personalizar este separador:

```ts filename={"registro.ts"}
import { anthropic } desde '@ai-sdk/anthropic';
import { openai } desde '@ai-sdk/openai';

export const registroConSeparadorPersonalizado = crearRegistroProveedor(
  {
    anthropic,
    openai,
  },
  { separador: ' > ' },
);
```

### Ejemplo: Utilizar modelos de lenguaje

Puede acceder a modelos de lenguaje utilizando el método `languageModel` en el registro.
El ID del proveedor se convertirá en el prefijo del ID del modelo: `providerId:modelId`.

```ts highlight={"5"}
import { generarTexto } desde 'ai';
import { registro } desde './registro';

const { texto } = await generarTexto({
  modelo: registro.languageModel('openai:gpt-4-turbo'), // separador por defecto
  // o con separador personalizado:
  // modelo: registroConSeparadorPersonalizado.languageModel('openai > gpt-4-turbo'),
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
});
```

### Ejemplo: Utilizar modelos de embeddings de texto

Puedes acceder a los modelos de embeddings de texto utilizando el método `textEmbeddingModel` en el registro.
El id del proveedor se convertirá en el prefijo del id del modelo: `providerId:modelId`.

```ts highlight={"5"}
import { embed } from 'ai';
import { registry } from './registry';

const { embedding } = await embed({
  model: registry.textEmbeddingModel('openai:text-embedding-3-small'),
  value: 'día soleado en la playa',
});
```

### Ejemplo: Utilizar modelos de imágenes

Puedes acceder a los modelos de imágenes utilizando el método `imageModel` en el registro.
El id del proveedor se convertirá en el prefijo del id del modelo: `providerId:modelId`.

```ts highlight={"5"}
import { generateImage } from 'ai';
import { registry } from './registry';

const { image } = await generateImage({
  model: registry.imageModel('openai:dall-e-3'),
  prompt: 'Un atardecer hermoso sobre un océano calmado',
});
```

## Combinando Proveedores Personalizados, Registro de Proveedores y Middleware

La idea central de la gestión de proveedores es configurar un archivo que contenga todos los proveedores y modelos que desee utilizar.
Puede desear configurar previamente las opciones de modelo, proporcionar alias de nombres de modelo, limitar los modelos disponibles, y más.

A continuación, se muestra un ejemplo que implementa los siguientes conceptos:

- pasar por un proveedor completo con un prefijo de espacio de nombres (aquí: `xai > *`)
- configurar un proveedor compatible con OpenAI con una clave API personalizada y una URL base (aquí: `custom > *`)
- configurar alias de nombres de modelo (aquí: `anthropic > rápido`, `anthropic > escritura`, `anthropic > razonamiento`)
- configurar previamente las opciones de modelo (aquí: `anthropic > razonamiento`)
- validar las opciones de proveedor específicas (aquí: `AnthropicProviderOptions`)
- utilizar un proveedor de fallback (aquí: `anthropic > *`)
- limitar un proveedor a ciertos modelos sin un fallback (aquí: `groq > gemma2-9b-it`, `groq > qwen-qwq-32b`)
- definir un separador personalizado para el registro de proveedores (aquí: `>`)

```ts
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { xai } from '@ai-sdk/xai';
import { groq } from '@ai-sdk/groq';
import {
  createProviderRegistry,
  customProvider,
  defaultSettingsMiddleware,
  wrapLanguageModel,
} from 'ai';

export const registry = createProviderRegistry(
  {
    // pasar por un proveedor completo con un prefijo de espacio de nombres
    xai,

    // acceder a un proveedor compatible con OpenAI con configuración personalizada
    custom: createOpenAICompatible({
      name: 'nombre-del-proveedor',
      apiKey: process.env.CUSTOM_API_KEY,
      baseURL: 'https://api.custom.com/v1',
    }),
```

// configuración de alias para el nombre del modelo
    anthropic: customProvider({
      languageModels: {
        rápido: customProvider({
          languageModels: {
            fast: anthropic('claude-3-haiku-20240307'),

            // modelo simple
            escritura: anthropic('claude-3-7-sonnet-20250219'),

            // configuración del modelo de razonamiento extendido:
            razonamiento: wrapLanguageModel({
              model: anthropic('claude-3-7-sonnet-20250219'),
              middleware: defaultSettingsMiddleware({
                settings: {
                  maxTokens: 100000, // configuración de ejemplo predeterminada
                  providerMetadata: {
                    anthropic: {
                      pensamiento: {
                        type: 'habilitado',


### Limitar un proveedor a ciertos modelos sin un fallback

    groq: customProvider({
      languageModels: {
        'gemma2-9b-it': groq('gemma2-9b-it'),
        'qwen-qwq-32b': groq('qwen-qwq-32b'),
      },
    }),
  },
  { separator: ' > ' },
);

### Uso:

```javascript
const model = registry.languageModel('anthropic > reasoning');
```

---
titulo: Manejo de Errores
descripcion: Aprende a manejar errores en el SDK de Inteligencia Artificial Core
---

# Manejo de Errores

## Manejo de errores regulares

Los errores regulares se lanzan y se pueden manejar utilizando el bloque `try/catch`.

```ts highlight="3,8-10"
import { generarTexto } from 'ai';

try {
  const { texto } = await generarTexto({
    modelo: tuModelo,
    prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
  });
} catch (error) {
  // manejar error
}
```

Consulte [Tipos de Errores](/docs/reference/ai-sdk-errors) para obtener más información sobre los diferentes tipos de errores que pueden ser lanzados.

## Manejo de errores de streaming (streams simples)

Cuando ocurren errores durante los streams que no admiten chunks de error,
el error se lanza como un error regular.
Puedes manejar estos errores utilizando el bloque `try/catch`.

```ts highlight="3,12-14"
import { generarTexto } from 'ai';

try {
  const { flujoDeTexto } = flujoDeTexto({
    modelo: tuModelo,
    prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
  });

  for await (const parteDeTexto of flujoDeTexto) {
    process.stdout.write(parteDeTexto);
  }
} catch (error) {
  // manejar error
}
```

## Manejo de errores de streaming (streaming con `error` soporte)

Los flujos de datos completos admiten partes de error.
Puedes manejar esas partes de manera similar a otras partes.
Se recomienda agregar también un bloque try-catch para errores que ocurren fuera del streaming.

```ts highlight="13-17"
import { generateText } from 'ai';

try {
  const { fullStream } = streamText({
    model: yourModel,
    prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
  });

  for await (const part of fullStream) {
    switch (part.type) {
      // ... maneja otros tipos de partes

      case 'error': {
        const error = part.error;
        // maneja error
        break;
      }
    }
  }
} catch (error) {
  // maneja error
}
```

---
titulo: Pruebas
descripcion: Aprende a usar los proveedores de pruebas de AI SDK Core para realizar pruebas.

# Pruebas

Pueden resultar desafiantes las pruebas de modelos de lenguaje, ya que son no deterministas y llamarlos es lento y costoso.

Para permitirte probar unitariamente tu código que utiliza la SDK de AI, el núcleo de la SDK de AI incluye proveedores de mockeo y ayudantes de prueba. Puedes importar los siguientes ayudantes de `ai/test`:

- `MockEmbeddingModelV1`: Un modelo de embeddings de mockeo utilizando la [especificación del modelo de embeddings v1](https://github.com/vercel/ai/blob/main/packages/provider/src/embedding-model/v1/embedding-model-v1.ts).
- `MockLanguageModelV1`: Un modelo de lenguaje de mockeo utilizando la [especificación del modelo de lenguaje v1](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
- `mockId`: Proporciona un ID de entero que aumenta.
- `mockValues`: Itera sobre un arreglo de valores con cada llamada. Devuelve el último valor cuando el arreglo se agota.
- [`simulateReadableStream`](/docs/reference/ai-sdk-core/simulate-readable-stream): Simula un flujo leible con retrasos.

Con proveedores de mockeo y ayudantes de prueba, puedes controlar la salida de la SDK de AI y probar tu código de manera repetible y determinista sin llamar realmente a un proveedor de modelo de lenguaje.

## Ejemplos

Puedes utilizar los ayudantes de prueba con las funciones de AI Core en tus pruebas unitarias:

### generateText

```ts
import { generateText } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';

const resultado = await generateText({
  model: new MockLanguageModelV1({
    doGenerate: async () => ({
      rawCall: { rawPrompt: null, rawSettings: {} },
      finishReason: 'stop',
      usage: { promptTokens: 10, completionTokens: 20 },
      text: `Hola, mundo!`,
    }),
  }),
  prompt: 'Hola, prueba!',
});
```

### streamText

```ts
import { streamText, simulateReadableStream } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';

const resultado = streamText({
  model: new MockLanguageModelV1({
    doStream: async () => ({
      stream: simulateReadableStream({
        chunks: [
          { type: 'text-delta', textDelta: 'Hola' },
          { type: 'text-delta', textDelta: ', ' },
          { type: 'text-delta', textDelta: `mundo!` },
          {
            type: 'finish',
            finishReason: 'stop',
            logprobs: undefined,
            usage: { completionTokens: 10, promptTokens: 3 },
          },
        ],
      }),
      rawCall: { rawPrompt: null, rawSettings: {} },
    }),
  }),
  prompt: 'Hola, prueba!',
});
```

### generarObjeto

```ts
import { generarObjeto } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';
import { z } from 'zod';

const resultado = await generarObjeto({
  modelo: new MockLanguageModelV1({
    modoGeneraciónObjetoPorDefecto: 'json',
    doGenerate: async () => ({
      llamadaBruta: { llamadaBrutaPrompt: null, llamadaBrutaConfiguración: {} },
      razónFinalización: 'stop',
      uso: { tokensPrompt: 10, tokensCompleción: 20 },
      texto: `{"content":"Hola, mundo!"}`,
    }),
  }),
  esquema: z.object({ contenido: z.string() }),
  sugerencia: 'Hola, prueba!',
});
```

### streamObject

```ts
import { streamObject, simulateReadableStream } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';
import { z } from 'zod';

const resultado = streamObject({
  modelo: new MockLanguageModelV1({
    modoDeGeneraciónPorDefecto: 'json',
    doStream: async () => ({
      stream: simulateReadableStream({
        chunks: [
          { type: 'text-delta', textDelta: '{ ' },
          { type: 'text-delta', textDelta: '"content": ' },
          { type: 'text-delta', textDelta: `"Hola, ` },
          { type: 'text-delta', textDelta: `mundo` },
          { type: 'text-delta', textDelta: `!"` },
          { type: 'text-delta', textDelta: ' }' },
          {
            type: 'finish',
            finishReason: 'stop',
            logprobs: undefined,
            usage: { completionTokens: 10, promptTokens: 3 },
          },
        ],
      }),
      rawCall: { rawPrompt: null, rawSettings: {} },
    }),
  }),
  schema: z.object({ contenido: z.string() }),
  prompt: 'Hola, test!',
});
```

### Simular Protocolo de Respuestas de Flujo de Datos

También se puede simular el [Protocolo de Flujo de Datos](/docs/ai-sdk-ui/stream-protocol)

# Protocolo de datos para respuestas de prueba, depuración o fines de demostración.

Aquí está un ejemplo de Next:

```ts filename="route.ts"
import { simulateReadableStream } from 'ai';

export async function POST(req: Request) {
  return new Response(
    simulateReadableStream({
      initialDelayInMs: 1000, // Retraso antes del primer chunk
      chunkDelayInMs: 300, // Retraso entre chunks
      chunks: [
        `0:"Esta"\n`,
        `0:" es un"\n`,
        `0:" ejemplo."\n`,
        `e:{"finishReason":"stop","usage":{"promptTokens":20,"completionTokens":50},"isContinued":false}\n`,
        `d:{"finishReason":"stop","usage":{"promptTokens":20,"completionTokens":50}}\n`,
      ],
    }).pipeThrough(new TextEncoderStream()),
    {
      status: 200,
      headers: {
        'X-Vercel-AI-Data-Stream': 'v1',
        'Content-Type': 'text/plain; charset=utf-8',
      },
    },
  );
}
```

---
titulo: Telemetría
descripcion: Utilizando OpenTelemetry con AI SDK Core
---

# Telemetría

<Nota tipo="advertencia">
  La telemetría de AI SDK es experimental y puede cambiar en el futuro.
</Nota>

El SDK de AI utiliza [OpenTelemetry](https://opentelemetry.io/) para recopilar datos de telemetría.
OpenTelemetry es un marco de observabilidad de código abierto diseñado para proporcionar instrumentación estandarizada para recopilar datos de telemetría.

Consulte las [integraciones de observabilidad de AI SDK](/providers/observability) para ver proveedores que ofrecen monitoreo y seguimiento para aplicaciones de AI SDK.

## Habilitando telemetría

Para aplicaciones de Next.js, por favor, siga el [guía de OpenTelemetry de Next.js](https://nextjs.org/docs/app/building-your-application/optimizing/open-telemetry) para habilitar la telemetría primero.

Puedes utilizar luego la opción `experimental_telemetry` para habilitar la telemetría en llamadas de función específicas mientras la característica es experimental:

```ts highlight="4"
const resultado = await generarTexto({
  modelo: openai('gpt-4-turbo'),
  prompt: 'Escribe un relato corto sobre un gato.',
  experimental_telemetry: { isEnabled: true },
});
```

Cuando la telemetría está habilitada, también puedes controlar si deseas grabar los valores de entrada y los valores de salida de la función.
Por defecto, ambos están habilitados. Puedes deshabilitarlos estableciendo las opciones `recordInputs` y `recordOutputs` en `false`.

Deshabilitar la grabación de entradas y salidas puede ser útil por razones de privacidad, transferencia de datos y rendimiento.
Puede querer deshabilitar la grabación de entradas si contienen información sensible.

## Metadatos de telemetría

Puedes proporcionar un `functionId` para identificar la función para la que los datos de telemetría son,
y `metadata` para incluir información adicional en los datos de telemetría.

```ts highlight="6-10"
const resultado = await generarTexto({
  modelo: openai('gpt-4-turbo'),
  prompt: 'Escribe un relato corto sobre un gato.',
  experimental_telemetry: {
    isEnabled: true,
    functionId: 'mi-función-impresionante',
    metadata: {
      algo: 'personalizado',
      otraCosa: 'otro-valor',
    },
  },
});
```

## Tracer Personalizado

Puede proporcionar un `tracer` que debe devolver un `Tracer` de OpenTelemetry. Esto es útil en situaciones en las que desea que sus trazas utilicen un `TracerProvider` distinto al proporcionado por el singleton `@opentelemetry/api`.

```ts highlight="7"
const tracerProvider = new NodeTracerProvider();
const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Escriba una historia corta sobre un gato.',
  experimental_telemetry: {
    isEnabled: true,
    tracer: tracerProvider.getTracer('ai'),
  },
});
```

## Datos Recopilados

### Función generateText

`generateText` registra 3 tipos de spans:

- `ai.generateText` (span): la longitud completa de la llamada a generateText. Contiene 1 o más spans `ai.generateText.doGenerate`.
  Contiene la [información básica del span del LLM](#información-básica-del-span-del-llm) y los siguientes atributos:

  - `operation.name`: `ai.generateText` y el functionId que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.generateText"`
  - `ai.prompt`: el prompt que se utilizó al llamar a `generateText`
  - `ai.response.text`: el texto que se generó
  - `ai.response.toolCalls`: las llamadas a herramientas que se realizaron como parte de la generación (JSON stringificado)
  - `ai.response.finishReason`: la razón por la que la generación terminó
  - `ai.settings.maxSteps`: el número máximo de pasos que se estableció

- `ai.generateText.doGenerate` (span): una llamada doGenerate del proveedor. Puede contener spans `ai.toolCall`.
  Contiene la [información de llamada del LLM](

# llam-span-información) y los siguientes atributos:

  - `operation.name`: `ai.generateText.doGenerate` y la funciónId que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.generateText.doGenerate"`
  - `ai.prompt.format`: el formato de la solicitud
  - `ai.prompt.messages`: las mensajes que se pasaron al proveedor
  - `ai.prompt.tools`: un array de definiciones de herramientas stringificadas. Las herramientas pueden ser de tipo `function` o `provider-defined`.
    Las herramientas de función tienen un `name`, `description` (opcional) y `parameters` (esquema JSON).
    Las herramientas definidas por el proveedor tienen un `name`, `id` y `args` (Registro).
  - `ai.prompt.toolChoice`: la configuración de herramienta stringificada (JSON). Tiene una propiedad `type` (`auto`, `none`, `required`, `tool`) y si el tipo es `tool`, una propiedad `toolName` con la herramienta específica.
  - `ai.response.text`: el texto que se generó
  - `ai.response.toolCalls`: las llamadas de herramienta que se realizaron como parte de la generación (stringificadas JSON)
  - `ai.response.finishReason`: la razón por la que la generación terminó

- `ai.toolCall` (span): una llamada de herramienta que se realiza como parte de la llamada generateText. Consulte [Llamadas de herramienta](#tool-call-spans) para obtener más detalles.

### función streamText

`streamText` registra 3 tipos de spans y 2 tipos de eventos:

- `ai.streamText` (span): la longitud completa de la llamada streamText. Contiene un `ai.streamText.doStream` span.
  Contiene la [información básica de span de LLM](

# Información de flujo de texto básico (LLM) y los siguientes atributos:

  - `operation.name`: `ai.streamText` y la funciónId que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.streamText"`
  - `ai.prompt`: la solicitud que se utilizó cuando se llamó a `streamText`
  - `ai.response.text`: el texto que se generó
  - `ai.response.toolCalls`: las llamadas a herramientas que se realizaron como parte de la generación (JSON stringificado)
  - `ai.response.finishReason`: la razón por la que la generación terminó
  - `ai.settings.maxSteps`: el número máximo de pasos que se estableció

- `ai.streamText.doStream` (span): una llamada doStream de proveedor.
  Este span contiene un evento `ai.stream.firstChunk` y spans `ai.toolCall`.
  Contiene la [información de span de llamada LLM](

# llam-span-información) y los siguientes atributos:

  - `operation.name`: `ai.streamText.doStream` y el `functionId` que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.streamText.doStream"`
  - `ai.prompt.format`: el formato de la solicitud
  - `ai.prompt.messages`: los mensajes que se pasaron al proveedor
  - `ai.prompt.tools`: un array de definiciones de herramientas stringificadas. Las herramientas pueden ser de tipo `function` o `provider-defined`.
    Las herramientas de función tienen un `name`, `description` (opcional) y `parameters` (esquema JSON).
    Las herramientas definidas por el proveedor tienen un `name`, `id` y `args` (Registro).
  - `ai.prompt.toolChoice`: la configuración de la herramienta stringificada (JSON). Tiene una propiedad `type` (`auto`, `none`, `required`, `tool`) y si el tipo es `tool`, una propiedad `toolName` con la herramienta específica.
  - `ai.response.text`: el texto que se generó
  - `ai.response.toolCalls`: las llamadas de herramienta que se realizaron como parte de la generación (stringificadas JSON)
  - `ai.response.msToFirstChunk`: el tiempo que tardó en recibir el primer trozo en milisegundos
  - `ai.response.msToFinish`: el tiempo que tardó en recibir la parte final del flujo de LLM en milisegundos
  - `ai.response.avgCompletionTokensPerSecond`: la cantidad promedio de tokens de completación por segundo
  - `ai.response.finishReason`: la razón por la que se terminó la generación

- `ai.toolCall` (span): una llamada de herramienta que se realiza como parte de la llamada `generateText`. Consulte [Llamadas de herramienta](

#tool-call-spans) para más detalles.

- `ai.stream.firstChunk` (evento): un evento que se emite cuando se recibe el primer trozo del flujo.

  - `ai.response.msToFirstChunk`: el tiempo que tardó en recibir el primer trozo

- `ai.stream.finish` (evento): un evento que se emite cuando se recibe la parte de finalización del flujo del LLM.

También registra un evento `ai.stream.firstChunk` cuando se recibe el primer trozo del flujo.

### función generateObject

`generateObject` registra 2 tipos de espacios:

- `ai.generateObject` (espacio): la longitud completa de la llamada a generateObject. Contiene 1 o más espacios `ai.generateObject.doGenerate`.
  Contiene la [información de espacio de LLM básica](#basic-llm-span-information) y las siguientes atributos:

  - `operation.name`: `ai.generateObject` y el functionId que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.generateObject"`
  - `ai.prompt`: la solicitud que se utilizó cuando se llamó a `generateObject`
  - `ai.schema`: Versión JSON stringificada del esquema que se pasó a la función `generateObject`
  - `ai.schema.name`: el nombre del esquema que se pasó a la función `generateObject`
  - `ai.schema.description`: la descripción del esquema que se pasó a la función `generateObject`
  - `ai.response.object`: el objeto que se generó (JSON stringificado)
  - `ai.settings.mode`: el modo de generación de objetos, por ejemplo `json`
  - `ai.settings.output`: el tipo de salida que se utilizó, por ejemplo `object` o `no-schema`

- `ai.generateObject.doGenerate` (espacio): una llamada doGenerate del proveedor.
  Contiene la [información de espacio de llamada de LLM](

# call-llm-span-information) y las siguientes atributos:

  - `operation.name`: `ai.generateObject.doGenerate` y el functionId que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.generateObject.doGenerate"`
  - `ai.prompt.format`: el formato de la solicitud
  - `ai.prompt.messages`: los mensajes que se pasaron al proveedor
  - `ai.response.object`: el objeto que se generó (JSON stringificado)
  - `ai.settings.mode`: el modo de generación de objetos
  - `ai.response.finishReason`: la razón por la que se terminó la generación

### streamObject function

`streamObject` registra 2 tipos de spans y 1 tipo de evento:

- `ai.streamObject` (span): la longitud completa de la llamada a streamObject. Contiene 1 o más spans `ai.streamObject.doStream`.
  Contiene la [información básica de span de LLM](

# Información de Span para LLM Básico y los siguientes atributos:

  - `operation.name`: `ai.streamObject` y el identificador de función que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.streamObject"`
  - `ai.prompt`: el prompt que se utilizó cuando se llamó a `streamObject`
  - `ai.schema`: Esquema de JSON stringificado de la versión del esquema que se pasó en la función `streamObject`
  - `ai.schema.name`: el nombre del esquema que se pasó en la función `streamObject`
  - `ai.schema.description`: la descripción del esquema que se pasó en la función `streamObject`
  - `ai.response.object`: el objeto que se generó (JSON stringificado)
  - `ai.settings.mode`: el modo de generación de objetos, por ejemplo `json`
  - `ai.settings.output`: el tipo de salida que se utilizó, por ejemplo `object` o `no-schema`

- `ai.streamObject.doStream` (span): una llamada de doStream de proveedor.
  Este span contiene un evento `ai.stream.firstChunk`.
  Contiene la [información de span de llamada LLM](

# Llamar LLM con Información de la Cadena

  - `operation.name`: `ai.streamObject.doStream` y el `functionId` que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.streamObject.doStream"`
  - `ai.prompt.format`: el formato de la solicitud
  - `ai.prompt.messages`: los mensajes que se pasaron al proveedor
  - `ai.settings.mode`: el modo de generación de objetos
  - `ai.response.object`: el objeto que se generó (JSON stringificado)
  - `ai.response.msToFirstChunk`: el tiempo que tardó en recibir el primer trozo
  - `ai.response.finishReason`: la razón por la que la generación terminó

- `ai.stream.firstChunk` (evento): un evento que se emite cuando se recibe el primer trozo de la cadena.
  - `ai.response.msToFirstChunk`: el tiempo que tardó en recibir el primer trozo

### función embed

`embed` registra 2 tipos de trazas:

- `ai.embed` (traza): la longitud completa de la llamada de embed. Contiene 1 `ai.embed.doEmbed` trazas.
  Contiene la [información básica de la traza de embed](#basic-embedding-span-information) y las siguientes atributos:

  - `operation.name`: `ai.embed` y el `functionId` que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.embed"`
  - `ai.value`: el valor que se pasó a la función `embed`
  - `ai.embedding`: una cadena JSON-stringificada de embed

- `ai.embed.doEmbed` (traza): una llamada de doEmbed del proveedor.
  Contiene la [información básica de la traza de embed](#basic-embedding-span-information)

# Información de span para la inmersión básica) y las siguientes atributos:

  - `operation.name`: `ai.embed.doEmbed` y el ID de función que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.embed.doEmbed"`
  - `ai.values`: los valores que se pasaron al proveedor (array)
  - `ai.embeddings`: un array de inmersiones JSON-stringificadas

### función embedMany

`embedMany` registra 2 tipos de spans:

- `ai.embedMany` (span): la longitud completa de la llamada a embedMany. Contiene 1 o más spans `ai.embedMany.doEmbed`.
  Contiene la [información de span de inmersión básica](#información-de-span-para-la-inmersión-básica) y los siguientes atributos:

  - `operation.name`: `ai.embedMany` y el ID de función que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.embedMany"`
  - `ai.values`: los valores que se pasaron a la función `embedMany`
  - `ai.embeddings`: un array de inmersiones JSON-stringificadas

- `ai.embedMany.doEmbed` (span): una llamada doEmbed del proveedor.
  Contiene la [información de span de inmersión básica](#información-de-span-para-la-inmersión-básica) y los siguientes atributos:

  - `operation.name`: `ai.embedMany.doEmbed` y el ID de función que se estableció a través de `telemetry.functionId`
  - `ai.operationId`: `"ai.embedMany.doEmbed"`
  - `ai.values`: los valores que se enviaron al proveedor
  - `ai.embeddings`: un array de inmersiones JSON-stringificadas para cada valor

## Detalles de Span

### Información básica de span de LLM

Muchos spans que utilizan LLMs (`ai.generateText`, `ai.generateText.doGenerate`, `ai.streamText`, `ai.streamText.doStream`,
`ai.generateObject`, `ai.generateObject.doGenerate`, `ai.streamObject`, `ai.streamObject.doStream`) contienen las siguientes atributos:

- `resource.name`: el identificador de función que se estableció a través de `telemetry.functionId`
- `ai.model.id`: el id del modelo
- `ai.model.provider`: el proveedor del modelo
- `ai.request.headers.*`: las cabeceras de solicitud que se pasaron a través de `headers`
- `ai.settings.maxRetries`: el número máximo de intentos que se estableció
- `ai.telemetry.functionId`: el identificador de función que se estableció a través de `telemetry.functionId`
- `ai.telemetry.metadata.*`: el metadatos que se pasaron a través de `telemetry.metadata`
- `ai.usage.completionTokens`: el número de tokens de completación que se utilizaron
- `ai.usage.promptTokens`: el número de tokens de solicitud que se utilizaron

### Información de span de llamada a LLM

Los spans que corresponden a llamadas individuales a LLM (`ai.generateText.doGenerate`, `ai.streamText.doStream`, `ai.generateObject.doGenerate`, `ai.streamObject.doStream`) contienen
[información básica de span de LLM](

#Información de LLM básica y los siguientes atributos:

- `ai.response.model`: el modelo que se utilizó para generar la respuesta. Esto puede ser diferente del modelo solicitado si el proveedor admite alias.
- `ai.response.id`: el id de la respuesta. Utiliza el ID del proveedor cuando está disponible.
- `ai.response.timestamp`: la fecha y hora de la respuesta. Utiliza la fecha y hora del proveedor cuando está disponible.
- [Convenios semánticos para operaciones de GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/)
  - `gen_ai.system`: el proveedor que se utilizó
  - `gen_ai.request.model`: el modelo que se solicitó
  - `gen_ai.request.temperature`: la temperatura que se estableció
  - `gen_ai.request.max_tokens`: el número máximo de tokens que se estableció
  - `gen_ai.request.frequency_penalty`: la penalización de frecuencia que se estableció
  - `gen_ai.request.presence_penalty`: la penalización de presencia que se estableció
  - `gen_ai.request.top_k`: el valor de la parámetro topK que se estableció
  - `gen_ai.request.top_p`: el valor de la parámetro topP que se estableció
  - `gen_ai.request.stop_sequences`: las secuencias de parada
  - `gen_ai.response.finish_reasons`: las razones de finalización que se devolvieron por el proveedor
  - `gen_ai.response.model`: el modelo que se utilizó para generar la respuesta. Esto puede ser diferente del modelo solicitado si el proveedor admite alias.
  - `gen_ai.response.id`: el id de la respuesta. Utiliza el ID del proveedor cuando está disponible.
  - `gen_ai.usage.input_tokens`: el número de tokens de entrada que se utilizaron
  - `gen_ai.usage.output_tokens`: el número de tokens de completado que se utilizaron

### Información básica de span de incorporación

Muchos spans que utilizan modelos de incorporación (`ai.embed`, `ai.embed.doEmbed`, `ai.embedMany`, `ai.embedMany.doEmbed`) contienen las siguientes atributos:

- `ai.model.id`: el id del modelo
- `ai.model.provider`: el proveedor del modelo
- `ai.request.headers.*`: los encabezados de solicitud que se pasaron a través de `headers`
- `ai.settings.maxRetries`: el número máximo de intentos que se estableció
- `ai.telemetry.functionId`: el id de función que se estableció a través de `telemetry.functionId`
- `ai.telemetry.metadata.*`: el metadato que se pasó a través de `telemetry.metadata`
- `ai.usage.tokens`: el número de tokens que se utilizaron
- `resource.name`: el id de función que se estableció a través de `telemetry.functionId`

### Spans de llamada a herramientas

Los spans de llamada a herramientas (`ai.toolCall`) contienen las siguientes atributos:

- `operation.name`: `"ai.toolCall"`
- `ai.operationId`: `"ai.toolCall"`
- `ai.toolCall.name`: el nombre de la herramienta
- `ai.toolCall.id`: el id de la llamada a la herramienta
- `ai.toolCall.args`: los parámetros de la llamada a la herramienta
- `ai.toolCall.result`: el resultado de la llamada a la herramienta. Solo disponible si la llamada a la herramienta es exitosa y el resultado es serializable.

---
title: Visión general
description: Una visión general de la IU del SDK de IA.
---

# SDK UI de IA

El SDK UI de IA está diseñado para ayudarte a crear aplicaciones de chat interactivas, completos y asistentes con facilidad. Es una **herramienta independiente de frameworks**, que simplifica la integración de funcionalidades de IA avanzadas en tus aplicaciones.

El SDK UI de IA proporciona abstracciones robustas que simplifican las complejas tareas de manejo de flujos de chat y actualizaciones de UI en el frontend, permitiéndote desarrollar interfaces dinámicas impulsadas por IA de manera más eficiente. Con cuatro principales hooks — **`useChat`**, **`useCompletion`**, **`useObject`**, y **`useAssistant`** — puedes incorporar capacidades de chat en tiempo real, completos de texto, objetos JSON en streaming, y características de asistentes interactivos en tu aplicación.

- **[`useChat`](/docs/ai-sdk-ui/chatbot)** ofrece un flujo en tiempo real de mensajes de chat, abstractando el manejo de estado para inputs, mensajes, carga y errores, lo que permite una integración suave en cualquier diseño de UI.
- **[`useCompletion`](/docs/ai-sdk-ui/completion)** te permite manejar completos de texto en tus aplicaciones, gestionando la entrada de promt y actualizando automáticamente la UI a medida que se reciben nuevos completos en streaming.
- **[`useObject`](/docs/ai-sdk-ui/object-generation)** es un hook que te permite consumir objetos JSON en streaming, proporcionando una forma simple de manejar y mostrar datos estructurados en tu aplicación.
- **[`useAssistant`](/docs/ai-sdk-ui/openai-assistants)** está diseñado para facilitar la interacción con APIs de asistentes compatibles con OpenAI, gestionando el estado de la UI y actualizándolo automáticamente a medida que se reciben respuestas en streaming.

Estos hooks están diseñados para reducir la complejidad y el tiempo requerido para implementar interacciones de IA, permitiéndote enfocarte en crear experiencias de usuario excepcionales.

## Soporte de Marcas de Interfaz de Usuario

La SDK de IA de UI admite las siguientes marcas de interfaz de usuario: [React](https://react.dev/), [Svelte](https://svelte.dev/), [Vue.js](https://vuejs.org/), y [SolidJS](https://www.solidjs.com/) (descontinuado).
Aquí está

| Función                                                  | React               | Svelte                               | Vue.js              | SolidJS (descontinuado) |
| --------------------------------------------------------- | ------------------- | ------------------------------------ | ------------------- | -------------------- |
| [useChat](/docs/reference/ai-sdk-ui/use-chat)             | <Check size={18} /> | <Check size={18} /> Chat             | <Check size={18} /> | <Check size={18} />  |
| [useCompletion](/docs/reference/ai-sdk-ui/use-completion) | <Check size={18} /> | <Check size={18} /> Completion       | <Check size={18} /> | <Check size={18} />  |
| [useObject](/docs/reference/ai-sdk-ui/use-object)         | <Check size={18} /> | <Check size={18} /> StructuredObject | <Cross size={18} /> | <Check size={18} />  |
| [useAssistant](/docs/reference/ai-sdk-ui/use-assistant)   | <Check size={18} /> | <Cross size={18} />                  | <Check size={18} /> | <Check size={18} />  |

<Nota>
  [Contribuciones](https://github.com/vercel/ai/blob/main/CONTRIBUTING.md) son
  bienvenidas para implementar características faltantes para frameworks no de React.
</Nota>

## Referencia de API

Por favor, consulte la [Referencia de API de SDK UI de IA](/docs/reference/ai-sdk-ui) para obtener más detalles sobre cada función.

---
titulo: Chatbot
descripcion: Aprenda a utilizar la función de uso de Chat.
---

# Chatbot

La función de uso de Chat hace que sea fácil crear una interfaz de usuario conversacional para tu aplicación de chatbot. Permite el streaming de mensajes de chat desde tu proveedor de inteligencia artificial, gestiona el estado del chat y actualiza automáticamente la interfaz de usuario a medida que llegan nuevos mensajes.

Para resumir, la función de uso de Chat proporciona las siguientes características:

- **Streaming de mensajes**: Todos los mensajes del proveedor de inteligencia artificial se streamean a la interfaz de chat en tiempo real.
- **Estados administrados**: La función gestiona los estados para la entrada, mensajes, estado, error y más por ti.
- **Integración suave**: Integra fácilmente tu chat AI en cualquier diseño o disposición con un mínimo de esfuerzo.

En esta guía, aprenderás a utilizar la función de uso de Chat para crear una aplicación de chatbot con streaming de mensajes en tiempo real.
Consulte nuestra [guía de chatbot con herramientas](/docs/ai-sdk-ui/chatbot-with-tool-calling) para aprender a utilizar herramientas en tu chatbot.
Comencemos con el siguiente ejemplo primero.

```javascript
import { useChat } from 'ai-sdk-ui';

function Chatbot() {
  const { messages, sendMessage, status, error } = useChat({
    // Initialize your AI provider here
  });

  return (
    <div>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message.text}</li>
        ))}
      </ul>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <button onClick={sendMessage}>Enviar</button>
      <p>Status: {status}</p>
      <p>Error: {error}</p>
    </div>
  );
}
```

## Ejemplo

```tsx filename='app/page.tsx'
'use client';

import { useChat } from '@ai-sdk/react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({});

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.role === 'user' ? 'Usuario: ' : 'IA: '}
          {message.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input name="prompt" value={input} onChange={handleInputChange} />
        <button type="submit">Enviar</button>
      </form>
    </>
  );
}
```

```ts filename='app/api/chat/route.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

// Permite streaming de respuestas hasta 30 segundos
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4-turbo'),
    system: 'Usted es un asistente útil.',
    messages,
  });

  return result.toDataStreamResponse();
}
```

<Nota>
  Los mensajes de la interfaz de usuario tienen una nueva propiedad `parts` que contiene los partes del mensaje.
  Recomendamos renderizar los mensajes utilizando la propiedad `parts` en lugar de la propiedad `content`.
  La propiedad `parts` admite diferentes tipos de mensajes, incluyendo texto, invocación de herramientas y resultado de herramientas, y permite interfaces de chat más flexibles y complejas.
</Nota>

En el componente `Page`, el hook `useChat` solicitará a tu proveedor de IA el endpoint cada vez que el usuario envíe un mensaje.
Los mensajes se devuelven en tiempo real y se muestran en la interfaz de chat.

Esto permite una experiencia de chat fluida donde el usuario puede ver la respuesta de IA tan pronto como esté disponible,
sin tener que esperar a que se reciba toda la respuesta.

## Interfaz Personalizada

`useChat` también proporciona formas de gestionar los estados de mensajes de chat y de entrada mediante código, mostrar el estado, y actualizar mensajes sin que se desencadenen mediante interacciones del usuario.

### Estado

El hook `useChat` devuelve un `status`. Tiene los siguientes valores posibles:

- `enviado`: El mensaje ha sido enviado a la API y estamos esperando el inicio de la transmisión de la respuesta.
- `transmitiendo`: La respuesta está transmitiéndose activamente desde la API, recibiendo trozos de datos.
- `listo`: La respuesta completa ha sido recibida y procesada; un nuevo mensaje de usuario puede ser enviado.
- `error`: Ocurrió un error durante la solicitud de la API, impidiendo una finalización exitosa.

Puedes utilizar `status` para fines como:

- Mostrar un cargador de espíritu mientras el chatbot procesa el mensaje del usuario.
- Mostrar un botón "Detener" para abortar el mensaje actual.
- Deshabilitar el botón de envío.

```tsx filename='app/page.tsx' highlight="6,20-27,34"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit, status, stop } =
    useChat({});

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.role === 'user' ? 'Usuario: ' : 'IA: '}
          {message.content}
        </div>
      ))}

      {(status === 'enviado' || status === 'transmitiendo') && (
        <div>
          {status === 'enviado' && <Spinner />}
          <button type="button" onClick={() => stop()}>
            Detener
          </button>
        </div>
      )}
```

<form onSubmit={handleSubmit}>
        <input
          name="prompt"
          value={input}
          onChange={handleInputChange}
          disabled={estatus !== 'ready'}
        />
        <button type="submit">Enviar</button>
      </form>
   

### Estado de Error

De manera similar, el estado `error` refleja el objeto de error lanzado durante la solicitud de fetch.
Puede utilizarse para mostrar un mensaje de error, deshabilitar el botón de submit o mostrar un botón de retry:

<Nota>
  Recomendamos mostrar un mensaje de error genérico al usuario, como "Algo salió mal."
  Esta es una buena práctica para evitar revelar información del servidor.
</Nota>

```tsx file="app/page.tsx" highlight="6,18-25,31"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, error, reload } =
    useChat({});

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}
        </div>
      ))}

      {error && (
        <>
          <div>Se produjo un error.</div>
          <button type="button" onClick={() => reload()}>
            Volver a intentarlo
          </button>
        </>
      )}

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          disabled={error != null}
        />
      </form>
    </div>
  );
}
```

Consulte también la guía de [manejo de errores](/docs/ai-sdk-ui/error-handling) para obtener más información.

### Modificar mensajes

A veces, puede que desee modificar directamente algunos mensajes existentes. Por ejemplo, se puede agregar un botón de eliminar a cada mensaje para que los usuarios puedan eliminarlos de la historia de chat.

La función `setMessages` puede ayudarlo a lograr estos objetivos:

```tsx
const { messages, setMessages, ... } = useChat()

const handleDelete = (id) => {
  setMessages(messages.filter(message => message.id !== id))
}

return <>
  {messages.map(message => (
    <div key={message.id}>
      {message.role === 'user' ? 'Usuario: ' : 'IA: '}
      {message.content}
      <button onClick={() => handleDelete(message.id)}>Eliminar</button>
    </div>
  ))}
  ...
```

Puede pensar en `messages` y `setMessages` como una pareja de `state` y `setState` en React.

### Entrada controlada

En el ejemplo inicial, tenemos las funciones de llamada a retorno `handleSubmit` y `handleInputChange` que gestionan los cambios de entrada y las presentaciones de formulario. Estas son útiles para casos de uso comunes, pero también puede utilizar APIs no controladas para escenarios más avanzados como la validación de formulario o componentes personalizados.

El siguiente ejemplo demuestra cómo utilizar APIs más granulares como `setInput` y `append` con sus componentes de entrada y botón de envío personalizados:

```tsx
const { input, setInput, append } = useChat()

return <>
  <MiEntradaPersonalizada value={input} onChange={value => setInput(value)} />
  <MiBotonDeEnviar onClick={() => {
    // Envía un nuevo mensaje al proveedor de IA
    append({
      role: 'user',
      content: input,
    })
  }}/>
  ...
```

### Cancelación y regeneración

También es un caso de uso común abortar el mensaje de respuesta mientras aún está siendo transmitido desde el proveedor de IA. Puedes hacer esto llamando a la función `stop` devuelta por la función de hook `useChat`.

```tsx
const { stop, status, ... } = useChat()

return <>
  <button onClick={stop} disabled={!(status === 'streaming' || status === 'submitted')}>Detener</button>
  ...
```

Cuando el usuario hace clic en el botón "Detener", la solicitud de fetch se abortará. Esto evita el consumo de recursos innecesarios y mejora la experiencia del usuario de tu aplicación de chatbot.

De manera similar, también puedes solicitar al proveedor de IA que reprociese el último mensaje llamando a la función `reload` devuelta por la función de hook `useChat`:

```tsx
const { reload, status, ... } = useChat()

return <>
  <button onClick={reload} disabled={!(status === 'ready' || status === 'error')}>Regenerar</button>
  ...
</>
```

Cuando el usuario hace clic en el botón "Regenerar", el proveedor de IA regenerará el último mensaje y lo reemplazará correspondientemente.

### Ralentización de actualizaciones de UI

<Nota>Esta función solo está disponible actualmente para React.</Nota>

Por defecto, la función de hook `useChat` provocará un renderizado cada vez que se reciba un nuevo trozo.
Puedes ralentizar las actualizaciones de UI con la opción `experimental_throttle`.

```tsx filename="page.tsx" highlight="2-3"
const { messages, ... } = useChat({
  // Ralentiza las actualizaciones de mensajes y datos a 50ms:
  experimental_throttle: 50
})
```

## Eventos de Callback

`useChat` proporciona callbacks de eventos opcionales que puedes utilizar para manejar diferentes etapas del ciclo de vida del chatbot:

- `onFinish`: Llamado cuando el mensaje del asistente se completa
- `onError`: Llamado cuando ocurre un error durante la solicitud de fetch.
- `onResponse`: Llamado cuando se recibe la respuesta del API.

Estos callbacks se pueden utilizar para desencadenar acciones adicionales, como registro, análisis o actualizaciones de interfaz de usuario personalizadas.

```tsx
import { Message } from '@ai-sdk/react';

const {
  /* ... */
} = useChat({
  onFinish: (message, { usage, finishReason }) => {
    console.log('Se ha completado la transmisión del mensaje:', message);
    console.log('Uso del token:', usage);
    console.log('Razón de finalización:', finishReason);
  },
  onError: error => {
    console.error('Ocurrió un error:', error);
  },
  onResponse: response => {
    console.log('Se recibió la respuesta HTTP del servidor:', response);
  },
});
```

Es importante tener en cuenta que puedes abortar el procesamiento lanzando un error en el callback `onResponse`. Esto desencadenará el callback `onError` y detendrá el mensaje de ser agregado a la interfaz de usuario del chat. Esto puede ser útil para manejar respuestas inesperadas del proveedor de inteligencia artificial.

## Configuración de la solicitud

### Encabezados, cuerpo y credenciales personalizadas

Por defecto, la función de hook `useChat` envía una solicitud HTTP POST a la ruta `/api/chat` con la lista de mensajes como cuerpo de la solicitud. Puedes personalizar la solicitud pasando opciones adicionales a la función de hook `useChat`:

```tsx
const { messages, input, handleInputChange, handleSubmit } = useChat({
  api: '/api/chat-personalizado',
  headers: {
    Authorization: 'tu_token',
  },
  body: {
    id_usuario: '123',
  },
  credentials: 'same-origin',
});
```

En este ejemplo, la función de hook `useChat` envía una solicitud POST a la ruta `/api/chat-personalizado` con los encabezados, campos de cuerpo adicionales y credenciales especificados para esa solicitud de fetch. En el lado del servidor, puedes manejar la solicitud con esta información adicional.

### Configurando campos de cuerpo personalizados por solicitud

Puedes configurar campos `body` personalizados en una base por solicitud utilizando la opción `body` de la función `handleSubmit`.
Esto es útil si deseas pasar información adicional a tu backend que no forma parte de la lista de mensajes.

```tsx archivo="app/page.tsx" resaltado="18-20"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}
        </div>
      ))}

      <form
        onSubmit={event => {
          handleSubmit(event, {
            body: {
              customKey: 'customValue',
            },
          });
        }}
      >
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

Puedes recuperar estos campos personalizados en tu lado servidor desestructurando el cuerpo de la solicitud:

```ts archivo="app/api/chat/route.ts" resaltado="3"
export async function POST(req: Request) {
  // Extrae la información adicional ("customKey") del cuerpo de la solicitud:
  const { messages, customKey } = await req.json();
  //...
}
```

## Controlando el flujo de respuesta

Con `streamText`, puedes controlar cómo se envían mensajes de error y información de uso a la cliente.

### Mensajes de Error

Por defecto, el mensaje de error está oculto por razones de seguridad.
El mensaje de error predeterminado es "Se produjo un error."
Puedes enviar mensajes de error o enviar tu propio mensaje de error proporcionando una función `getErrorMessage`:

```ts filename="app/api/chat/route.ts" highlight="13-27"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
  });

  return result.toDataStreamResponse({
    getErrorMessage: error => {
      if (error == null) {
        return 'error desconocido';
      }

      if (typeof error === 'string') {
        return error;
      }

      if (error instanceof Error) {
        return error.message;
      }

      return JSON.stringify(error);
    },
  });
}
```

### Información de Uso

Por defecto, la información de uso se envía de regreso al cliente. Puedes deshabilitarlo estableciendo la opción `sendUsage` en `false`:

```ts filename="app/api/chat/route.ts" highlight="13"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
  });

  return result.toDataStreamResponse({
    sendUsage: false,
  });
}
```

### Flujos de texto

`useChat` puede manejar flujos de texto plano estableciendo la opción `streamProtocol` a `text`:

```tsx filename="app/page.tsx" highlight="7"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages } = useChat({
    streamProtocol: 'text',
  });

  return <>...</>;
}
```

Esta configuración también funciona con otros servidores de backend que emiten texto plano.
Consulte la [guía de protocolo de flujo](/docs/ai-sdk-ui/stream-protocol) para obtener más información.

<Nota>
  Cuando se utiliza `streamProtocol: 'text'`, no se tienen disponibles las llamadas de herramienta, la información de uso y las razones de finalización.
</Nota>

## Submisiones vacías

Puede configurar la función de hook `useChat` para permitir submisiones vacías estableciendo la opción `allowEmptySubmit` en `true`.

```tsx filename="app/page.tsx" highlight="18"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}
        </div>
      ))}

      <form
        onSubmit={event => {
          handleSubmit(event, {
            allowEmptySubmit: true,
          });
        }}
      >
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

## Razonamiento

Algunos modelos como DeepSeek `deepseek-reasoner` y Anthropic `claude-3-7-sonnet-20250219` admiten tokens de razonamiento. Estos tokens se envían típicamente antes del contenido del mensaje. Puedes enviarlos al cliente con la opción `sendReasoning`:

```ts filename="app/api/chat/route.ts" highlight="13"
import { deepseek } from '@ai-sdk/deepseek';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: deepseek('deepseek-reasoner'),
    messages,
  });

  return result.toDataStreamResponse({
    sendReasoning: true,
  });
}
```

En el lado del cliente, puedes acceder a las partes de razonamiento del objeto de mensaje.

Tienen una propiedad `details` que contiene las partes de razonamiento y redactadas. También puedes usar `reasoning` para acceder solo a la razonamiento como una cadena.

```tsx filename="app/page.tsx"
messages.map(message => (
  <div key={message.id}>
    {message.role === 'user' ? 'Usuario: ' : 'IA: '}
    {message.parts.map((part, index) => {
      // partes de texto:
      if (part.type === 'text') {
        return <div key={index}>{part.text}</div>;
      }

// partes de razonamiento:
      if (part.type === 'razonamiento') {
        return (
          <pre key={index}>
            {part.details.map(detail =>
              detail.type === 'texto' ? detail.text : '<restringido>',
            )}
          </pre>
        );
      }
    })}
  </div>
));

## Fuentes

Algunos proveedores, como [Perplexity](/providers/ai-sdk-providers/perplexity#fuentes) y
[

# Fuente) incluya fuentes en la respuesta.

Actualmente, las fuentes están limitadas a páginas web que respaldan la respuesta.
Puede enviarlas al cliente con la opción `sendSources`:

```ts filename="app/api/chat/route.ts" highlight="13"
import { perplexity } from '@ai-sdk/perplexity';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: perplexity('sonar-pro'),
    messages,
  });

  return result.toDataStreamResponse({
    sendSources: true,
  });
}
```

En el lado del cliente, puede acceder a las partes de fuente del objeto de mensaje.
Aquí hay un ejemplo que renderiza las fuentes como enlaces en la parte inferior del mensaje:

```tsx
// app/page.tsx
messages.map(message => (
  <div key={message.id}>
    {message.role === 'user' ? 'Usuario: ' : 'IA: '}
    {message.parts
      .filter(part => part.type !== 'source')
      .map((part, index) => {
        if (part.type === 'text') {
          return <div key={index}>{part.text}</div>;
        }
      })}
    {message.parts
      .filter(part => part.type === 'source')
      .map(part => (
        <span key={`source-${part.source.id}`}>
          [
          <a href={part.source.url} target="_blank">
            {part.source.title ?? new URL(part.source.url).hostname}
          </a>
          ]
        </span>
      ))}
  </div>
));
```

```diff
- No cambios en el código.
```

## Generación de Imágenes

Algunos modelos, como Google `gemini-2.0-flash-exp`, admiten la generación de imágenes.
Cuando se generan imágenes, se exponen como archivos al cliente.
En el lado del cliente, puedes acceder a las partes de archivo del objeto de mensaje
y renderizarlas como imágenes.

```tsx filename="app/page.tsx"
messages.map(message => (
  <div key={message.id}>
    {message.role === 'user' ? 'Usuario: ' : 'IA: '}
    {message.parts.map((part, index) => {
      if (part.type === 'text') {
        return <div key={index}>{part.text}</div>;
      } else if (part.type === 'file' && part.mimeType.startsWith('image/')) {
        return (
          <img key={index} src={`data:${part.mimeType};base64,${part.data}`} />
        );
      }
    })}
  </div>
));
```

## Adjuntos (Experimental)

La función de hook `useChat` admite enviar adjuntos junto con un mensaje, así como renderizarlos en el lado del cliente. Esto puede ser útil para construir aplicaciones que involucran enviar imágenes, archivos o contenido de medios a proveedores de IA.

Hay dos formas de enviar adjuntos con un mensaje, ya sea proporcionando un objeto `FileList` o una lista de URLs a la función `handleSubmit`:

### FileList

Al utilizar `FileList`, puedes enviar múltiples archivos como adjuntos junto con un mensaje utilizando el elemento de entrada de archivo. La función de hook `useChat` convertirá automáticamente los archivos en URLs de datos y los enviará al proveedor de IA.

<Nota>
  Actualmente, solo los tipos de contenido `image/*` y `text/*` se convierten automáticamente
  en [partes de contenido multimodal](/docs/foundations/prompts)

# Mensajes Multi-Modales). Tendrás que manejar otros tipos de contenido manualmente.
</Note>

```tsx filename="app/page.tsx"
'use client';

import { useChat } from '@ai-sdk/react';
import { useRef, useState } from 'react';

export default function Page() {
  const { messages, input, handleSubmit, handleInputChange, status } =
    useChat();

  const [files, setFiles] = useState<FileList | undefined>(undefined);
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <div>
      <div>
        {messages.map(message => (
          <div key={message.id}>
            <div>{`${message.role}: `}</div>

            <div>
              {message.content}
```

Nota: La traducción de "multi-modal" a "multi-Modales" se realizó considerando el contexto de la documentación.

<div>
  {message.experimental_attachments
    ?.filter(attachment =>
      attachment.contentType.startsWith('image/'),
    )
    .map((attachment, index) => (
      <img
        key={`${message.id}-${index}`}
        src={attachment.url}
        alt={attachment.name}
      />
    ))}
</div>
</div>
</div>
</div>

<form
  onSubmit={event => {
    handleSubmit(event, {
      experimental_attachments: archivos,


Si (fileInputRef.current) {
            fileInputRef.current.value = '';
          }
        }}
      >
        <input
          type="file"
          onChange={event => {
            if (event.target.files) {
              setFiles(event.target.files);
            }
          }}
          multiple
          ref={fileInputRef}
        />
        <input
          value={input}
          placeholder="Enviar mensaje..."
          onChange={handleInputChange}
          disabled={status !== 'ready'}
        />
      </form>
    </div>
  );

### URLs

También puedes enviar URLs como adjuntos junto con un mensaje. Esto puede ser útil para enviar enlaces a recursos o contenido de medios externos.

> **Nota:** La URL también puede ser una URL de datos, que es una cadena base64 codificada que representa el contenido de un archivo. Actualmente, solo los tipos de contenido `image/*` se convierten automáticamente en [partes de contenido multimodal](/docs/foundations/prompts)

# Mensajes Multi-Modales). Deberá manejar otros tipos de contenido manualmente.

```tsx filename="app/page.tsx"
'use client';

import { useChat } from '@ai-sdk/react';
import { useState } from 'react';
import { Attachment } from '@ai-sdk/ui-utils';

export default function Page() {
  const { messages, input, handleSubmit, handleInputChange, status } =
    useChat();

  const [attachments] = useState<Attachment[]>([
    {
      name: 'tierra.png',
      contentType: 'image/png',
      url: 'https://example.com/tierra.png',
    },
    {
      name: 'luna.png',
      contentType: 'image/png',
      url: 'data:image/png;base64,iVBORw0KGgo...',
    },
  ]);

  return (
    <div>
      <div>
        {messages.map(message => (
          <div key={message.id}>
            <div>{`${message.role}: `}</div>

            <div>
              {message.content}
```

Nota: No se tradujo el código de la imagen base64 para evitar problemas de compatibilidad.

<div>
  {message.experimental_attachments
    ?.filter(attachment =>
      attachment.contentType?.startsWith('image/'),
    )
    .map((attachment, index) => (
      <img
        key={`${message.id}-${index}`}
        src={attachment.url}
        alt={attachment.name}
      />
    ))}


<form
        onSubmit={event => {
          handleSubmit(event, {
            experimental_attachments: attachments,
          });
        }}
      >
        <input
          value={input}
          placeholder="Enviar mensaje..."
          onChange={handleInputChange}
          disabled={status !== 'ready'}
        />
      </form>
    </div>
  );
}
```

---
titulo: Persistencia de mensajes de chatbot
descripcion: Aprende a almacenar y cargar mensajes de chat en un chatbot.
---

# Persistencia de mensajes de chat

La capacidad de almacenar y cargar mensajes de chat es crucial para la mayoría de los chatbots de IA.
En esta guía, mostraremos cómo implementar la persistencia de mensajes con `useChat` y `streamText`.

<Nota>
  Esta guía no cubre la autorización, el manejo de errores o otras consideraciones del mundo real.
  Está destinada a ser un ejemplo simple de cómo implementar la persistencia de mensajes.
</Nota>

## Iniciando una nueva conversación

Cuando el usuario navega a la página de chat sin proporcionar un ID de conversación,
debemos crear una nueva conversación y redirigir a la página de chat con el nuevo ID de conversación.

```tsx filename="app/chat/page.tsx"
import { redirect } from 'next/navigation';
import { createChat } from '@tools/chat-store';

export default async function Page() {
  const id = await createChat(); // crear una nueva conversación
  redirect(`/chat/${id}`); // redirigir a la página de chat, véase a continuación
}
```

Nuestra implementación de almacenamiento de chat utiliza archivos para almacenar los mensajes de chat.
En una aplicación real, utilizarías una base de datos o un servicio de almacenamiento en la nube,
y obtendrías el ID de la conversación de la base de datos.
Dicho esto, las interfaces de función están diseñadas para ser fácilmente reemplazadas con otras implementaciones.

```tsx filename="tools/chat-store.ts"
import { generateId } from 'ai';
import { existsSync, mkdirSync } from 'fs';
import { writeFile } from 'fs/promises';
import path from 'path';

export async function createChat(): Promise<string> {
  const id = generateId(); // generar un ID de conversación único
  await writeFile(getChatFile(id), '[]'); // crear un archivo de chat vacío
  return id;
}

function getChatFile(id: string): string {
  const chatDir = path.join(process.cwd(), '.chats');
  if (!existsSync(chatDir)) mkdirSync(chatDir, { recursive: true });
  return path.join(chatDir, `${id}.json`);
}
```

## Cargando una conversación existente

Cuando el usuario navega a la página de chat con un ID de conversación, debemos cargar los mensajes de la conversación y mostrarlos.

```tsx filename="app/chat/[id]/page.tsx"
import { loadChat } from '@tools/chat-store';
import Chat from '@ui/chat';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const { id } = await props.params; // obtener el ID de la conversación desde la URL
  const messages = await loadChat(id); // cargar los mensajes de la conversación
  return <Chat id={id} initialMessages={messages} />; // mostrar la conversación
}
```

La función `loadChat` en nuestro almacén de chat basado en archivos se implementa de la siguiente manera:

```tsx filename="tools/chat-store.ts"
import { Message } from 'ai';
import { readFile } from 'fs/promises';

export async function loadChat(id: string): Promise<Message[]> {
  return JSON.parse(await readFile(getChatFile(id), 'utf8'));
}

// ... resto del archivo
```

El componente de visualización es un componente de chat simple que utiliza la hook `useChat` para enviar y recibir mensajes:

```tsx filename="ui/chat.tsx" highlight="10-12"
'use client';

import { Message, useChat } from '@ai-sdk/react';

export default function Chat({
  id,
  initialMessages,
}: { id?: string | undefined; initialMessages?: Message[] } = {}) {
  const { input, handleInputChange, handleSubmit, messages } = useChat({
    id, // usar el ID de la conversación proporcionado
    initialMessages, // mensajes inicializados si se proporcionan
    sendExtraMessageFields: true, // enviar id y createdAt para cada mensaje
  });
```

// código de renderizado simplificado, ampliar según sea necesario:
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role === 'user' ? 'Usuario: ' : 'IA: '}
          {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}

## Almacenar mensajes

`useChat` envía el id de la conversación y los mensajes al backend.
Hemos habilitado la opción `sendExtraMessageFields` para enviar los campos `id` y `createdAt`, lo que significa que almacenamos los mensajes en el formato de mensaje `useChat`.

<Nota>
  El formato de mensaje `useChat` es diferente del formato `CoreMessage`. El formato de mensaje `useChat` está diseñado para la visualización en el frontend y contiene campos adicionales como `id` y `createdAt`. Recomendamos almacenar los mensajes en el formato `useChat`.
</Nota>

El almacenamiento de mensajes se realiza en el callback `onFinish` de la función `streamText`. `onFinish` recibe los mensajes de la respuesta del modelo AI como un arreglo `CoreMessage[]`, y utilizamos la función ayudante `appendResponseMessages` para agregar los mensajes de la respuesta del modelo AI a los mensajes de la conversación.

```tsx filename="app/api/chat/route.ts" highlight="6,11-19"
import { openai } from '@ai-sdk/openai';
import { appendResponseMessages, streamText } from 'ai';
import { saveChat } from '@tools/chat-store';

export async function POST(req: Request) {
  const { messages, id } = await req.json();

  const result = streamText({
    model: openai('gpt-4o-mini'),
    messages,
    async onFinish({ response }) {
      await saveChat({
        id,
        messages: appendResponseMessages({
          messages,
          responseMessages: response.messages,
        }),
      });
    },
  });

  return result.toDataStreamResponse();
}
```

El almacenamiento real de los mensajes se realiza en la función `saveChat`, que en nuestro almacenamiento de conversaciones basado en archivos se implementa de la siguiente manera:

```tsx
// tools/chat-store.ts
import { Message } from 'ai';
import { writeFile } from 'fs/promises';

/**
 * Guarda una conversación en un archivo.
 * 
 * @param {Object} options - Opciones para guardar la conversación.
 * @param {string} options.id - Identificador único de la conversación.
 * @param {Message[]} options.messages - Mensajes de la conversación.
 */
export async function saveChat({
  id,
  messages,
}: {
  id: string;
  messages: Message[];
}): Promise<void> {
  const content = JSON.stringify(messages, null, 2);
  await writeFile(getChatFile

## Identificadores de Mensajes

Además de un ID de chat, cada mensaje tiene un ID propio.
Puedes utilizar este ID de mensaje para manipular mensajes individuales.

Los IDs para mensajes de usuarios se generan mediante el hook `useChat` en el cliente,
y los IDs para respuestas de IA se generan mediante `streamText`.

Puedes controlar el formato de ID proporcionando generadores de ID
(consulte [`createIdGenerator()`](/docs/reference/ai-sdk-core/create-id-generator):

```tsx filename="ui/chat.tsx" highlight="8-12"
import { createIdGenerator } from 'ai';
import { useChat } from '@ai-sdk/react';

const {
  // ...
} = useChat({
  // ...
  // formato de ID para mensajes del lado del cliente:
  generateId: createIdGenerator({
    prefix: 'msgc',
    size: 16,
  }),
});
```

```tsx filename="app/api/chat/route.ts" highlight="7-11"
import { createIdGenerator, streamText } from 'ai';

export async function POST(req: Request) {
  // ...
  const result = streamText({
    // ...
    // formato de ID para mensajes del lado del servidor:
    experimental_generateMessageId: createIdGenerator({
      prefix: 'msgs',
      size: 16,
    }),
  });
  // ...
}
```

## Enviar solo el último mensaje

Una vez que hayas implementado la persistencia de mensajes, podrías querer enviar solo el último mensaje al servidor.
Esto reduce la cantidad de datos enviados al servidor en cada solicitud y puede mejorar el rendimiento.

Para lograr esto, puedes proporcionar una función `experimental_prepareRequestBody` a la hook `useChat` (solo React).
Esta función recibe los mensajes y el ID de la conversación, y devuelve el cuerpo de la solicitud que se enviará al servidor.

```tsx filename="ui/chat.tsx" highlight="7-10"
import { useChat } from '@ai-sdk/react';

const {
  // ...
} = useChat({
  // ...
  // solo envía el último mensaje al servidor:
  experimental_prepareRequestBody({ messages, id }) {
    return { message: messages[messages.length - 1], id };
  },
});
```

En el servidor, puedes cargar los mensajes anteriores y agregar el nuevo mensaje a los mensajes anteriores:

```tsx filename="app/api/chat/route.ts" highlight="2-9"
import { appendClientMessage } from 'ai';

export async function POST(req: Request) {
  // obtén el último mensaje del cliente:
  const { message, id } = await req.json();

  // carga los mensajes anteriores desde el servidor:
  const previousMessages = await loadChat(id);

  // agrega el nuevo mensaje a los mensajes anteriores:
  const messages = appendClientMessage({
    messages: previousMessages,
    message,
  });

  const result = streamText({
    // ...
    messages,
  });

  // ...
}
```

## Manejando desconexiones del cliente

Por defecto, la función `streamText` del SDK de AI utiliza backpressure hacia el proveedor de modelos de lenguaje para prevenir
el consumo de tokens que no se han solicitado aún.

Sin embargo, esto significa que cuando el cliente se desconecta, por ejemplo, cerrando la pestaña del navegador o debido a un problema de red,
el flujo desde el LLM se abortará y la conversación puede terminar en un estado roto.

Asumiendo que tienes una [solución de almacenamiento](

# Almacenando mensajes

Si deseas mantener el flujo de mensajes en su lugar, puede utilizar el método `consumeStream` para consumir el flujo en el backend, y luego guardar el resultado de manera habitual.
`consumeStream` elimina efectivamente la presión de retroceso,
lo que significa que el resultado se almacena incluso cuando el cliente ya se ha desconectado.

```tsx filename="app/api/chat/route.ts" highlight="21-23"
import { appendResponseMessages, streamText } from 'ai';
import { saveChat } from '@tools/chat-store';

export async function POST(req: Request) {
  const { messages, id } = await req.json();

  const result = streamText({
    model,
    messages,
    async onFinish({ response }) {
      await saveChat({
        id,
        messages: appendResponseMessages({
          messages,
          responseMessages: response.messages,
        }),
      });
    },
  });

  // consuma el flujo para asegurarse de que se ejecute hasta su finalización y active onFinish
  // incluso cuando la respuesta del cliente se aborta:
  result.consumeStream(); // no await

  return result.toDataStreamResponse();
}
```

Cuando el cliente recarga la página después de una desconexión, el chat se restaurará desde la solución de almacenamiento.

<Nota>
  En aplicaciones de producción, también rastrearía el estado de la solicitud (en progreso, completa) en los mensajes almacenados y utilizaría en el cliente para cubrir el caso en el que el cliente recarga la página después de una desconexión, pero el streaming no se ha completado aún.
</Nota>

## Reanudando flujos en curso

<Nota>Esta característica es experimental y puede cambiar en versiones futuras.</Nota>

El hook `useChat` tiene un soporte experimental para reanudar un flujo de generación de chat en curso por cualquier cliente, ya sea después de una desconexión de red o al recargar la página de chat. Esto puede ser útil para construir aplicaciones que involucran conversaciones de larga duración o para asegurarse de que los mensajes no se pierdan en caso de fallas de red.

Los siguientes son los requisitos previos para que tu aplicación de chat soporte flujos reanudables:

- Instalar el paquete `resumable-stream` <https://www.npmjs.com/package/resumable-stream> que ayuda a crear y gestionar el mecanismo de publicador/ suscriptor de los flujos.
- Crear una instancia de [Redis](https://vercel.com/marketplace/redis) para almacenar el estado del flujo.
- Crear una tabla que rastree los IDs de flujo asociados con un chat.

Para reanudar un flujo de chat, utilizarás la función `experimental_resume` devuelta por el hook `useChat`. Llamarás a esta función durante la montaje inicial del hook dentro del componente principal de chat.

```tsx filename="app/components/chat.tsx"
'use client';

import { useChat } from '@ai-sdk/react';
import { Input } from '@/components/input';
import { Messages } from '@/components/messages';

export function Chat() {
  const { experimental_resume } = useChat({ id });

  useEffect(() => {
    experimental_resume();

    // usamos un arreglo vacío de dependencias para
    // asegurarnos de que este efecto se ejecute solo una vez
  }, []);

  return (
    <div>
      <Messages />
      <Input />
    </div>
  );
}
```

Para una implementación más resistente que maneje condiciones de carrera que pueden ocurrir durante una solicitud de reanudación, puedes utilizar el siguiente hook `useAutoResume`. Esto procesará automáticamente los datos de SSE `append-message` que se transmiten por el servidor.

```tsx filename="app/hooks/use-auto-resume.ts"
'use client';

```javascript
import { useEffect } from 'react';
import type { UIMensaje } from 'ai';
import type { UseChatAyudas } from '@ai-sdk/react';

export type DataPart = { tipo: 'append-message'; mensaje: string };

export interface Props {
  autoResume: boolean;
  mensajesIniciales: UIMensaje[];
  experimental_resume: UseChatAyudas['experimental_resume'];
  data: UseChatAyudas['data'];
  setMessages: UseChatAyudas['setMessages'];
}

export function useAutoResume({
  autoResume,
  mensajesIniciales,
  experimental_resume,
  data,
  setMessages,
}: Props) {
  useEffect(() => {
    if (!autoResume) return;

    const mensajeMásReciente = mensajesIniciales.at(-1);

    if (mensajeMásReciente?.role === 'user') {
      experimental_resume();
    }

    // ejecutamos esto una vez intencionalmente
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!data || data.length === 0) return;

    const dataPart = data[0] as DataPart;

    if (dataPart.tipo === 'append-message') {
      const mensaje = JSON.parse(dataPart.mensaje) as UIMensaje;
      setMessages([...mensajesIniciales, mensaje]);
    }
  }, [data, mensajesIniciales, setMessages]);
}
```

Puedes utilizar esta función de hook en tu componente de chat de la siguiente manera.

```tsx filename="app/components/chat.tsx"
'use client';

import { useChat } from '@ai-sdk/react';
import { Input } from '@/components/input';
import { Messages } from '@/components/messages';
import { useAutoResume } from '@/hooks/use-auto-resume';
```

```javascript
export function Chat() {
  const { experimental_resume, data, setMessages } = useChat({ id });

  useAutoResume({
    autoResume: true,
    initialMessages: [],
    experimental_resume,
    data,
    setMessages,
  });

  return (
    <div>
      <Messages />
      <Input />
    </div>
  );
}
```

La función `experimental_resume` realiza una solicitud `GET` a tu punto de conexión de chat configurado (o `/api/chat` por defecto) cada vez que tu cliente la llama. Si hay un flujo activo, continuará desde donde lo dejó, de lo contrario simplemente terminará sin error.

La solicitud `GET` agrega automáticamente el parámetro de consulta `chatId` a la URL para ayudar a identificar el chat a la que pertenece la solicitud. Utilizando el `chatId`, puedes buscar el ID del flujo más reciente en la base de datos y reanudar el flujo.

```bash
GET /api/chat?chatId=<tu-id-de-chat>
```

Anteriormente, debiste haber implementado el manejo de `POST` para la ruta `/api/chat` para crear nuevas generaciones de chats. Cuando se utiliza `experimental_resume`, también debes implementar el maneje de `GET` para la ruta `/api/chat` para reanudar los flujos.

### 1. Implementar el manejador GET

Agregar un método `GET` a `/api/chat` que:

1. Lee `chatId` desde la cadena de consulta
2. Lo valida para asegurarse de que esté presente
3. Carga cualquier ID de flujo almacenado para ese chat
4. Devuelve el más reciente a `streamContext.resumableStream()`
5. Se reemplaza por un flujo vacío si ya está cerrado

```ts filename="app/api/chat/route.ts"
import { loadStreams } from '@/util/chat-store';
import { createDataStream, getMessagesByChatId } from 'ai';
import { after } from 'next/server';
import { createResumableStreamContext } from 'resumable-stream';

const streamContext = createResumableStreamContext({
  waitUntil: after,
});

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const chatId = searchParams.get('chatId');

  if (!chatId) {
    return new Response('es requerido', { status: 400 });
  }

  const streamIds = await loadStreams(chatId);

  if (!streamIds.length) {
    return new Response('No se encontraron flujos', { status: 404 });
  }

  const recentStreamId = streamIds.at(-1);

  if (!recentStreamId) {
    return new Response('No se encontró el flujo más reciente', { status: 404 });
  }

  const emptyDataStream = createDataStream({
    execute: () => {},
  });

  const stream = await streamContext.resumableStream(
    recentStreamId,
    () => emptyDataStream,
  );

  if (stream) {
    return new Response(stream, { status: 200 });
  }

  /*
   * Para cuando la generación está "activa" durante SSR pero el
   * flujo resumible ha concluido después de llegar a este punto.
   */

  const messages = await getMessagesByChatId({ id: chatId });
  const mostRecentMessage = messages.at(-1);
```

Si (!mostRecentMessage || mostRecentMessage.role !== 'assistant') {
    return new Response(emptyDataStream, { status: 200 });
  }

  const fechaDeCreacionDelMensaje = new Date(mostRecentMessage.createdAt);

  const streamConMensaje = createDataStream({
    execute: buffer => {
      buffer.writeData({
        type: 'append-message',
        message: JSON.stringify(mostRecentMessage),
      });
    },
  });

  return new Response(streamConMensaje, { status: 200 });
}

---

Después de implementar el manipulador `GET`, puedes actualizar el manipulador `POST` para manejar la creación de flujos resumibles.

### 2. Actualice el manejador POST

Cuando creas una nueva completación de chat, debes:

1. Generar un `streamId` fresco
2. Persistirlo junto con tu `chatId`
3. Iniciar un `createDataStream` que envíe tokens a medida que lleguen
4. Entregar ese nuevo flujo a `streamContext.resumableStream()`

```ts filename="app/api/chat/route.ts"
import {
  appendResponseMessages,
  createDataStream,
  generateId,
  streamText,
} from 'ai';
import { appendStreamId, saveChat } from '@/util/chat-store';
import { createResumableStreamContext } from 'resumable-stream';

const streamContext = createResumableStreamContext({
  waitUntil: after,
});

async function POST(request: Request) {
  const { id, messages } = await request.json();
  const streamId = generateId();

  // Registra este nuevo flujo para poder reanudarlo más tarde
  await appendStreamId({ chatId: id, streamId });

  // Construye el flujo de datos que emitirá tokens
  const stream = createDataStream({
    execute: dataStream => {
      const result = streamText({
        model: openai('gpt-4o'),
        messages,
        onFinish: async ({ response }) => {
          await saveChat({
            id,
            messages: appendResponseMessages({
              messages,
              responseMessages: response.messages,
            }),
          });
        },
      });

      // Devuelve un flujo reanudable al cliente
      result.mergeIntoDataStream(dataStream);
    },
  });
```

return new Response(
    await streamContext.resumableStream(streamId, () => stream),
  );
}

Con ambos manejadores, sus clientes pueden reanudar ahora flujos en curso de manera amigable.

---
titulo: Uso de Herramientas de Chatbot
descripcion: Aprenda a usar herramientas con la función useChat.
---

# Uso de la Herramienta de Chatbot

Con [`useChat`](/docs/reference/ai-sdk-ui/use-chat) y [`streamText`](/docs/reference/ai-sdk-core/stream-text), puedes utilizar herramientas en tu aplicación de chatbot.
El SDK de IA admite tres tipos de herramientas en este contexto:

1. Herramientas ejecutadas automáticamente en el servidor
2. Herramientas ejecutadas automáticamente en el cliente
3. Herramientas que requieren interacción del usuario, como diálogos de confirmación

El flujo es el siguiente:

1. El usuario ingresa un mensaje en la interfaz de chat.
1. El mensaje se envía a la ruta de API.
1. En tu ruta de servidor, el modelo de lenguaje genera llamadas a herramientas durante la llamada a `streamText`.
1. Todas las llamadas a herramientas se envían al cliente.
1. Las herramientas del servidor se ejecutan utilizando su método `execute` y sus resultados se envían al cliente.
1. Las herramientas del cliente que deben ejecutarse automáticamente se manejan con la callback `onToolCall`.
   Puedes devolver el resultado de la herramienta desde la callback.
1. Las herramientas del cliente que requieren interacción del usuario pueden ser mostradas en la interfaz.
   Las llamadas a herramientas y resultados están disponibles como partes de invocación de herramientas en la propiedad `parts` del último mensaje del asistente.
1. Cuando la interacción del usuario está completa, se puede utilizar `addToolResult` para agregar el resultado de la herramienta a la conversación.
1. Cuando hay llamadas a herramientas en el último mensaje del asistente y todos los resultados de herramientas están disponibles, el cliente envía los mensajes actualizados de vuelta al servidor.
   Esto desencadena otra iteración de este flujo.

Las llamadas a herramientas y ejecuciones de herramientas están integradas en el mensaje del asistente como partes de invocación de herramientas.
Una invocación de herramienta es al principio una llamada a herramienta, y luego se convierte en un resultado de herramienta cuando la herramienta se ejecuta.
El resultado de herramienta contiene toda la información sobre la llamada a herramienta así como el resultado de la ejecución de la herramienta.

<Nota>
  Para enviar automáticamente otra solicitud al servidor cuando todas las llamadas a herramientas sean del servidor, debes establecer
  [`maxSteps`](/docs/reference/ai-sdk-ui/use-chat#max-steps) en un valor mayor que 1 en las opciones de `useChat`.
  Está deshabilitado por defecto para compatibilidad hacia atrás.
</Nota>

## Ejemplo

En este ejemplo, utilizaremos tres herramientas:

- `getWeatherInformation`: Una herramienta de servidor ejecutada automáticamente que devuelve el clima de una ciudad determinada.
- `askForConfirmation`: Una herramienta de cliente de interacción con el usuario que solicita la confirmación del usuario.
- `getLocation`: Una herramienta de cliente ejecutada automáticamente que devuelve una ciudad aleatoria.

### Ruta de API

```tsx filename='app/api/chat/ruta.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { z } from 'zod';

// Permitir respuestas en streaming hasta 30 segundos
export const maxDuration = 30;

export async function POST(req: Request) {
  const { mensajes } = await req.json();
```

```markdown
const resultado = streamText({
    modelo: openai('gpt-4o'),
    mensajes,
    herramientas: {
      // Herramienta del lado del servidor con función de ejecución:
      obtenerInformaciónMeteorológica: {
        descripcion: 'muestra el clima en una ciudad determinada al usuario',
        parámetros: z.object({ ciudad: z.string() }),
        ejecutar: async ({}: { ciudad: string }) => {
          const opcionesMeteorológicas = ['sunny', 'cloudy', 'rainy', 'snowy', 'windy'];
          return opcionesMeteorológicas[
            Math.floor(Math.random() * opcionesMeteorológicas.length)
          ];
        },
      },
      // Herramienta del lado del cliente que inicia la interacción con el usuario:
      pedirConfirmación: {
        descripcion: 'Pide al usuario confirmación.',
        parámetros: z.object({
          mensaje: z.string().describe('El mensaje para pedir confirmación.'),
        }),
      },
      // Herramienta del lado del cliente que se ejecuta automáticamente en el cliente:
      obtenerUbicación: {
        descripcion:
          'Obtiene la ubicación del usuario. Siempre pide confirmación antes de usar esta herramienta.',
        parámetros: z.object({}),
      },
    },
  });

  return resultado.toDataStreamResponse();
}
```

### Página del lado del cliente

La página del lado del cliente utiliza el hook `useChat` para crear una aplicación de chatbot con transmisión de mensajes en tiempo real.
Las invocaciones de herramientas se muestran en la interfaz de chat como partes de invocación de herramientas.
Asegúrese de renderizar los mensajes utilizando la propiedad `parts` del mensaje.

Hay tres cosas que vale la pena mencionar:

1. El callback `onToolCall` se utiliza para manejar herramientas del lado del cliente que deben ejecutarse automáticamente.
   En este ejemplo, la herramienta `getLocation` es una herramienta del lado del cliente que devuelve una ciudad aleatoria.

2. La propiedad `toolInvocations` del último mensaje del asistente contiene todas las llamadas y resultados de herramientas.
   La herramienta del lado del cliente `askForConfirmation` se muestra en la UI.
   Preguntará al usuario por confirmación y mostrará el resultado una vez que el usuario confirme o niegue la ejecución.
   El resultado se agrega a la chat utilizando `addToolResult`.

3. La propiedad `maxSteps` se utiliza para limitar el número de pasos en la conversación.

# Opción `max-steps` está configurada en 5.
   Esto habilita varias iteraciones de uso de herramientas entre el cliente y el servidor.

```tsx filename='app/page.tsx' highlight="9,12,31"
'use client';

import { ToolInvocation } from 'ai';
import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, addToolResult } =
    useChat({
      maxSteps: 5,

      // ejecuta herramientas del lado del cliente que se ejecutan automáticamente:
      async onToolCall({ toolCall }) {
        if (toolCall.toolName === 'getLocation') {
          const cities = [
            'Nueva York',
            'Los Ángeles',
            'Chicago',
            'San Francisco',
          ];
          return cities[Math.floor(Math.random() * cities.length)];
        }
      },
    });

  return (
    <>
      {messages?.map(message => (
        <div key={message.id}>
          <strong>{`${message.role}: `}</strong>
          {message.parts.map(part => {
            switch (part.type) {
              // renderiza partes de texto como texto simple:
              case 'text':
                return part.text;
```

// para invocaciones de herramientas, distingue entre las herramientas y el estado:
              case 'tool-invocation': {
                const callId = part.toolInvocation.toolCallId;

```markdown
switch (part.toolInvocation.toolName) {
  caso 'askForConfirmation': {
    switch (part.toolInvocation.state) {
      caso 'call':
        return (
          <div key={callId}>
            {part.toolInvocation.args.message}
            <div>
              <button
                onClick={() =>
                  addToolResult({
                    toolCallId: callId,
                    result: 'Sí

>
                                Sí
                              </button>
                              <button
                                onClick={() =>
                                  addToolResult({
                                    toolCallId: callId,
                                    result: 'No, denegado',
                                  })
                                }
                              >
                                No
                              </button>
                           

</div>
                    );
                  case 'result':
                    return (
                      <div key={callId}>
                        El acceso a la ubicación está permitido: {' '}
                        {part.toolInvocation.result}
                      </div>
                    );
                }
                break;

caso 'getLocation': {
                    switch (part.toolInvocation.state) {
                      caso 'call':
                        return <div key={callId}>Obteniendo ubicación...</div>;
                      caso 'result':
                        return (
                          <div key={callId}>
                            Ubicación: {part.toolInvocation.result}
                          </div>
                        );
                    }
                    break;


caso 'obtenerInformaciónDelClima': {
  switch (part.toolInvocation.state) {
    // ejemplo de llamadas de herramientas de streaming de pre-rendering:
    caso 'llamada-parcial':
      return (
        <pre key={callId}>
          {JSON.stringify(part.toolInvocation, null, 2)}
        </pre>
      );
    caso 'llamada':
      return (
        <div key={callId}>
          Está obteniendo la información del clima para{' '}
          {part.toolInvocation.args

caso 'result':
  regresa (
    <div key={callId}>
      El clima en {part.toolInvocation.args.ciudad}:{' '}
      {part.toolInvocation.result}
    </div>
  );
  break;
}
break;
}

}

}

</div>
</div>

<form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
</>
);

## Llamadas a herramientas en streaming

Puedes transmitir llamadas a herramientas mientras se están generando habilitando la opción `toolCallStreaming` en `streamText`.

```tsx filename='app/api/chat/route.ts' highlight="5"
export async function POST(req: Request) {
  // ...

  const result = streamText({
    toolCallStreaming: true,
    // ...
  });

  return result.toDataStreamResponse();
}
```

Cuando la bandera está habilitada, las llamadas a herramientas parciales se transmitirán como parte del flujo de datos.
Están disponibles a través de la función de hook `useChat`.
Las partes de invocación de herramientas de mensajes de asistente también contendrán llamadas a herramientas parciales.
Puedes utilizar la propiedad `state` de la invocación de herramienta para renderizar la interfaz de usuario correcta.

```tsx filename='app/page.tsx' highlight="9,10"
export default function Chat() {
  // ...
  return (
    <>
      {messages?.map(message => (
        <div key={message.id}>
          {message.parts.map(part => {
            if (part.type === 'invocación-de-herramienta') {
              switch (part.invocaciónDeHerramienta.estado) {
                case 'llamada-parcial':
                  return <>render llamada parcial de herramienta</>;
                case 'llamada':
                  return <>render llamada completa de herramienta</>;
                case 'resultado':
                  return <>render resultado de herramienta</>;
              }
            }
          })}
        </div>
      ))}
    </>
  );
}
```

## Pasos iniciales de partes

Cuando se utilizan llamadas de herramientas en varias etapas, el SDK de IA agregará partes de inicio de paso a los mensajes del asistente.
Si deseas mostrar límites entre las invocaciones de herramientas, puedes utilizar las partes `step-start` de la siguiente manera:

```tsx filename='app/page.tsx'
// ...
// donde renderizas las partes del mensaje:
message.parts.map((part, index) => {
  switch (part.type) {
    case 'step-start':
      // muestra límites de paso como líneas horizontales:
      return index > 0 ? (
        <div key={index} className="text-gray-500">
          <hr className="my-2 border-gray-300" />
        </div>
      ) : null;
    case 'text':
    // ...
    case 'tool-invocation':
    // ...
  }
});
// ...
```

## Llamadas Multi-Pasos en Servidor

También puedes utilizar llamadas multi-pasos en el lado del servidor con `streamText`.
Esto funciona cuando todos los herramientas invocadas tienen una función `execute` en el lado del servidor.

```tsx filename='app/api/chat/route.ts' highlight="15-21,24"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    herramientas: {
      obtenerInformaciónMeteorológica: {
        descripcion: 'muestra el clima en una ciudad determinada al usuario',
        parámetros: z.object({ ciudad: z.string() }),
        // herramienta tiene función execute:
        execute: async ({}: { ciudad: string }) => {
          const opcionesDelClima = ['sunny', 'cloudy', 'rainy', 'snowy', 'windy'];
          return opcionesDelClima[
            Math.floor(Math.random() * opcionesDelClima.length)
          ];
        },
      },
    },
    maxPasos: 5,
  });

  return result.toDataStreamResponse();
}
```

## Errores

Los modelos de lenguaje pueden cometer errores al llamar herramientas.
Por defecto, estos errores están ocultos por razones de seguridad y se muestran como "Ocurrió un error" en la interfaz de usuario.

Para mostrar los errores, puedes utilizar la función `getErrorMessage` cuando llames a `toDataStreamResponse`.

```tsx
export function errorHandler(error: unknown) {
  if (error == null) {
    return 'error desconocido';
  }

  if (typeof error === 'string') {
    return error;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return JSON.stringify(error);
}
```

```tsx
const result = streamText({
  // ...
});

return result.toDataStreamResponse({
  getErrorMessage: errorHandler,
});
```

En caso de que estés utilizando `createDataStreamResponse`, puedes utilizar la función `onError` cuando llames a `toDataStreamResponse`:

```tsx
const response = createDataStreamResponse({
  // ...
  async execute(dataStream) {
    // ...
  },
  onError: error => `Error personalizado: ${error.message}`,
});
```

---
titulo: Interfaces de usuario generativas
descripcion: Aprende a construir UI generativas con el SDK de IA UI.
---

# Interfaces de Usuario Generativos

Las interfaces de usuario generativas (generative UI) son el proceso de permitir a un modelo de lenguaje grande (LLM) ir más allá del texto y "generar UI". Esto crea una experiencia más atractiva y nativa de IA para los usuarios.

<WeatherSearch />

En el núcleo de las interfaces de usuario generativas están [ herramientas ](/docs/ai-sdk-core/tools-and-tool-calling), que son funciones que proporcionas al modelo para realizar tareas especializadas como obtener el clima en una ubicación. El modelo puede decidir cuándo y cómo utilizar estas herramientas en función del contexto de la conversación.

Las interfaces de usuario generativas son el proceso de conectar los resultados de una llamada a herramientas a un componente de React. Aquí está cómo funciona:

1. Proporcionas al modelo una solicitud o historia de conversación, junto con un conjunto de herramientas.
2. Basándose en el contexto, el modelo puede decidir llamar a una herramienta.
3. Si se llama a una herramienta, se ejecutará y devolverá datos.
4. Estos datos pueden entonces pasar a un componente de React para su renderizado.

Al pasar los resultados de las herramientas a componentes de React, puedes crear una experiencia de interfaz de usuario generativa que sea más atractiva y adaptable a tus necesidades.

## Construye una Interfaz de Chat de UI Generativa

Vamos a crear una interfaz de chat que maneje conversaciones de texto y incorpore elementos de UI dinámicos basados en respuestas del modelo.

### Implementación básica de chat

Comienza con una implementación básica de chat utilizando el hook `useChat`:

```tsx filename="app/page.tsx"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Página() {
  const { mensajes, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div>
      {mensajes.map(mensaje => (
        <div key={mensaje.id}>
          <div>{mensaje.role === 'user' ? 'Usuario: ' : 'IA: '}</div>
          <div>{mensaje.content}</div>
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Escribe un mensaje..."
        />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}
```

Para manejar las solicitudes de chat y las respuestas del modelo, configura una ruta de API:

```ts filename="app/api/chat/route.ts"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(request: Request) {
  const { mensajes } = await request.json();

  const resultado = streamText({
    modelo: openai('gpt-4o'),
    sistema: 'Usted es un asistente amigable!',
    mensajes,
    maxPasos: 5,
  });

  return resultado.toDataStreamResponse();
}
```

Esta ruta de API utiliza la función `streamText` para procesar mensajes de chat y enviar las respuestas del modelo de vuelta al cliente.

### Crear una Herramienta

Antes de mejorar la interfaz de chat con elementos UI dinámicos, necesitas crear una herramienta y el componente de React correspondiente. Una herramienta permitirá al modelo realizar una acción específica, como obtener información de clima.

Crea un nuevo archivo llamado `ai/tools.ts` con el siguiente contenido:

```ts filename="ai/tools.ts"
import { tool as createTool } from 'ai';
import { z } from 'zod';

export const weatherTool = createTool({
  description: 'Mostrar el clima para una ubicación',
  parameters: z.object({
    location: z.string().describe('La ubicación para obtener el clima'),
  }),
  execute: async function ({ location }) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    return { weather: 'Soleado', temperatura: 75, location };
  },
});

export const herramientas = {
  mostrarClima: weatherTool,
};
```

En este archivo, has creado una herramienta llamada `weatherTool`. Esta herramienta simula obtener información de clima para una ubicación dada. Esta herramienta devolverá datos simulados después de un retraso de 2 segundos. En una aplicación real, reemplazarías esta simulación con una llamada real a una API de servicio de clima.

### Actualizar la Ruta de la API

Actualiza la ruta de la API para incluir la herramienta que has definido:

```ts filename="app/api/chat/route.ts" highlight="3,13"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { herramientas } from '@/ai/tools';

export async function POST(request: Request) {
  const { mensajes } = await request.json();

  const resultado = streamText({
    modelo: openai('gpt-4o'),
    sistema: 'Eres un asistente amigable!',
    mensajes,
    maxPasos: 5,
    herramientas,
  });

  return resultado.toDataStreamResponse();
}
```

Ahora que has definido la herramienta y la has agregado a tu llamada a `streamText`, vamos a crear un componente de React para mostrar la información de clima que devuelve.

### Crear Componentes de Interfaz de Usuario

Crea un nuevo archivo llamado `components/weather.tsx`:

```tsx filename="components/weather.tsx"
type WeatherProps = {
  temperatura: number;
  clima: string;
  ubicación: string;
};

export const Weather = ({ temperatura, clima, ubicación }: WeatherProps) => {
  return (
    <div>
      <h2>Actualidad del Clima para {ubicación}</h2>
      <p>Condición: {clima}</p>
      <p>Temperatura: {temperatura}°C</p>
    </div>
  );
};
```

Este componente mostrará la información del clima para una ubicación determinada. Recibe tres props: `temperatura`, `clima`, y `ubicación` (exactamente lo que devuelve `weatherTool`).

### Render el Componente del Clima

Ahora que tienes tu herramienta y el componente de React correspondiente, intégralos en tu interfaz de chat. Renderizarás el componente del clima cuando el modelo invoque la herramienta del clima.

Para verificar si el modelo ha llamado a una herramienta, puedes utilizar la propiedad `toolInvocations` del objeto de mensaje. Esta propiedad contiene información sobre cualquier herramienta que se haya invocado en esa generación, incluyendo `toolCallId`, `toolName`, `args`, `toolState`, y `result`.

Actualiza tu archivo `page.tsx`:

```tsx filename="app/page.tsx" highlight="4,16-39"
'use client';

import { useChat } from '@ai-sdk/react';
import { Weather } from '@/components/weather';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          <div>{message.role === 'user' ? 'Usuario: ' : 'IA: '}</div>
          <div>{message.content}</div>

          <div>
            {message.toolInvocations?.map(toolInvocation => {
              const { toolName, toolCallId, state } = toolInvocation;
```

Si (estado === 'resultado') {
  Si (nombreDeHerramienta === 'mostrarClima') {
    const { resultado } = herramientaDeInvocación;
    return (
      <div clave={llamadaAToolId}>
        <Clima {...resultado} />
      </div>
    );
  }
} else {
  return (
    <div clave={llamadaAToolId}>
      {nombreDeHerramienta === 'mostrarClima' ? (
        <div>Cargando clima...</div>
      ) : null}
    </div>
  );
}
})}

<form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Escribe un mensaje..."
        />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}
```

En este fragmento de código actualizado, se realizan las siguientes acciones:

1. Se verifica si el mensaje tiene `toolInvocations`.
2. Se verifica si el estado de la invocación de herramienta es 'result'.
3. Si es un resultado y el nombre de la herramienta es 'displayWeather', se renderiza el componente Weather.
4. Si el estado de la invocación de herramienta no es 'result', se muestra un mensaje de carga.

Este enfoque permite renderizar componentes de interfaz de usuario de manera dinámica según las respuestas del modelo, lo que crea una experiencia de chat más interactiva y consciente del contexto.

## Ampliando Tu Aplicación de UI Generativa

Puedes mejorar tu aplicación de chat agregando más herramientas y componentes, creando una experiencia de usuario más rica y versátil. Aquí te mostramos cómo puedes ampliar tu aplicación:

---

### 1. Agregar Funcionalidades de Moderación

Puedes agregar funcionalidades de moderación para que los administradores puedan controlar el contenido de la conversación y mantener un ambiente

### Agregando Más Herramientas

Para agregar más herramientas, simplemente defínalas en tu archivo `ai/tools.ts`:

```ts
// Agrega una nueva herramienta de acciones bursátiles
export const stockTool = createTool({
  description: 'Obtén el precio de una acción',
  parameters: z.object({
    symbol: z.string().describe('El símbolo de la acción para obtener el precio'),
  }),
  execute: async function ({ symbol }) {
    // Llamada simulada a la API
    await new Promise(resolve => setTimeout(resolve, 2000));
    return { symbol, price: 100 };
  },
});

// Actualiza el objeto de herramientas
export const tools = {
  displayWeather: weatherTool,
  getStockPrice: stockTool,
};
```

Ahora, crea un nuevo archivo llamado `components/stock.tsx`:

```tsx
type StockProps = {
  price: number;
  symbol: string;
};

export const Stock = ({ price, symbol }: StockProps) => {
  return (
    <div>
      <h2>Información de la Acción</h2>
      <p>Símbolo: {symbol}</p>
      <p>Precio: ${price}</p>
    </div>
  );
};
```

Finalmente, actualiza tu archivo `page.tsx` para incluir el nuevo componente Stock:

```tsx
'use client';

import { useChat } from '@ai-sdk/react';
import { Weather } from '@/components/weather';
import { Stock } from '@/components/stock';

export default function Page() {
  const { messages, input, setInput, handleSubmit } = useChat();

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          <div>{message.role}</div>
          <div>{message.content}</div>
```

<div>
            {message.toolInvocations?.map(toolInvocation => {
              const { nombreDelHerramienta, idDeLaLlamadaDelHerramienta,

Si (`state === 'result'`) {
  Si (`toolName === 'displayWeather'`) {
    const { result } = toolInvocation;
    return (
      <div key={toolCallId}>
        <Weather {...result} />
      </div>
    );
  } else if (`toolName === 'getStockPrice'`) {
    const { result } = toolInvocation;
    return <Stock key={toolCallId} {...result} />;
  }
} else {
  return (
    <div key={toolCallId}>
      {toolName === 'displayWeather' ? (
        <div>Cargando el clima...</div>
      ) : toolName === 'getStockPrice' ? (
        <div>Cargando el precio de la acción...</div>
      ) : (
        <div> </div>
      )
    }
  );
}

<div>Cargando...</div>
                    )}
                  </div>
                );
              }
            })}
          </div>
        </div>


<form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={event => {
            setInput(event.target.value);
          }}
        />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}
```

Siguiendo este patrón, puede seguir agregando más herramientas y componentes, ampliando las capacidades de su aplicación de UI Generativa.

---
titulo: Completar
descripcion: Aprenda a utilizar la hook useCompletion.
---

# Completación

El hook `useCompletion` te permite crear una interfaz de usuario para manejar las completaciones de texto en tu aplicación. Permite la transmisión en streaming de las completaciones de texto desde tu proveedor de inteligencia artificial, gestiona el estado para la entrada de chat y actualiza la interfaz de usuario automáticamente a medida que se reciben nuevos mensajes.

En esta guía, aprenderás a utilizar el hook `useCompletion` en tu aplicación para generar completaciones de texto y transmitirlas en tiempo real a tus usuarios.

## Ejemplo

```tsx filename='app/page.tsx'
'use client';

import { useCompletion } from '@ai-sdk/react';

export default function Page() {
  const { completion, input, handleInputChange, handleSubmit } = useCompletion({
    api: '/api/completion',
  });

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="prompt"
        value={input}
        onChange={handleInputChange}
        id="input"
      />
      <button type="submit">Enviar</button>
      <div>{completion}</div>
    </form>
  );
}
```

```ts filename='app/api/completion/route.ts'
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

// Permitir streaming de respuestas hasta 30 segundos
export const maxDuration = 30;

export async function POST(req: Request) {
  const { prompt }: { prompt: string } = await req.json();

  const result = streamText({
    model: openai('gpt-3.5-turbo'),
    prompt,
  });

  return result.toDataStreamResponse();
}
```

En el componente `Page`, el hook `useCompletion` solicitará a su proveedor de inteligencia artificial el endpoint cada vez que el usuario envíe un mensaje. La completación se devuelve en tiempo real y se muestra en la interfaz de usuario.

Esto permite una experiencia de completación de texto fluida donde el usuario puede ver la respuesta del AI en cuanto esté disponible, sin tener que esperar a que se reciba toda la respuesta.

## Interfaz de usuario personalizada

`useCompletion` también proporciona formas de gestionar el prompt mediante código, mostrar estados de carga y de error, y actualizar mensajes sin que se active mediante interacciones del usuario.

### Estados de carga y errores

Para mostrar un spinner de carga mientras el chatbot procesa el mensaje del usuario, puedes utilizar el estado `isLoading` devuelto por la función de hook `useCompletion`:

```tsx
const { isLoading, ... } = useCompletion()

return(
  <>
    {isLoading ? <Spinner /> : null}
  </>
)
```

De manera similar, el estado `error` refleja el objeto de error lanzado durante la solicitud de fetch. Puedes utilizarlo para mostrar un mensaje de error, o mostrar una notificación de toast:

```tsx
const { error, ... } = useCompletion()

useEffect(() => {
  if (error) {
    toast.error(error.message)
  }
}, [error])

// O mostrar el mensaje de error en la interfaz de usuario:
return (
  <>
    {error ? <div>{error.message}</div> : null}
  </>
)
```

### Entrada controlada

En el ejemplo inicial, tenemos las llamadas a `handleSubmit` y `handleInputChange` que gestionan los cambios de entrada y las submission de formularios. Estas son útiles para casos de uso comunes, pero también puedes utilizar APIs no controladas para escenarios más avanzados, como la validación de formularios o componentes personalizados.

El siguiente ejemplo muestra cómo utilizar APIs más granulares como `setInput` con tus componentes de entrada personalizados y botón de submit:

```tsx
const { input, setInput } = useCompletion();

return (
  <>
    <MyCustomInput value={input} onChange={value => setInput(value)} />
  </>
);
```

### Cancelación

También es un caso de uso común abortar el mensaje de respuesta mientras aún está en streaming desde el proveedor AI. Puedes hacer esto llamando a la función `stop` devuelta por el hook `useCompletion`.

```tsx
const { stop, isLoading, ... } = useCompletion()

return (
  <>
    <button onClick={stop} disabled={!isLoading}>Detener</button>
  </>
)
```

Cuando el usuario hace clic en el botón "Detener", la solicitud de fetch se abortará. Esto evita consumir recursos innecesarios y mejora la experiencia del usuario de tu aplicación.

### Ralentización de Actualizaciones de UI

<Nota>Esta función es actualmente solo disponible para React.</Nota>

Por defecto, el hook `useCompletion` desencadenará una renderización cada vez que se reciba un nuevo trozo.
Puedes ralentizar las actualizaciones de UI con la opción `experimental_throttle`.

```tsx filename="page.tsx" highlight="2-3"
const { completion, ... } = useCompletion({
  // Ralentiza la actualización de la completación y los datos a 50ms:
  experimental_throttle: 50
})
```

## Llamadas de Evento

`useCompletion` también proporciona llamadas de evento opcionales que puedes utilizar para manejar diferentes etapas del ciclo de vida del chatbot. Estas llamadas de evento se pueden utilizar para desencadenar acciones adicionales, como el registro, las métricas, o actualizaciones de UI personalizadas.

```tsx
const { ... } = useCompletion({
  onResponse: (response: Response) => {
    console.log('Se recibió la respuesta del servidor:', response)
  },
  onFinish: (message: Message) => {
    console.log('Se completó la transmisión del mensaje:', message)
  },
  onError: (error: Error) => {
    console.error('Ocurrió un error:', error)
  },
})
```

Es importante tener en cuenta que puedes abortar el procesamiento lanzando una excepción en la llamada de evento `onResponse`. Esto desencadenará la llamada de evento `onError` y detendrá el mensaje de ser agregado a la interfaz de chat. Esto puede ser útil para manejar respuestas inesperadas del proveedor AI.

## Configurar Opciones de Solicitud

Por defecto, el hook `useCompletion` envía una solicitud HTTP POST a la ruta `/api/completion` con el prompt como parte del cuerpo de la solicitud. Puedes personalizar la solicitud pasando opciones adicionales al hook `useCompletion`:

```tsx
const { messages, input, handleInputChange, handleSubmit } = useCompletion({
  api: '/api/completado-personalizado',
  headers: {
    Authorization: 'tu_token',
  },
  body: {
    user_id: '123',
  },
  credentials: 'same-origin',
});
```

En este ejemplo, el hook `useCompletion` envía una solicitud POST a la ruta `/api/completado` con los encabezados, campos adicionales del cuerpo y credenciales especificados para esa solicitud de fetch. En el lado del servidor, puedes manejar la solicitud con esta información adicional.

---
title: Generación de Objetos
description: Aprende a usar el hook `useObject`.
---

# Generación de Objetos

<Nota>`useObject` es una característica experimental y solo está disponible en React.</Nota>

El hook [`useObject`](/docs/reference/ai-sdk-ui/use-object) te permite crear interfaces que representen un objeto JSON estructurado que se está transmitiendo.

En esta guía, aprenderás a usar el hook `useObject` en tu aplicación para generar UIs para datos estructurados en tiempo real.

## Ejemplo

El ejemplo muestra una pequeña aplicación de demostración de notificaciones que genera notificaciones falsas en tiempo real.

### Esquema

Es útil configurar el esquema en un archivo separado que se importa tanto en el lado del cliente como en el lado del servidor.

```ts filename='app/api/notifications/schema.ts'
import { z } from 'zod';

// define un esquema para las notificaciones
export const notificationSchema = z.object({
  notifications: z.array(
    z.object({
      name: z.string().describe('Nombre de una persona ficticia.'),
      message: z.string().describe('Mensaje. No utilices emojis o enlaces.'),
    }),
  ),
});
```

### Cliente

El cliente utiliza [`useObject`](/docs/reference/ai-sdk-ui/use-object) para transmitir el proceso de generación del objeto.

Los resultados son parciales y se muestran según se reciben.
Tenga en cuenta el código para manejar valores `undefined` en JSX.

```tsx filename='app/page.tsx'
'use client';

import { experimental_useObject as useObject } from '@ai-sdk/react';
import { notificationSchema } from './api/notifications/schema';

export default function Page() {
  const { object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <>
      <button onClick={() => submit('Mensajes durante la semana de exámenes.')}>
        Generar notificaciones
      </button>

      {object?.notifications?.map((notification, index) => (
        <div key={index}>
          <p>{notification?.name}</p>
          <p>{notification?.message}</p>
        </div>
      ))}
    </>
  );
}
```

### Servidor

En el servidor, utilizamos [`streamObject`](/docs/reference/ai-sdk-core/stream-object) para transmitir el proceso de generación de objetos.

```typescript filename='app/api/notifications/route.ts'
import { openai } from '@ai-sdk/openai';
import { streamObject } from 'ai';
import { notificationSchema } from './schema';

// Se permite la transmisión de respuestas durante un máximo de 30 segundos
export const maxDuration = 30;

export async function POST(req: Request) {
  const contexto = await req.json();

  const resultado = streamObject({
    modelo: openai('gpt-4-turbo'),
    schema: notificationSchema,
    prompt:
      `Generar 3 notificaciones para una aplicación de mensajes en este contexto:` + contexto,
  });

  return resultado.toTextStreamResponse();
}
```

## Interfaz personalizada

`useObject` también proporciona formas de mostrar estados de carga y de error:

### Estado de Carga

El estado `isLoading` devuelto por el hook `useObject` se puede utilizar para varios fines:

- Mostrar un indicador de carga mientras el objeto se genera.
- Deshabilitar el botón de enviar.

```tsx filename='app/page.tsx' highlight="6,13-20,24"
'use client';

import { useObject } from '@ai-sdk/react';

export default function Page() {
  const { isLoading, object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <>
      {isLoading && <Spinner />}

      <button
        onClick={() => submit('Mensajes durante la semana de exámenes finales.')}
        disabled={isLoading}
      >
        Generar notificaciones
      </button>

      {object?.notifications?.map((notification, index) => (
        <div key={index}>
          <p>{notification?.name}</p>
          <p>{notification?.message}</p>
        </div>
      ))}
    </>
  );
}
```

### Manejador de parada

La función `stop` se puede utilizar para detener el proceso de generación de objetos. Esto puede ser útil si el usuario quiere cancelar la solicitud o si el servidor está tardando demasiado en responder.

```tsx filename='app/page.tsx' highlight="6,14-16"
'use client';

import { useObject } from '@ai-sdk/react';

export default function Page() {
  const { isLoading, stop, object, submit } = useObject({
    api: '/api/notificaciones',
    schema: notificationSchema,
  });

  return (
    <>
      {isLoading && (
        <button type="button" onClick={() => stop()}>
          Detener
        </button>
      )}

      <button onClick={() => submit('Mensajes durante la semana de exámenes.')}>
        Generar notificaciones
      </button>

      {object?.notificaciones?.map((notificación, index) => (
        <div key={index}>
          <p>{notificación?.nombre}</p>
          <p>{notificación?.mensaje}</p>
        </div>
      ))}
    </>
  );
}
```

### Estado de Error

De manera similar, el estado `error` refleja el objeto de error lanzado durante la solicitud de fetch.
Puede utilizarse para mostrar un mensaje de error o para deshabilitar el botón de envío:

<Nota>
  Recomendamos mostrar un mensaje de error genérico al usuario, como "Algo salió mal."
  Esta es una buena práctica para evitar revelar información del servidor.
</Nota>

```tsx file="app/page.tsx" highlight="6,13"
'use client';

import { useObject } from '@ai-sdk/react';

export default function Page() {
  const { error, object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <>
      {error && <div>Se produjo un error.</div>}

      <button onClick={() => submit('Mensajes durante la semana de exámenes.')}>
        Generar notificaciones
      </button>

      {object?.notifications?.map((notification, index) => (
        <div key={index}>
          <p>{notification?.name}</p>
          <p>{notification?.message}</p>
        </div>
      ))}
    </>
  );
}
```

## Eventos de Devolución de Llamada

`useObject` proporciona devoluciones de llamada opcionales que puedes utilizar para manejar eventos de ciclo de vida.

- `onFinish`: Se llama cuando la generación del objeto está completada.
- `onError`: Se llama cuando ocurre un error durante la solicitud de fetch.

Estas devoluciones de llamada se pueden utilizar para desencadenar acciones adicionales, como registro, análisis o actualizaciones de interfaz de usuario personalizadas.

```tsx filename='app/page.tsx' highlight="10-20"
'use client';

import { experimental_useObject as useObject } from '@ai-sdk/react';
import { notificationSchema } from './api/notifications/schema';

export default function Page() {
  const { object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
    onFinish({ object, error }) {
      // objeto tipado, indefinido si la validación de schema falla:
      console.log('La generación del objeto está completada:', object);

      // error, indefinido si la validación de schema es exitosa:
      console.log('Error de validación de schema:', error);
    },
    onError(error) {
      // error durante la solicitud de fetch:
      console.error('Ocurrió un error:', error);
    },
  });

  return (
    <div>
      <button onClick={() => submit('Mensajes durante la semana de exámenes.')}>
        Generar notificaciones
      </button>

      {object?.notifications?.map((notification, index) => (
        <div key={index}>
          <p>{notification?.name}</p>
          <p>{notification?.message}</p>
        </div>
      ))}
    </div>
  );
}
```

## Configurar Opciones de Solicitud

Puedes configurar el punto final de la API, encabezados opcionales y credenciales utilizando las configuraciones `api`, `headers` y `credentials`.

```tsx highlight="2-5"
const { submit, object } = useObject({
  api: '/api/use-object',
  headers: {
    'X-Custom-Header': 'CustomValue',
  },
  credentials: 'include',
  schema: yourSchema,
});
```

---
title: Asistentes de OpenAI
description: Aprende a utilizar la función de hook `useAssistant`.
---

# Asistentes de OpenAI

La función de hook `useAssistant` te permite manejar el estado del cliente al interactuar con una API compatible con asistentes de OpenAI.
Esta función de hook es útil cuando deseas integrar capacidades de asistentes en tu aplicación,
con la interfaz de usuario actualizada automáticamente a medida que el asistente transmite su ejecución.

La función de hook `useAssistant` se admite en `@ai-sdk/react`, `ai/svelte` y `ai/vue`.

## Ejemplo

```tsx filename='app/page.tsx'
'use client';

import { Message, useAssistant } from '@ai-sdk/react';

export default function Chat() {
  const { status, messages, input, submitMessage, handleInputChange } =
    useAssistant({ api: '/api/assistant' });

  return (
    <div>
      {messages.map((m: Message) => (
        <div key={m.id}>
          <strong>{`${m.role}: `}</strong>
          {m.role !== 'data' && m.content}
          {m.role === 'data' && (
            <>
              {(m.data as any).description}
              <br />
              <pre className={'bg-gray-200'}>
                {JSON.stringify(m.data, null, 2)}
              </pre>
            </>
          )}
        </div>
      ))}

      {status === 'in_progress' && <div />}
    </div>
  );
}
```

```jsx
<form onSubmit={submitMessage}>
        <input
          disabled={estatus !== 'esperando_mensaje'}
          value={input}
          placeholder="¿Cuál es la temperatura en el salón?"
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
```

```tsx filename='app/api/assistant/route.ts'
import { AssistantResponse } from 'ai';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || '',
});

// Permitir streaming de respuestas hasta 30 segundos
export const maxDuration = 30;

export async function POST(req: Request) {
  // Parsear el cuerpo de la solicitud
  const input: {
    threadId: string | null;
    message: string;
  } = await req.json();

  // Crear un hilo si es necesario
  const threadId = input.threadId ?? (await openai.beta.threads.create({})).id;

  // Agregar un mensaje al hilo
  const createdMessage = await openai.beta.threads.messages.create(threadId, {
    role: 'user',
    content: input.message,
  });
```

`return AssistantResponse(
    { threadId, messageId: createdMessage.id },
    async ({ forwardStream, sendDataMessage }) => {
      // Ejecuta el asistente en el hilo
      const runStream = openai.beta.threads.runs.stream(threadId, {
        assistant_id:
          process.env.ASSISTANT_ID ??
          (() => {
            throw new Error('ASSISTANT_ID no está configurado');
          })(),
      });

      // El estado de ejecución se puede transmitir mediante mensajes delta
      let runResult = await forwardStream(runStream);

      // El estado puede ser: en cola, en progreso, requiere acción, cancelando, cancelado, fallido, completado o expirado
      while (
        runResult?.status === 'requiere_acción' &&
        runResult.required_action?.type === 'enviar_salidas_de_herramienta'
      ) {
        const tool_outputs =
          runResult.required_action.submit_tool_outputs.tool_calls.map(
            (toolCall: any) => {
              const parameters = JSON.parse(toolCall.function.arguments);

              switch (toolCall.function.name) {
                // configura tus llamadas a herramientas aquí
`
 
Note: I translated 'requires_action' to 'requiere_acción', 'submit_tool_outputs' to 'enviar_salidas_de_herramienta', and 'tool_calls' to 'llam

```markdown
# default
            lanzar new Error(
              `La función de llamada de herramienta desconocida: ${toolCall.function.name}`,
            );
          }
        },
      );

      resultadoDeEjecución = await forwardStream(
        openai.beta.threads.runs.submitToolOutputsStream(
          threadId,
          resultadoDeEjecución.id,
          { tool_outputs },
        ),
      );
    }
  );
}


## Interfaz Personalizada

`useAssistant` también proporciona formas de gestionar los estados de mensajes de chat y de entrada mediante código y mostrar estados de carga y errores.

### Estados de carga y errores

Para mostrar un indicador de carga mientras el asistente está ejecutando el hilo, puedes utilizar el estado `status` devuelto por el hook `useAssistant`:

```tsx
const { status, ... } = useAssistant()

return(
  <>
    {status === "in_progress" ? <Spinner /> : null}
  </>
)
```

De manera similar, el estado `error` refleja el objeto de error lanzado durante la solicitud de fetch. Puedes utilizarlo para mostrar un mensaje de error, o mostrar una notificación de toast:

```tsx
const { error, ... } = useAssistant()

useEffect(() => {
  if (error) {
    toast.error(error.message)
  }
}, [error])

// O mostrar el mensaje de error en la interfaz de usuario:
return (
  <>
    {error ? <div>{error.message}</div> : null}
  </>
)
```

### Entrada controlada

En el ejemplo inicial, tenemos las funciones de llamada a `handleSubmit` y `handleInputChange` que gestionan los cambios de entrada y las presentaciones de formulario. Estas son útiles para casos de uso comunes, pero también puedes utilizar APIs no controladas para escenarios más avanzados como la validación de formularios o componentes personalizados.

El siguiente ejemplo demuestra cómo utilizar APIs más granulares como `append` con tus componentes de entrada y botón de envío personalizados:

```tsx
const { append } = useAssistant();

return (
  <>
    <MiBotonDeEnvio
      onClick={() => {
        // Envía un nuevo mensaje al proveedor de IA
        append({
          role: 'user',
          content: input,
        });
      }}
    />
  </>
);
```

## Configurar Opciones de Solicitud

Por defecto, el hook `useAssistant` envía una solicitud HTTP POST a la ruta `/api/assistant` con el prompt como parte del cuerpo de la solicitud. Puedes personalizar la solicitud pasando opciones adicionales al hook `useAssistant`:

```tsx
const { messages, input, handleInputChange, handleSubmit } = useAssistant({
  api: '/api/completación-custodia',
  headers: {
    Authorization: 'tu_token',
  },
  body: {
    user_id: '123',
  },
  credentials: 'same-origin',
});
```

En este ejemplo, el hook `useAssistant` envía una solicitud POST a la ruta `/api/completación-custodia` con los encabezados, campos del cuerpo adicional y credenciales especificados para esa solicitud de fetch. En el lado del servidor, puedes manejar la solicitud con esta información adicional.

---
titulo: Transmisión de Datos Personalizados
descripcion: Aprende a transmitir datos personalizados al cliente.
---

# Transmisión de Datos Personalizados

A menudo es útil enviar datos adicionales junto con la respuesta del modelo.
Por ejemplo, puedes enviar información de estado, los ids de mensaje después de almacenarlos,
o referencias a contenido que el modelo de lenguaje se refiere a.

El SDK de IA proporciona varios ayudantes que permiten transmitir datos adicionales al cliente
y adjuntarlos a la `Message` o al objeto `data` del hook `useChat`:

- `createDataStream`: crea un flujo de datos
- `createDataStreamResponse`: crea un objeto de respuesta que transmite datos
- `pipeDataStreamToResponse`: envía un flujo de datos a un objeto de respuesta del servidor

Los datos se transmiten como parte del flujo de respuesta.

## Enviar Datos Personalizados desde el Servidor

En tu manejador de rutas del lado del servidor, puedes utilizar `createDataStreamResponse` y `pipeDataStreamToResponse` en combinación con `streamText`.
Necesitas:

1. Llamar a `createDataStreamResponse` o `pipeDataStreamToResponse` para obtener una función de llamada con un `DataStreamWriter`.
2. Escribe en el `DataStreamWriter` para enviar datos adicionales.
3. Mezclar el resultado de `streamText` en el `DataStreamWriter`.
4. Devolver la respuesta desde `createDataStreamResponse` (si se utiliza ese método)

Aquí hay un ejemplo:

```tsx filename="route.ts" highlight="7-10,16,19-23,25-26,30"
import { openai } from '@ai-sdk/openai';
import { generateId, createDataStreamResponse, streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  // inicia la transmisión de datos de manera inmediata (resuelve problemas de RAG con el estado, etc.)
  return createDataStreamResponse({
    execute: dataStream => {
      dataStream.writeData('llamada inicializada');

      const result = streamText({
        model: openai('gpt-4o'),
        messages,
        onChunk() {
          dataStream.writeMessageAnnotation({ chunk: '123' });
        },
        onFinish() {
          // anotación de mensaje:
          dataStream.writeMessageAnnotation({
            id: generateId(), // e.g. id desde el registro guardado en la base de datos
            other: 'información',
          });

          // anotación de llamada:
          dataStream.writeData('llamada completada');
        },
      });
```

`result.mergeIntoDataStream(dataStream);`,
},
onError: error => {
  // Los mensajes de error están ocultos por defecto por razones de seguridad.
  // Si deseas exponer el mensaje de error al cliente, puedes hacerlo aquí:
  return error instanceof Error ? error.message : String(error);
},
});

<Nota>
  También puedes enviar datos de flujo desde backends personalizados, por ejemplo Python / FastAPI,
  utilizando el [Protocolo de Flujo de Datos](/docs/ai-sdk-ui/stream-protocol)

# Protocolo de datos de flujo).

</Note>

## Enviar fuentes personalizadas

Puedes enviar fuentes personalizadas al cliente utilizando el método `writeSource` en el `DataStreamWriter`:

```tsx filename="route.ts" highlight="9-15"
import { openai } from '@ai-sdk/openai';
import { createDataStreamResponse, streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  return createDataStreamResponse({
    execute: dataStream => {
      // escribir una fuente de URL personalizada en el flujo:
      dataStream.writeSource({
        sourceType: 'url',
        id: 'source-1',
        url: 'https://example.com',
        title: 'Fuente de ejemplo',
      });

      const result = streamText({
        model: openai('gpt-4o'),
        messages,
      });

      result.mergeIntoDataStream(dataStream);
    },
  });
}
```

## Procesar datos personalizados en `useChat`

El hook `useChat` procesa automáticamente los datos de flujo y los hace disponibles para ti.

### Acceder a los datos

En el cliente, puedes desestructurar `data` del hook `useChat`, que almacena todos los `StreamData` como un `JSONValue[]`.

```tsx filename="page.tsx"
import { useChat } from '@ai-sdk/react';

const { data } = useChat();
```

### Accediendo a Anotaciones de Mensajes

Cada mensaje del hook `useChat` tiene una propiedad opcional `annotations` que contiene las anotaciones de mensajes enviadas desde el servidor.

Dado que la forma de las anotaciones depende de lo que se envía desde el servidor,
tienes que desestructurarlas de manera segura en el lado del cliente.

Aquí solo mostramos las anotaciones como una cadena de JSON:

```tsx filename="page.tsx" highlight="9"
import { Message, useChat } from '@ai-sdk/react';

const { messages } = useChat();

const result = (
  <>
    {messages?.map((m: Message) => (
      <div key={m.id}>
        {m.annotations && <>{JSON.stringify(m.annotations)}</>}
      </div>
    ))}
  </>
);
```

### Actualizando y Limpiando Datos

Puedes actualizar y limpiar el objeto `data` del hook `useChat` utilizando la función `setData`.

```tsx filename="page.tsx"
const { setData } = useChat();

// limpia los datos existentes
setData(undefined);

// establece nuevos datos
setData([{ test: 'value' }]);

// transforma los datos existentes, por ejemplo, agregando valores adicionales:
setData(currentData => [...currentData, { test: 'value' }]);
```

#### Ejemplo: Borrar al enviar

```tsx filename="page.tsx" highlight="18-21"
'use client';

import { Message, useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, data, setData } =
    useChat();

  return (
    <>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}

      {messages?.map((m: Message) => (
        <div key={m.id}>{`${m.role}: ${m.content}`}</div>
      ))}

      <form
        onSubmit={e => {
          setData(undefined); // borrar datos de flujo
          handleSubmit(e);
        }}
      >
        <input value={input} onChange={handleInputChange} />
      </form>
    </>
  );
}
```

---
titulo: Manejo de errores
descripcion: Aprende a manejar errores en la interfaz de usuario de la SDK de IA
---

# Manejo de errores

### Objeto de ayuda de errores

Cada hook de la interfaz de usuario de la SDK de IA también devuelve un [error](/docs/reference/ai-sdk-ui/use-chat)

#error) objeto que puedes utilizar para renderizar el error en tu interfaz de usuario.
Puedes utilizar el objeto de error para mostrar un mensaje de error, deshabilitar el botón de envío o mostrar un botón de reintento.

<Nota>
  Recomendamos mostrar un mensaje de error genérico al usuario, como "Algo salió mal." Esta es una buena práctica para evitar filtrar información desde el servidor.
</Nota>

```tsx archivo="app/page.tsx" resaltar="7,17-24,30"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, error, reload } =
    useChat({});

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}
        </div>
      ))}

      {error && (
        <>
          <div>Se produjo un error.</div>
          <button type="button" onClick={() => reload()}>
            Reintentar
          </button>
        </>
      )}

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          disabled={error != null}
        />
      </form>
    </div>
  );
}
```

#### Alternativa: reemplazar el último mensaje

Alternativamente, puedes escribir un manejador de formulario personalizado que reemplace el último mensaje cuando haya un error presente.

```tsx file="app/page.tsx" highlight="15-21,33"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const {
    handleInputChange,
    handleSubmit,
    error,
    input,
    messages,
    setMessages,
  } = useChat({});

  function customSubmit(event: React.FormEvent<HTMLFormElement>) {
    if (error != null) {
      setMessages(messages.slice(0, -1)); // eliminar último mensaje
    }

    handleSubmit(event);
  }

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}
        </div>
      ))}

      {error && <div>Ocurrió un error.</div>}

      <form onSubmit={customSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

### Callback de Manejo de Errores

Los errores se pueden procesar pasando un [`onError`](/docs/reference/ai-sdk-ui/use-chat)

# (on-error) función de llamada de retorno como opción a los hooks [`useChat`](/docs/reference/ai-sdk-ui/use-chat), [`useCompletion`](/docs/reference/ai-sdk-ui/use-completion) o [`useAssistant`](/docs/reference/ai-sdk-ui/use-assistant).
La función de llamada de retorno recibe un objeto de error como argumento.

```tsx file="app/page.tsx" highlight="8-11"
import { useChat } from '@ai-sdk/react';

export default function Page() {
  const {
    /* ... */
  } = useChat({
    // manejar errores:
    onError: error => {
      console.error(error);
    },
  });
}
```

### Inyectar Errores para Pruebas

Quizás desee crear errores para pruebas.
Puede hacerlo fácilmente lanzando un error en su manejador de ruta:

```ts file="app/api/chat/route.ts"
export async function POST(req: Request) {
  throw new Error('Este es un error de prueba');
}
```

---
titulo: Streaming suave de texto japonés
descripcion: Aprenda a streamear texto japonés de manera suave
---

# Streaming suave de texto japonés

Puede streamear texto japonés de manera suave utilizando la función `smoothStream` y la siguiente expresión regular que divide el texto en palabras y caracteres japoneses:

```tsx filename="page.tsx"
import { smoothStream } from 'ai';
import { useChat } from '@ai-sdk/react';

const { data } = useChat({
  experimental_transform: smoothStream({
    chunking: /[\u3040-\u309F\u30A0-\u30FF]|\S+\s+/,
  }),
});
```

---
titulo: Streaming suave de texto chino
descripcion: Aprenda a streamear texto chino de manera suave
---

# Streaming texto chino suave

Puedes streaming chino suave de texto utilizando la función `smoothStream` y el siguiente regex que divide tanto en palabras como en caracteres chinos:

```tsx filename="page.tsx"
import { smoothStream } from 'ai';
import { useChat } from '@ai-sdk/react';

const { data } = useChat({
  experimental_transform: smoothStream({
    chunking: /[\u4E00-\u9FFF]|\S+\s+/,
  }),
});
```

---
title: AI_APICallError
description: Aprende a solucionar AI_APICallError
---

# AI_APICallError

Este error ocurre cuando una llamada a la API falla.

## Propiedades

- `url`: La URL de la solicitud de API que falló
- `requestBodyValues`: Los valores del cuerpo de la solicitud enviados a la API
- `statusCode`: El código de estado HTTP devuelto por la API
- `responseHeaders`: Las cabeceras de respuesta devueltas por la API
- `responseBody`: El cuerpo de respuesta devuelto por la API
- `isRetryable`: Si la solicitud se puede volver a intentar según el código de estado
- `data`: Cualquier dato adicional asociado con el error

## Verificando este error

Puedes verificar si un error es una instancia de `AI_APICallError` utilizando:

```typescript
import { APICallError } from 'ai';

if (APICallError.isInstance(error)) {
  // Maneja el error
}
```

---
title: AI_DownloadError
description: Aprende a solucionar AI_DownloadError
---

# AI_DownloadError

Este error ocurre cuando una descarga falla.

## Propiedades

- `url`: La URL que falló al descargar
- `statusCode`: El código de estado HTTP devuelto por el servidor
- `statusText`: El texto de estado HTTP devuelto por el servidor
- `message`: El mensaje de error que contiene detalles sobre la falla de la descarga

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_DownloadError` utilizando:

```typescript
import { DownloadError } from 'ai';

if (DownloadError.isInstance(error)) {
  // Maneja el error
}
```

---
title: AI_EmptyResponseBodyError
description: Aprende a solucionar AI_EmptyResponseBodyError
---

# AI_EmptyResponseBodyError

Este error se produce cuando el servidor devuelve un cuerpo de respuesta vacío.

## Propiedades

- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_EmptyResponseBodyError` utilizando:

```typescript
import { EmptyResponseBodyError } from 'ai';

if (EmptyResponseBodyError.isInstance(error)) {
  // Maneja el error
}
```

---
title: AI_InvalidArgumentError
description: Aprende a solucionar AI_InvalidArgumentError
---

# AI_InvalidArgumentError

Este error se produce cuando se proporcionó un argumento inválido.

## Propiedades

- `parameter`: El nombre del parámetro que es inválido
- `value`: El valor inválido
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidArgumentError` utilizando:

```typescript
import { InvalidArgumentError } from 'ai';

if (InvalidArgumentError.isInstance(error)) {
  // Maneja el error
}
```

---
title: AI_InvalidDataContentError
description: Cómo solucionar AI_InvalidDataContentError
---

# AI_InvalidDataContentError

Este error se produce cuando el contenido de datos proporcionado en una parte de mensaje multimodal es inválido. Consulta los [ ejemplos de promp para mensajes multimodales ](/docs/foundations/prompts#message-prompts).

## Propiedades

- `content`: El valor de contenido inválido
- `message`: El mensaje de error que describe los tipos de contenido esperados y recibidos

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidDataContentError` utilizando:

```typescript
import { InvalidDataContentError } from 'ai';

if (InvalidDataContentError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_InvalidDataContent
descripcion: Aprende a solucionar AI_InvalidDataContent
---

# AI_InvalidDataContent

Este error ocurre cuando se proporciona contenido de datos inválido.

## Propiedades

- `content`: El valor de contenido inválido
- `message`: El mensaje de error
- `cause`: La causa del error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidDataContent` utilizando:

```typescript
import { InvalidDataContent } from 'ai';

if (InvalidDataContent.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_InvalidMessageRoleError
descripcion: Aprende a solucionar AI_InvalidMessageRoleError
---

# AI_InvalidMessageRoleError

Este error ocurre cuando se proporciona un rol de mensaje inválido.

## Propiedades

- `role`: El valor de rol inválido
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidMessageRoleError` utilizando:

```typescript
import { InvalidMessageRoleError } from 'ai';

if (InvalidMessageRoleError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_InvalidPromptError
descripcion: Aprende a solucionar AI_InvalidPromptError
---

# AI_InvalidPromptError

Este error ocurre cuando el prompt proporcionado es inválido.

## Propiedades

- `prompt`: El valor de prompt inválido
- `message`: El mensaje de error
- `cause`: La causa del error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidPromptError` usando:

```typescript
import { InvalidPromptError } from 'ai';

if (InvalidPromptError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_InvalidResponseDataError
descripcion: Aprende a solucionar AI_InvalidResponseDataError
---

# AI_InvalidResponseDataError

Este error se produce cuando el servidor devuelve una respuesta con un contenido de datos inválido.

## Propiedades

- `data`: El valor de datos de respuesta inválido
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidResponseDataError` usando:

```typescript
import { InvalidResponseDataError } from 'ai';

if (InvalidResponseDataError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_InvalidToolArgumentsError
descripcion: Aprende a solucionar AI_InvalidToolArgumentsError
---

# AI_InvalidToolArgumentsError

Este error se produce cuando se proporcionó un argumento de herramienta inválido.

## Propiedades

- `toolName`: El nombre de la herramienta con argumentos inválidos
- `toolArgs`: Los argumentos de herramienta inválidos
- `message`: El mensaje de error
- `cause`: La causa del error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_InvalidToolArgumentsError` usando:

```typescript
import { InvalidToolArgumentsError } from 'ai';

if (InvalidToolArgumentsError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_JSONParseError
descripcion: Aprende a solucionar AI_JSONParseError
---

# AI_JSONParseError

Este error se produce cuando JSON falla al parsear.

## Propiedades

- `text`: El valor de texto que no pudo ser parseado
- `message`: El mensaje de error que incluye detalles del error de parseo

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_JSONParseError` utilizando:

```typescript
import { JSONParseError } from 'ai';

if (JSONParseError.isInstance(error)) {
  // Maneja el error
}
```

---
titulo: AI_LoadAPIKeyError
descripcion: Aprende a solucionar AI_LoadAPIKeyError
---

# AI_LoadAPIKeyError

Este error ocurre cuando la API key no se carga con éxito.

## Propiedades

- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_LoadAPIKeyError` utilizando:

```typescript
import { LoadAPIKeyError } from 'ai';

if (LoadAPIKeyError.isInstance(error)) {
  // Maneja el error
}
```

---
titulo: AI_LoadSettingError
descripcion: Aprende a solucionar AI_LoadSettingError
---

# AI_LoadSettingError

Este error ocurre cuando una configuración no se carga con éxito.

## Propiedades

- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_LoadSettingError` utilizando:

```typescript
import { LoadSettingError } from 'ai';

if (LoadSettingError.isInstance(error)) {
  // Maneja el error
}
```

---
titulo: AI_MessageConversionError
descripcion: Aprende a solucionar AI_MessageConversionError
---

# AI_MessageConversionError

Este error ocurre cuando la conversión de mensaje falla.

## Propiedades

- `originalMessage`: El mensaje original que falló la conversión
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_MessageConversionError` utilizando:

```typescript
import { MessageConversionError } from 'ai';

if (MessageConversionError.isInstance(error)) {
  // Maneja el error
}
```

---
titulo: AI_NoAudioGeneratedError
descripcion: Aprende a solucionar AI_NoAudioGeneratedError
---

# Error de AI_NoAudioGeneratedError

Este error se produce cuando no se pudo generar audio a partir de la entrada.

## Propiedades

- `responses`: Array de respuestas
- `message`: El mensaje de error

## Verificar este Error

Puedes verificar si un error es una instancia de `AI_NoAudioGeneratedError` utilizando:

```typescript
import { NoAudioGeneratedError } from 'ai';

if (NoAudioGeneratedError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: Error de AI_NoContentGeneratedError
descripcion: Aprende a solucionar el error de AI_NoContentGeneratedError
---

# Error de AI_NoContentGeneratedError

Este error se produce cuando el proveedor de inteligencia artificial falla en generar contenido.

## Propiedades

- `message`: El mensaje de error

## Verificar este Error

Puedes verificar si un error es una instancia de `AI_NoContentGeneratedError` utilizando:

```typescript
import { NoContentGeneratedError } from 'ai';

if (NoContentGeneratedError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: Error de AI_NoImageGeneratedError
descripcion: Aprende a solucionar el error de AI_NoImageGeneratedError
---

# Error de AI_NoImageGeneratedError

Este error se produce cuando el proveedor de inteligencia artificial falla en generar una imagen.
Puede surgir debido a las siguientes razones:

- El modelo falló en generar una respuesta.
- El modelo generó una respuesta inválida.

## Propiedades

- `message`: El mensaje de error.
- `responses`: Metadatos sobre las respuestas del modelo de imagen, incluyendo fecha y hora, modelo y encabezados.
- `cause`: La causa del error. Puedes utilizar esto para manejar errores de manera más detallada.

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoImageGeneratedError` utilizando:

```typescript
import { generateImage, NoImageGeneratedError } from 'ai';

try {
  await generateImage({ model, prompt });
} catch (error) {
  if (NoImageGeneratedError.isInstance(error)) {
    console.log('NoImageGeneratedError');
    console.log('Causa:', error.cause);
    console.log('Respuestas:', error.responses);
  }
}
```

---
title: AI_NoObjectGeneratedError
description: Aprende a solucionar AI_NoObjectGeneratedError
---

# AI_NoObjectGeneratedError

Este error ocurre cuando el proveedor de inteligencia artificial falla en generar un objeto parseable que cumpla con el esquema.
Puede surgir debido a las siguientes razones:

- El modelo falló en generar una respuesta.
- El modelo generó una respuesta que no pudo ser parseada.
- El modelo generó una respuesta que no pudo ser validada contra el esquema.

## Propiedades

- `message`: El mensaje de error.
- `text`: El texto que fue generado por el modelo. Este puede ser el texto bruto o el texto de llamada de herramienta, dependiendo del modo de generación de objetos.
- `response`: Metadatos sobre la respuesta del modelo de lenguaje, incluyendo id de respuesta, timestamp y modelo.
- `usage`: Uso del token de solicitud.
- `finishReason`: Razón de finalización de la solicitud. Por ejemplo 'length' si el modelo generó el número máximo de tokens, lo que podría resultar en un error de parsing de JSON.
- `cause`: La causa del error (por ejemplo, un error de parsing de JSON). Puedes utilizar esto para un manejo de errores más detallado.

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoObjectGeneratedError` utilizando:

```typescript
import { generateObject, NoObjectGeneratedError } from 'ai';

try {
  await generateObject({ model, schema, prompt });
} catch (error) {
  if (NoObjectGeneratedError.isInstance(error)) {
    console.log('NoObjectGeneratedError');
    console.log('Causa:', error.cause);
    console.log('Texto:', error.text);
    console.log('Respuesta:', error.response);
    console.log('Uso:', error.usage);
    console.log('Razón de finalización:', error.finishReason);
  }
}
```

---
titulo: AI_NoOutputSpecifiedError
descripcion: Aprende a solucionar AI_NoOutputSpecifiedError
---

# AI_NoOutputSpecifiedError

Este error se produce cuando no se especificó un formato de salida para la respuesta del IA, y se llaman métodos relacionados con la salida.

## Propiedades

- `mensaje`: El mensaje de error (por defecto, 'No se especificó un formato de salida.')

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoOutputSpecifiedError` utilizando:

```typescript
import { NoOutputSpecifiedError } from 'ai';

if (NoOutputSpecifiedError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_NoSuchModelError
descripcion: Aprende a solucionar AI_NoSuchModelError
---

# AI_NoSuchModelError

Este error se produce cuando no se encuentra un ID de modelo.

## Propiedades

- `modelId`: El ID del modelo que no se encontró
- `modelType`: El tipo de modelo
- `mensaje`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoSuchModelError` usando:

```typescript
import { NoSuchModelError } from 'ai';

if (NoSuchModelError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_NoSuchProviderError
descripcion: Aprende a solucionar AI_NoSuchProviderError
---

# AI_NoSuchProviderError

Este error ocurre cuando no se encuentra un ID de proveedor.

## Propiedades

- `providerId`: El ID del proveedor que no se encontró
- `availableProviders`: Array de IDs de proveedores disponibles
- `modelId`: El ID del modelo
- `modelType`: El tipo de modelo
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoSuchProviderError` usando:

```typescript
import { NoSuchProviderError } from 'ai';

if (NoSuchProviderError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_NoSuchToolError
descripcion: Aprende a solucionar AI_NoSuchToolError
---

# AI_NoSuchToolError

Este error ocurre cuando un modelo intenta llamar a una herramienta no disponible.

## Propiedades

- `toolName`: El nombre de la herramienta que no se encontró
- `availableTools`: Array de nombres de herramientas disponibles
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoSuchToolError` usando:

```typescript
import { NoSuchToolError } from 'ai';

if (NoSuchToolError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_NoTranscriptGeneratedError
descripcion: Aprende a solucionar AI_NoTranscriptGeneratedError
---

# AI_NoTranscriptGeneratedError

Este error ocurre cuando no se puede generar un transcripto a partir de la entrada.

## Propiedades

- `responses`: Array de respuestas
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_NoTranscriptGeneratedError` utilizando:

```typescript
import { NoTranscriptGeneratedError } from 'ai';

if (NoTranscriptGeneratedError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_RetryError
descripcion: Aprende a solucionar AI_RetryError
---

# AI_RetryError

Este error ocurre cuando una operación de retry falla.

## Propiedades

- `reason`: La razón del fracaso de la operación de retry
- `lastError`: El error más reciente que ocurrió durante las operaciones de retry
- `errors`: Array de todos los errores que ocurrieron durante las operaciones de retry
- `message`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_RetryError` utilizando:

```typescript
import { RetryError } from 'ai';

if (RetryError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: AI_TooManyEmbeddingValuesForCallError
descripcion: Aprende a solucionar AI_TooManyEmbeddingValuesForCallError
---

# AI_TooManyEmbeddingValuesForCallError

Este error ocurre cuando se proporcionan demasiados valores en una sola llamada de embedding.

## Propiedades

- `provider`: El nombre del proveedor de AI
- `modelId`: El ID del modelo de embedding
- `maxEmbeddingsPerCall`: El número máximo de embeddings permitidos por llamada
- `values`: El array de valores que se proporcionó

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_TooManyEmbeddingValuesForCallError` utilizando:

```typescript
import { TooManyEmbeddingValuesForCallError } from 'ai';

if (TooManyEmbeddingValuesForCallError.isInstance(error)) {
  // Manejar el error
}
```

---
titulo: ToolCallRepairError
descripcion: Aprende a solucionar AI SDK ToolCallRepairError
---

# Error de Reparación de Llamada a Herramienta

Este error se produce cuando hay una falla al intentar reparar una llamada a herramienta inválida.
Esto sucede típicamente cuando el AI intenta corregir tanto
un `Error de Herramienta No Encontrada` como un `Error de Argumentos de Herramienta Inválidos`.

## Propiedades

- `originalError`: El error original que desencadenó el intento de reparación (ya sea `Error de Herramienta No Encontrada` o `Error de Argumentos de Herramienta Inválidos`)
- `message`: El mensaje de error
- `cause`: El error subyacente que causó que la reparación fallara

## Verificación de este Error

Puedes verificar si un error es una instancia de `Error de Reparación de Llamada a Herramienta` usando:

```typescript
import { ToolCallRepairError } from 'ai';

if (ToolCallRepairError.isInstance(error)) {
  // Maneja el error
}
```

---
title: Error de Ejecución de Herramienta AI
description: Aprende a solucionar el Error de Ejecución de Herramienta AI
---

 # Error de Ejecución de Herramienta AI

Este error se produce cuando hay una falla durante la ejecución de una herramienta.

## Propiedades

- `toolName`: El nombre de la herramienta que falló
- `toolArgs`: Los argumentos pasados a la herramienta
- `toolCallId`: El ID de la llamada a la herramienta que falló
- `message`: El mensaje de error
- `cause`: El error subyacente que causó que la ejecución de la herramienta fallara

## Verificación de este Error

Puedes verificar si un error es una instancia de `Error de Ejecución de Herramienta AI` usando:

```typescript
import { ToolExecutionError } from 'ai';

if (ToolExecutionError.isInstance(error)) {
  // Maneja el error
}
```

---
title: Error de Validación de Tipo AI
description: Aprende a solucionar el Error de Validación de Tipo AI
---

 # Error de Validación de Tipo AI

Este error se produce cuando la validación de tipo falla.

## Propiedades

- `value`: El valor que falló la validación
- `message`: El mensaje de error que incluye detalles de validación

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_TypeValidationError` utilizando:

```typescript
import { TypeValidationError } from 'ai';

if (TypeValidationError.isInstance(error)) {
  // Manejar el error
}
```

---
 título: AI_UnsupportedFunctionalityError
 descripción: Aprende a solucionar AI_UnsupportedFunctionalityError
---

 # AI_UnsupportedFunctionalityError

Este error se produce cuando la funcionalidad no es soportada.

## Propiedades

- `funcionalidad`: El nombre de la funcionalidad no soportada
- `mensaje`: El mensaje de error

## Verificando este Error

Puedes verificar si un error es una instancia de `AI_UnsupportedFunctionalityError` utilizando:

```typescript
import { UnsupportedFunctionalityError } from 'ai';

if (UnsupportedFunctionalityError.isInstance(error)) {
  // Manejar el error
}
```

---
 título: xAI Grok
 descripción: Aprende a utilizar xAI Grok.
---

 # Proveedor xAI Grok

El [proveedor xAI Grok](https://x.ai) contiene soporte para modelos de lenguaje para la [API xAI](https://x.ai/api).

## Configuración

El proveedor xAI Grok está disponible a través del módulo `@ai-sdk/xai`. Puedes
instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/xai" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/xai" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/xai" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `xai` desde `@ai-sdk/xai`:

```ts
import { xai } from '@ai-sdk/xai';
```

Si necesitas una configuración personalizada, puedes importar `createXai` desde `@ai-sdk/xai`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createXai } from '@ai-sdk/xai';

const xai = createXai({
  apiKey: 'tu-clave-de-api',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor xAI:

- **baseURL** _cadena_

  Utiliza una URL diferente para prefixiar las llamadas a API, por ejemplo, para utilizar servidores proxy.
  La URL predeterminada es `https://api.x.ai/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`. Por defecto, se utiliza la variable de entorno `XAI_API_KEY`.

- **headers** _Registro&lt;cadena,cadena&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(_entrada: Información de solicitud, init?: Inicialización de solicitud) => Promesa&lt;Respuesta&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). Por defecto, se utiliza la función global `fetch`. Puedes utilizarla como middleware para interceptar solicitudes, o proporcionar una implementación de fetch personalizada para pruebas, por ejemplo.

## Modelos de Lenguaje

Puedes crear modelos [xAI](https://console.x.ai) utilizando una instancia de proveedor. El primer argumento es el identificador del modelo, por ejemplo, `grok-beta`.

```ts
const model = xai('grok-3');
```

### Ejemplo

Puedes utilizar modelos de lenguaje xAI para generar texto con la función `generateText`:

```ts
import { xai } from '@ai-sdk/xai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: xai('grok-3'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje xAI también se pueden utilizar en las funciones `streamText`, `generateObject`, y `streamObject` (consulte [AI SDK Core](/docs/ai-sdk-core)).

### Modelos de Chat

Los modelos de chat xAI también admiten algunas configuraciones específicas del modelo que no forman parte de
las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings). Puedes pasarlas como
argumento de opciones:

```ts
const model = xai('grok-3', {
  user: 'test-user', // identificador de usuario único (opcional)
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de chat xAI:

- **user** _cadena_

  Un identificador único que representa a su usuario final, lo que puede ayudar a xAI a
  monitorear y detectar abuso.

Los modelos de chat xAI también admiten algunas opciones de proveedor específicas del modelo. Puedes pasarlas en el argumento `providerOptions`:

```ts
const model = xai('grok-3');

await generateText({
  model,
  providerOptions: {
    xai: {
      reasoningEffort: 'alto',
    },
  },
});
```

Las siguientes opciones de proveedor opcionales están disponibles para los modelos de chat xAI:

- **reasoningEffort** _'bajo' | 'medio' | 'alto'_

  Esfuerzo de razonamiento para modelos de razonamiento. Por defecto, es `medio`. Si utilizas `providerOptions` para establecer la opción `reasoningEffort`, esta configuración del modelo se ignorará.

## Capabilidades del Modelo

| Modelo                | Entrada de Imagen         | Generación de Objetos   | Uso de Herramientas          | Streaming de Herramientas      |
| -------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `grok-3`             | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-3-fast`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-3-mini`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-3-mini-fast`   | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-2-1212`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-2-vision-1212` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-beta`          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-vision-beta`   | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. Consulte la documentación de [xAI](https://docs.x.ai/docs)

# Modelos) para obtener una lista completa de modelos disponibles. La tabla anterior muestra modelos populares. También puedes pasar cualquier ID de modelo de proveedor disponible como cadena si es necesario.

## Modelos de Imágenes

Puedes crear modelos de imágenes de xAI utilizando el método de fábrica `.imageModel()`. Para obtener más información sobre la generación de imágenes con el SDK de AI, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { xai } from '@ai-sdk/xai';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: xai.image('grok-2-image'),
  prompt: 'Una ciudad futurista al atardecer',
});
```

<Nota>
  El modelo de imagen de xAI no admite actualmente los parámetros `aspectRatio` o `size`.
  El tamaño de la imagen predeterminado es 1024x768.
</Nota>

### Opciones específicas del modelo

Puedes personalizar el comportamiento de generación de imágenes con ajustes específicos del modelo:

```ts
import { xai } from '@ai-sdk/xai';
import { experimental_generateImage as generateImage } from 'ai';

const { images } = await generateImage({
  model: xai.image('grok-2-image', {
    maxImagesPerCall: 5, // Valor predeterminado es 10
  }),
  prompt: 'Una ciudad futurista al atardecer',
  n: 2, // Genera 2 imágenes
});
```

### Capabilidades del Modelo

| Modelo          | Tamaños              | Notas                                                                                                                                                                                                    |
| -------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grok-2-image` | 1024x768 (por defecto) | El modelo de generación de imágenes de texto a imagen de xAI, diseñado para crear imágenes de alta calidad a partir de promt de texto. Está entrenado en un conjunto de datos diverso y puede generar imágenes en varios estilos, temas y configuraciones. |

---
title: Vercel
description: Aprende a utilizar los modelos v0 de Vercel con la SDK de IA.
---

# Proveedor de Vercel

El [proveedor de Vercel](https://vercel.com) te da acceso a la [API v0](https://vercel.com/docs/v0/api), diseñada para construir aplicaciones web modernas. El modelo `v0-1.0-md` admite inputs de texto e imágenes y proporciona respuestas de streaming rápidas.

Puedes crear tu clave de API de Vercel en [v0.dev](https://v0.dev/chat/settings/keys).

<Nota>
  La API v0 actualmente se encuentra en beta y requiere un plan Premium o de equipo con facturación basada en el uso habilitada. Para obtener más detalles, visita la [página de precios](https://v0.dev/pricing). Para solicitar un límite más alto, contacta con Vercel en support@v0.dev.
</Nota>

## Características

- **Completaciones conscientes de marco**: Evaluadas en pilas modernas como Next.js y Vercel
- **Auto-reparación**: Identifica y corrige problemas de codificación comunes durante la generación
- **Edición rápida**: Transmite ediciones en línea mientras están disponibles
- **Compatibilidad con OpenAI**: Puede usarse con cualquier herramienta o SDK que admita el formato de API de OpenAI
- **Multimodal**: Admite tanto inputs de texto como de imágenes

## Configuración

El proveedor de Vercel está disponible a través del módulo `@ai-sdk/vercel`. Puedes instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/vercel" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/vercel" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/vercel" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `vercel` desde `@ai-sdk/vercel`:

```ts
import { vercel } from '@ai-sdk/vercel';
```

Si necesitas una configuración personalizada, puedes importar `createVercel` desde `@ai-sdk/vercel` y crear una instancia de proveedor con tus ajustes:

```ts
import { createVercel } from '@ai-sdk/vercel';

const vercel = createVercel({
  apiKey: process.env.VERCEL_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Vercel:

- **baseURL** _cadena_

  Utiliza una dirección URL diferente para prefixiar las llamadas a la API. El prefijo predeterminado es `https://api.v0.dev/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`. Por defecto, es la variable de entorno `VERCEL_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(entrada: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). Por defecto, es la función global `fetch`. Puedes utilizarla como middleware para interceptar solicitudes, o para proporcionar una implementación de fetch personalizada para pruebas, por ejemplo.

## Modelos de Lenguaje

Puedes crear modelos de lenguaje utilizando una instancia de proveedor. El primer argumento es el ID del modelo, por ejemplo:

```ts
import { vercel } from '@ai-sdk/vercel';
import { generateText } from 'ai';

const { text } = await generateText({
  model: vercel('v0-1.0-md'),
  prompt: 'Crear un chatbot de AI de Next.js',
});
```

Los modelos de lenguaje de Vercel también se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

## Ejemplo con AI SDK

```ts
import { generateText } from 'ai';
import { createVercel } from '@ai-sdk/vercel';

const vercel = createVercel({
  baseURL: 'https://api.v0.dev/v1',
  apiKey: process.env.VERCEL_API_KEY,
});

const { text } = await generateText({
  model: vercel('v0-1.0-md'),
  prompt: 'Crear un chatbot de Next.js de AI con autenticación',
});
```

## Modelos

### v0-1.0-md

El modelo `v0-1.0-md` es el modelo predeterminado servido por la API v0.

Capacidades:

- Soporta entradas de texto e imagen (multimodal)
- Soporta llamadas a funciones y herramientas
- Respuestas en streaming con baja latencia
- Optimizado para el desarrollo web frontend y full-stack

## Capacidad de Modelos

| Modelo       | Entrada de Imagen         | Generación de Objetos   | Uso de Herramientas          | Streaming de Herramientas      |
| ----------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `v0-1.0-md` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
title: OpenAI
description: Aprende a utilizar el proveedor OpenAI para el SDK de AI.
---

# Proveedor de OpenAI

El [proveedor de OpenAI](https://openai.com/) contiene soporte para modelos de lenguaje para las API de respuestas, chat y completación de OpenAI, así como soporte para modelos de embebedad para la API de embebedad de OpenAI.

## Configuración

El proveedor de OpenAI está disponible en el módulo `@ai-sdk/openai`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/openai" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/openai" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/openai" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor por defecto `openai` de `@ai-sdk/openai`:

```ts
import { openai } from '@ai-sdk/openai';
```

Si necesitas una configuración personalizada, puedes importar `createOpenAI` de `@ai-sdk/openai` y crear una instancia de proveedor con tus ajustes:

```ts
import { createOpenAI } from '@ai-sdk/openai';

const openai = createOpenAI({
  // ajustes personalizados, p. ej.
  compatibility: 'strict', // modo estricto, habilita cuando se utiliza la API de OpenAI
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor de OpenAI:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para las llamadas a la API, p. ej. para utilizar servidores de proxy.
  El prefijo predeterminado es `https://api.openai.com/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, se utiliza la variable de entorno `OPENAI_API_KEY`.

- **name** _cadena_

  El nombre del proveedor. Puedes establecer esto cuando se utilicen proveedores compatibles con OpenAI
  para cambiar la propiedad del modelo de proveedor. Por defecto, es `openai`.

- **organization** _cadena_

  Organización de OpenAI.

- **project** _cadena_

  Proyecto de OpenAI.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, se utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

- **compatibility** _"strict" | "compatible"_

Modo de compatibilidad de OpenAI. Debe configurarse en `strict` cuando se utiliza la API de OpenAI,
  y `compatible` cuando se utilizan proveedores de terceros. En modo `compatible`, la información más reciente
  como `streamOptions` no se envía, lo que resulta en un uso de tokens `NaN`. Por defecto, se configura en 'compatible'.

## Modelos de Lenguaje

La instancia del proveedor de OpenAI es una función que puedes invocar para crear un modelo de lenguaje:

```ts
const modelo = openai('gpt-4-turbo');
```

Automáticamente selecciona la API correcta según la ID del modelo.
También puedes pasar configuraciones adicionales en la segunda argumento:

```ts
const modelo = openai('gpt-4-turbo', {
  // configuraciones adicionales
});
```

Las opciones disponibles dependen de la API que se elige automáticamente para el modelo (consulte a continuación).
Si deseas seleccionar explícitamente una API específica para un modelo, puedes usar `.chat` o `.completion`.

### Ejemplo

Puedes usar modelos de lenguaje de OpenAI para generar texto con la función `generateText`:

```ts
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { texto } = await generateText({
  modelo: openai('gpt-4-turbo'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de OpenAI también se pueden usar en las funciones `streamText`, `generateObject`, y `streamObject` (consulte [AI SDK Core](/docs/ai-sdk-core)).

### Modelos de Chat

Puedes crear modelos que llamen a la [API de chat de OpenAI](https://platform.openai.com/docs/api-reference/chat) utilizando el método de fábrica `.chat()`.
El primer argumento es el identificador del modelo, por ejemplo `gpt-4`.
Los modelos de chat de OpenAI admiten llamadas a herramientas y algunos tienen capacidades multi-modales.

```ts
const modelo = openai.chat('gpt-3.5-turbo');
```

Los modelos de chat de OpenAI admiten también algunas configuraciones específicas del modelo que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const modelo = openai.chat('gpt-3.5-turbo', {
  logitBias: {
    // valor de probabilidad opcional para tokens específicos
    '50256': -100,
  },
  usuario: 'test-user', // identificador de usuario único opcional
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de chat de OpenAI:

- **logitBias** _Registro&lt;number, number&gt;_

  Modifica la probabilidad de que los tokens específicos aparezcan en la completación.

  Acepta un objeto JSON que mapea tokens (especificados por su ID de token en el tokenizador GPT) a un valor de sesgo asociado entre -100 y 100. Puedes utilizar esta herramienta de tokenizador para convertir texto a IDs de token. Matemáticamente, el sesgo se suma a los logits generados por el modelo antes de la muestra. El efecto exacto variará por modelo, pero valores entre -1 y 1 deberían disminuir o aumentar la probabilidad de selección; valores como -100 o 100 deberían resultar en una prohibición o selección exclusiva del token relevante.

  Por ejemplo, puedes pasar `{"50256": -100}` para evitar que el token se genere.

- **logprobs** _boolean | number_

  Devuelve las probabilidades logarítmicas de los tokens. Incluir logprobs aumentará el tamaño de la respuesta y puede ralentizar los tiempos de respuesta. Sin embargo, puede ser útil para comprender mejor cómo se comporta el modelo.

  Establecer a true devolverá las probabilidades logarítmicas de los tokens que se generaron.

Establecer a un número devolverá las probabilidades logarítmicas de los n tokens más generados.

- **parallelToolCalls** _boolean_

  Si habilitar llamadas de función paralelas durante el uso de herramientas. Por defecto, `true`.

- **useLegacyFunctionCalls** _boolean_

  Si utilizar llamadas de función legadas. Por defecto, `false`.

  Requerido por algunos motores de inferencia de código abierto que no admiten la API `tools`. También puede proporcionar un trabajo alrededor de `parallelToolCalls` resultando en el proveedor almacenando llamadas de herramienta, lo que causa `streamObject` no ser de transmisión.

  Preferir establecer `parallelToolCalls: false` sobre esta opción.

- **structuredOutputs** _boolean_

  Si utilizar [salidas estructuradas](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-structured-output)

# Salidas Estructuradas).
  Por defecto, `false` para modelos normales, y `true` para modelos de razonamiento.

  Cuando está habilitado, las llamadas a herramientas y la generación de objetos serán estrictas y seguirán el esquema proporcionado.

- **usuario** _cadena_

  Un identificador único que representa a su usuario final, que puede ayudar a OpenAI a monitorear y detectar abuso. [Aprende más](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

- **descargarImagenes** _boolean_

  Descargar imágenes automáticamente y pasar la imagen como datos al modelo.
  OpenAI admite URLs de imágenes para modelos públicos, por lo que esto solo es necesario para modelos privados o cuando las imágenes no están accesibles públicamente.
  Por defecto, `false`.

- **simularStreaming** _boolean_

  Simula streaming utilizando una llamada de generación normal y devolviéndolo como un flujo.
  Activa esta opción si el modelo que estás utilizando no admite streaming.
  Por defecto, `false`.

- **esfuerzoDeRazonamiento** _'bajo' | 'medio' | 'alto'_

  Esfuerzo de razonamiento para modelos de razonamiento. Por defecto, `medio`. Si utiliza `providerOptions` para establecer la opción `esfuerzoDeRazonamiento`, esta configuración del modelo se ignorará.

#### Razonamiento

OpenAI ha introducido la serie de modelos de [razonamiento](https://platform.openai.com/docs/guides/reasoning) `o1`, `o3`, y `o4`. Actualmente están disponibles `o4-mini`, `o3`, `o3-mini`, `o1`, `o1-mini`, y `o1-preview`.

Los modelos de razonamiento solo generan texto, tienen varias limitaciones y solo se admiten utilizando `generateText` y `streamText`.

Además, admiten ajustes adicionales y metadatos de respuesta:

- Puedes utilizar `providerOptions` para establecer

  - la opción `reasoningEffort` (o alternativamente la configuración del modelo `reasoningEffort`), que determina la cantidad de razonamiento que realiza el modelo.

- Puedes utilizar los metadatos de respuesta `providerMetadata` para acceder al número de tokens de razonamiento que el modelo generó.

```ts highlight="4,7-11,17"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text, usage, providerMetadata } = await generateText({
  model: openai('o3-mini'),
  prompt: 'Inventa un nuevo feriado y describe sus tradiciones.',
  providerOptions: {
    openai: {
      reasoningEffort: 'bajo',
    },
  },
});

console.log(text);
console.log('Uso:', {
  ...usage,
  tokensDeRazonamiento: providerMetadata?.openai?.reasoningTokens,
});
```

<Nota>
  Los mensajes del sistema se convierten automáticamente en mensajes del desarrollador de OpenAI para
  los modelos de razonamiento cuando se admiten. Para los modelos que no admiten mensajes del desarrollador,
  como `o1-preview`, los mensajes del sistema se eliminan y se agrega una advertencia.
</Nota>

<Nota>
  Los modelos de razonamiento como `o1-mini` y `o1-preview` requieren inferencia de tiempo de ejecución adicional para completar su fase de razonamiento antes de generar una respuesta. Esto introduce una latencia más larga en comparación con otros modelos, con `o1-preview` exhibiendo significativamente más tiempo de inferencia que `o1-mini`.
</Nota>

<Nota>
  `maxTokens` se mapea automáticamente a `max_completion_tokens` para modelos de razonamiento.
</Nota>

#### Salidas Estructuradas

Puedes habilitar [salidas estructuradas de OpenAI](https://openai.com/index/introduciendo-salidas-estructuradas-en-la-api/) estableciendo la opción `structuredOutputs` en `true`.
Las salidas estructuradas son una forma de generación guiada por gramática.
Se utiliza el esquema JSON como gramática y las salidas siempre se ajustarán al esquema.

```ts highlight="7"
import { openai } from '@ai-sdk/openai';
import { generateObject } from 'ai';
import { z } from 'zod';

const result = await generateObject({
  model: openai('gpt-4o-2024-08-06', {
    structuredOutputs: true,
  }),
  schemaName: 'receta',
  schemaDescription: 'Una receta para lasaña.',
  schema: z.object({
    nombre: z.string(),
    ingredientes: z.array(
      z.object({
        nombre: z.string(),
        cantidad: z.string(),
      }),
    ),
    pasos: z.array(z.string()),
  }),
  prompt: 'Genera una receta de lasaña.',
});

console.log(JSON.stringify(result.object, null, 2));
```

<Nota tipo="advertencia">
  Las salidas estructuradas de OpenAI tienen varias
  [limitaciones](https://openai.com/index/introduciendo-salidas-estructuradas-en-la-api),
  en particular alrededor de los [esquemas soportados](https://platform.openai.com/docs/guides/structured-outputs/supported-schemas),
  y por lo tanto son de opt-in.

Por ejemplo, las propiedades de esquema opcionales no están soportadas.
Necesitas cambiar Zod `.nullish()` y `.optional()` a `.nullable()`.

</Nota>

#### Soporte de PDF

La API de Chat de OpenAI admite la lectura de archivos PDF.
Puedes pasar archivos PDF como parte del contenido del mensaje utilizando el tipo `file`:

```ts
const result = await generateText({
  model: openai('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Cuál es un modelo de inmersión?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
          filename: 'ai.pdf', // opcional
        },
      ],
    },
  ],
});
```

El modelo tendrá acceso a los contenidos del archivo PDF y responderá a preguntas sobre él.
El archivo PDF debe ser pasado utilizando el campo `data`, y el `mimeType` debe estar configurado en `'application/pdf'`.

#### Salidas Predichas

OpenAI admite [salidas predichas](https://platform.openai.com/docs/guides/latency-optimization)

# (use-predicted-outputs) para `gpt-4o` y `gpt-4o-mini`.
Los resultados predichos te ayudan a reducir la latencia permitiéndote especificar un texto base que el modelo deberá modificar.
Puedes habilitar los resultados predichos agregando la opción `prediction` al objeto `providerOptions.openai`:

```ts highlight="15-18"
const result = streamText({
  model: openai('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: 'Reemplaza la propiedad Username con una propiedad Email.',
    },
    {
      role: 'user',
      content: existingCode,
    },
  ],
  providerOptions: {
    openai: {
      prediction: {
        type: 'content',
        content: existingCode,
      },
    },
  },
});
```

OpenAI proporciona información de uso para los resultados predichos (`acceptedPredictionTokens` y `rejectedPredictionTokens`).
Puedes acceder a ella en el objeto `providerMetadata`.

```ts highlight="11"
const openaiMetadata = (await result.providerMetadata)?.openai;

const acceptedPredictionTokens = openaiMetadata?.acceptedPredictionTokens;
const rejectedPredictionTokens = openaiMetadata?.rejectedPredictionTokens;
```

<Nota tipo="advertencia">
  Los resultados predichos de OpenAI tienen varias
  [limitaciones](https://platform.openai.com/docs/guides/predicted-outputs#limitations),
  por ejemplo, parámetros de API no admitidos y sin soporte de llamadas de herramientas.
</Nota>

#### Detalle de imagen

Puedes utilizar la opción de proveedor `openai` para establecer el [detalle de entrada de imagen](https://platform.openai.com/docs/guides/images-vision?api-mode=respons

# Especificar el nivel de detalles del input de imagen a `alto`, `bajo` o `auto`:

```ts highlight="13-16"
const resultado = await generarTexto({
  modelo: openai('gpt-4o'),
  mensajes: [
    {
      rol: 'usuario',
      contenido: [
        { tipo: 'texto', texto: 'Describa la imagen en detalle.' },
        {
          tipo: 'imagen',
          imagen:
            'https://github.com/vercel/ai/blob/main/examples/ai-core/data/comic-cat.png?raw=true',

          // Opciones específicas de OpenAI - detalles de la imagen:
          opcionesDelProveedor: {
            openai: { imagenDetallada: 'bajo' },
          },
        },
      ],
    },
  ],
});
```

<Nota tipo="advertencia">
  Debido al tipo `UIMensaje` (utilizado por las funciones de hook de UI de SDK de IA como `useChat`) no
  admite la propiedad `opcionesDelProveedor`, puedes utilizar `convertToCoreMessages`
  primero antes de pasar los mensajes a funciones como `generarTexto` o
  `streamText`. Para obtener más detalles sobre el uso de `opcionesDelProveedor`, consulta
  [aquí](/docs/fundamentos/prompts#opciones-del-proveedor).
</Nota>

#### Destilación

OpenAI admite la destilación de modelos para algunos modelos.
Si deseas almacenar una generación para su uso en el proceso de destilación, puedes agregar la opción `store` al objeto `providerOptions.openai`.
Esto guardará la generación en la plataforma OpenAI para su uso posterior en la destilación.

```typescript highlight="9-16"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';
import 'dotenv/config';

async function main() {
  const { text, usage } = await generateText({
    model: openai('gpt-4o-mini'),
    prompt: '¿Quién trabajó en el Macintosh original?',
    providerOptions: {
      openai: {
        store: true,
        metadata: {
          custom: 'value',
        },
      },
    },
  });

  console.log(text);
  console.log();
  console.log('Uso:', usage);
}

main().catch(console.error);
```

#### Caché de Solicitud

OpenAI ha introducido [Caché de Solicitud](https://platform.openai.com/docs/guides/prompt-caching) para modelos compatibles
incluyendo `gpt-4o`, `gpt-4o-mini`, `o1-preview`, y `o1-mini`.

- El caché de solicitud se habilita automáticamente para estos modelos, cuando la solicitud es de 1024 tokens o más larga. No
  necesita ser habilitado explícitamente.
- Puedes utilizar la información de `providerMetadata` para acceder al número de tokens de solicitud que fueron un golpe de caché.
- Tenga en cuenta que el comportamiento de caché depende de la carga en la infraestructura de OpenAI. Los prefijos de solicitud generalmente permanecen en la caché durante 5-10 minutos de inactividad antes de ser expulsados, pero durante períodos de baja demanda pueden persistir durante hasta una hora.

```ts highlight="11"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text, usage, providerMetadata } = await generateText({
  model: openai('gpt-4o-mini'),
  prompt: `Una solicitud de 1024 tokens o más larga...`,
});

console.log(`uso:`, {
  ...usage,
  cachedPromptTokens: providerMetadata?.openai?.cachedPromptTokens,
});
```

#### Entrada de Audio

Con el modelo `gpt-4o-audio-preview`, puedes pasar archivos de audio al modelo.

<Nota tipo="advertencia">
  El modelo `gpt-4o-audio-preview` se encuentra actualmente en versión de prueba y requiere al menos algunos datos de audio. No funcionará con datos no de audio.
</Nota>

```ts highlight="12-14"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const resultado = await generateText({
  modelo: openai('gpt-4o-audio-preview'),
  mensajes: [
    {
      rol: 'usuario',
      contenido: [
        { tipo: 'texto', texto: '¿Qué está diciendo el audio?' },
        {
          tipo: 'archivo',
          mimeType: 'audio/mpeg',
          data: fs.readFileSync('./data/galileo.mp3'),
        },
      ],
    },
  ],
});
```

### Modelos de Respuestas

Puedes utilizar la API de respuestas de OpenAI con el método de fábrica `openai.responses(modelId)`.

```ts
const modelo = openai.responses('gpt-4o-mini');
```

Se puede realizar una configuración adicional utilizando opciones del proveedor de OpenAI.
Puedes validar las opciones del proveedor utilizando el tipo `OpenAIResponsesProviderOptions`.

```ts
import { openai, OpenAIResponsesProviderOptions } from '@ai-sdk/openai';
import { generateText } from 'ai';

const resultado = await generateText({
  modelo: openai.responses('gpt-4o-mini'),
  opcionesDelProveedor: {
    openai: {
      llamadasParalelasHerramientas: false,
      almacenar: false,
      usuario: 'user_123',
      // ...
    } satisface OpenAIResponsesProviderOptions,
  },
  // ...
});
```

Las siguientes opciones del proveedor están disponibles:

- **llamadasParalelasHerramientas** _boolean_
  Si se deben utilizar llamadas paralelas de herramientas. Por defecto es `true`.

- **almacenar** _boolean_
  Si se deben almacenar las generaciones. Por defecto es `true`.

- **metadata** _Registro&lt;string, string&gt;_
  Metadatos adicionales para almacenar con la generación.

- **idDeLaRespuestaAnterior** _string_
  El ID de la respuesta anterior. Puedes utilizarlo para continuar una conversación. Por defecto es `undefined`.

- **instrucciones** _string_
  Instrucciones para el modelo.
  Pueden utilizarse para cambiar el mensaje del sistema o del desarrollador cuando se continúa una conversación utilizando la opción `idDeLaRespuestaAnterior`.
  Por defecto es `undefined`.

- **usuario** _string_
  Un identificador único que representa a tu usuario final, lo que puede ayudar a OpenAI a monitorear y detectar abuso. Por defecto es `undefined`.

- **esfuerzoDeRazonamiento** _'bajo' | 'medio' | 'alto'_
  Esfuerzo de razonamiento para modelos de razonamiento. Por defecto, es `medio`. Si utiliza `providerOptions` para establecer la opción `reasoningEffort`, este ajuste del modelo se ignorará.

- **resumenDeRazonamiento** _'auto' | 'detallado'_
  Controla si el modelo devuelve su proceso de razonamiento. Establezca a `'auto'` para un resumen condensado, `'detallado'` para un razonamiento más completo. Por defecto, es `undefined` (sin resúmenes de razonamiento). Cuando está habilitado, los resúmenes de razonamiento aparecen en el flujo como eventos con tipo `'reasoning'` y en las respuestas no de flujo dentro del campo `reasoning`.

- **esquemasEstrictos** _boolean_
  Si se deben utilizar esquemas JSON estrictos en herramientas y al generar salidas JSON. Por defecto, es `true`.

El proveedor de respuestas de OpenAI también devuelve metadatos específicos del proveedor:

```ts
const { providerMetadata } = await generateText({
  model: openai.responses('gpt-4o-mini'),
});

const openaiMetadata = providerMetadata?.openai;
```

Los siguientes metadatos específicos de OpenAI se devuelven:

- **responseId** _string_
  La ID de la respuesta. Puede usarse para continuar una conversación.

- **cachedPromptTokens** _number_
  El número de tokens de promoción que fueron un golpe de caché.

- **reasoningTokens** _number_
  El número de tokens de razonamiento que el modelo generó.

#### Búsqueda en la Web

El proveedor de respuestas de OpenAI admite la búsqueda en la web a través de la herramienta `openai.tools.webSearchPreview`.

Puede forzar el uso de la herramienta de búsqueda en la web estableciendo el parámetro `toolChoice` en `{ type: 'tool', toolName: 'web_search_preview' }`.

```ts
const resultado = await generarTexto({
  modelo: openai.respuestas('gpt-4o-mini'),
  prompt: '¿Qué sucedió en San Francisco la semana pasada?',
  herramientas: {
    web_search_preview: openai.tools.webSearchPreview({
      // configuración opcional:
      searchContextSize: 'alto',
      ubicaciónDelUsuario: {
        tipo: 'aproximado',
        ciudad: 'San Francisco',
        región: 'California',
      },
    }),
  },
  // Forzar la herramienta de búsqueda en la web:
  toolChoice: { type: 'tool', toolName: 'web_search_preview' },
});

// Fuentes URL
const fuentes = resultado.sources;
```

#### Resúmenes de Razonamiento

Para modelos de razonamiento como `o3-mini`, `o3` y `o4-mini`, puedes habilitar resúmenes de razonamiento para ver el proceso de pensamiento del modelo. Los diferentes modelos admiten diferentes resumidores—por ejemplo, `o4-mini` admite resúmenes detallados. Establece `reasoningSummary: "auto"` para recibir automáticamente el nivel más rico disponible.

```ts highlight="8-9,16"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

const result = streamText({
  model: openai.responses('o4-mini'),
  prompt: 'Habla sobre el debate sobre la burrita Mission en San Francisco.',
  providerOptions: {
    openai: {
      reasoningSummary: 'detailed', // 'auto' para resúmenes condensados o 'detailed' para resúmenes completos
    },
  },
});

for await (const part of result.fullStream) {
  if (part.type === 'reasoning') {
    console.log(`Razonamiento: ${part.textDelta}`);
  } else if (part.type === 'text-delta') {
    process.stdout.write(part.textDelta);
  }
}
```

Para llamadas no de flujo con `generateText`, los resúmenes de razonamiento están disponibles en el campo `reasoning` de la respuesta:

```ts highlight="8-9,13"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const result = await generateText({
  model: openai.responses('o3-mini'),
  prompt: 'Habla sobre el debate sobre la burrita Mission en San Francisco.',
  providerOptions: {
    openai: {
      reasoningSummary: 'auto',
    },
  },
});
console.log('Razonamiento:', result.reasoning);
```

Aprende más sobre resúmenes de razonamiento en la [documentación de OpenAI](https://platform.openai.com/docs/guides/reasoning?api-mode=responses

# Resumen-de-razonamiento).

#### Soporte para PDF

La API de Respuestas de OpenAI admite la lectura de archivos PDF.
Puedes pasar archivos PDF como parte del contenido del mensaje utilizando el tipo `file`:

```ts
const result = await generateText({
  model: openai.responses('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Cuál es un modelo de inmersión?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
          filename: 'ai.pdf', // opcional
        },
      ],
    },
  ],
});
```

El modelo tendrá acceso al contenido del archivo PDF y responderá a preguntas sobre él.
El archivo PDF debe ser pasado utilizando el campo `data`, y el `mimeType` debe estar configurado en `'application/pdf'`.

#### Salidas Estructuradas

La API de Respuestas de OpenAI admite salidas estructuradas. Puedes hacer que las salidas sean estructuradas utilizando `generateObject` o `streamObject`, que expone una opción `schema`. Además, puedes pasar un objeto Zod o JSON Schema a la opción `experimental_output` cuando uses `generateText` o `streamText`.

```ts
// Usando generateObject
const resultado = await generateObject({
  model: openai.responses('gpt-4.1'),
  schema: z.object({
    receta: z.object({
      nombre: z.string(),
      ingredientes: z.array(
        z.object({
          nombre: z.string(),
          cantidad: z.string(),
        }),
      ),
      pasos: z.array(z.string()),
    }),
  }),
  prompt: 'Genera una receta de lasaña.',
});

// Usando generateText
const resultado = await generateText({
  model: openai.responses('gpt-4.1'),
  prompt: '¿Cómo se hace una pizza?',
  experimental_output: Output.object({
    schema: z.object({
      ingredientes: z.array(z.string()),
      pasos: z.array(z.string()),
    }),
  }),
});
```

### Modelos de Completación

Puedes crear modelos que llamen a la [API de completación de OpenAI](https://platform.openai.com/docs/api-reference/completions) utilizando el método de fábrica `.completion()`.
El primer argumento es el ID del modelo.
Actualmente solo se admite `gpt-3.5-turbo-instruct`.

```ts
const model = openai.completion('gpt-3.5-turbo-instruct');
```

Los modelos de completación de OpenAI también admiten algunas configuraciones específicas del modelo que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const model = openai.completion('gpt-3.5-turbo-instruct', {
  echo: true, // opcional, devuelve el prompt en adición a la completación
  logitBias: {
    // opcional, probabilidad de aparición de tokens específicos
    '50256': -100,
  },
  suffix: 'some text', // sufijo opcional que se agrega después de una completación de texto insertado
  user: 'test-user', // identificador de usuario único opcional
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de completación de OpenAI:

- **echo**: _boolean_

  Devuelve el prompt en adición a la completación.

- **logitBias** _Registro&lt;number, number&gt;_

  Modifica la probabilidad de aparición de tokens específicos en la completación.

  Acepta un objeto JSON que mapea tokens (especificados por su ID de token en el tokenizador de GPT) a un valor de sesgo asociado entre -100 y 100. Puedes utilizar esta herramienta de tokenizador para convertir texto a IDs de token. Matemáticamente, el sesgo se suma a los logaritmos generados por el modelo antes de la muestra. El efecto exacto variará por modelo, pero valores entre -1 y 1 deberían disminuir o aumentar la probabilidad de selección; valores como -100 o 100 deberían resultar en una prohibición o selección exclusiva del token relevante.

  Por ejemplo, puedes pasar `{"50256": -100}` para evitar que el token &lt;|endoftext|&gt; se genere.

- **logprobs** _boolean | número_

Devuelve las probabilidades logarítmicas de los tokens. Incluir logprobs aumenta el tamaño de la respuesta y puede ralentizar los tiempos de respuesta. Sin embargo, puede ser útil para comprender mejor cómo se comporta el modelo.

Establecer a true devolverá las probabilidades logarítmicas de los tokens que se generaron.

Establecer a un número devolverá las probabilidades logarítmicas de los n tokens más altos que se generaron.

- **suffix** _cadena_

  La sufija que viene después de una completación de texto insertado.

- **user** _cadena_

  Un identificador único que representa a su usuario final, que puede ayudar a OpenAI a monitorear y detectar abusos. [Aprende más](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

### Capacidad del Modelo

### Resumen

| Modelo                  | Entrada de imagen         | Entrada de audio         | Generación de objetos   | Uso de herramientas          |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `gpt-4.1`              | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4.1-mini`         | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4.1-nano`         | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o`               | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-mini`          | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-audio-preview` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4-turbo`          | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4`                | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `gpt-3.5-turbo`        | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `o1`                   | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `o1-mini`              | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `o1-preview`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `o3-mini`              | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `o3`                   | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `o4-mini`              | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `chatgpt-4o-latest`    | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. Consulte los [documentos de OpenAI](https://platform.openai.com/docs/models) para obtener una lista completa de modelos disponibles. La tabla anterior muestra modelos populares. También puedes pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Integrando Modelos

Puedes crear modelos que llamen a la [API de embebedores de OpenAI](https://platform.openai.com/docs/api-reference/embeddings)
utilizando el método de fábrica `.embedding()`.

```ts
const modelo = openai.embedding('text-embedding-3-large');
```

Los modelos de embebedores de OpenAI admiten varios ajustes adicionales.
Puedes pasarlos como un argumento de opciones:

```ts
const modelo = openai.embedding('text-embedding-3-large', {
  dimensiones: 512 // opcional, número de dimensiones para el embebedor
  usuario: 'test-user' // identificador único del usuario
})
```

Los siguientes ajustes opcionales están disponibles para los modelos de embebedores de OpenAI:

- **dimensiones**: _número_

  El número de dimensiones que deben tener los embebedores de salida resultantes.
  Solo se admite en modelos text-embedding-3 y posteriores.

- **usuario** _cadena_

  Un identificador único que representa a tu usuario final, lo que puede ayudar a OpenAI a
  monitorear y detectar abusos. [Aprende más](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

### Capabilities de los Modelos

| Modelo                    | Dimensiones por defecto | Dimensiones personalizadas   |
| ------------------------ | ------------------ | ------------------- |
| `text-embedding-3-large` | 3072               | <Check size={18} /> |
| `text-embedding-3-small` | 1536               | <Check size={18} /> |
| `text-embedding-ada-002` | 1536               | <Cross size={18} /> |

## Modelos de Imágenes

Puedes crear modelos que llamen a la [API de generación de imágenes de OpenAI](https://platform.openai.com/docs/api-reference/images)
usando el método de fábrica `.image()`.

```ts
const model = openai.image('dall-e-3');
```

<Nota>
  Los modelos Dall-E no admiten el parámetro `aspectRatio`. Utiliza el parámetro `size` en su lugar.
</Nota>

### Capacidad de los Modelos

| Modelo         | Tamaños                           |
| ------------- | ------------------------------- |
| `gpt-image-1` | 1024x1024, 1536x1024, 1024x1536 |
| `dall-e-3`    | 1024x1024, 1792x1024, 1024x1792 |
| `dall-e-2`    | 256x256, 512x512, 1024x1024     |

Puedes pasar opciones `providerOptions` opcionales al modelo de imagen. Estas están sujetas a cambios por parte de OpenAI y dependen del modelo. Por ejemplo, el modelo `gpt-image-1` admite la opción `quality`:

```ts
const { image } = await generateImage({
  model: openai.image('gpt-image-1'),
  prompt: 'Un salamandra al amanecer en un estanque de bosque en las Seychelles.',
  providerOptions: {
    openai: { quality: 'alto' },
  },
});
```

Para más información sobre `generateImage()` consulta [Generación de Imágenes](/docs/ai-sdk-core/image-generation).

Para más información sobre las opciones de modelo de imagen disponibles en OpenAI, consulta la [referencia de la API de OpenAI](https://platform.openai.com/docs/api-reference/images/create).

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de OpenAI](https://platform.openai.com/docs/api-reference/audio/transcribe) 
usando el método de fábrica `.transcription()`.

El primer argumento es el id del modelo, por ejemplo `whisper-1`.

```ts
const modelo = openai.transcription('whisper-1');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo `en`) mejorará la precisión y la latencia.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';

const resultado = await transcribe({
  modelo: openai.transcription('whisper-1'),
  audio: new Uint8Array([1, 2, 3, 4]),
  providerOptions: { openai: { idioma: 'en' } },
});
```

Las siguientes opciones del proveedor están disponibles:

- **timestampGranularities** _string[]_
  La granularidad de los tiempos de la transcripción.
  Por defecto, es `['segment']`.
  Los valores posibles son `['word']`, `['segment']` y `['word', 'segment']`.
  Nota: No hay latencia adicional para los tiempos de segmento, pero generar tiempos de palabra incurre en latencia adicional.

- **idioma** _string_
  El idioma del audio de entrada. Suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo 'en') mejorará la precisión y la latencia.
  Opcional.

- **prompt** _string_
  Un texto opcional para guiar el estilo del modelo o continuar un segmento de audio previo. El prompt debe coincidir con el idioma del audio.
  Opcional.

- **temperatura** _number_
  La temperatura de muestreo, entre 0 y 1. Valores más altos como 0,8 harán que la salida sea más aleatoria, mientras que valores más bajos como 0,2 harán que sea más enfocada y determinista. Si se establece en 0, el modelo utilizará la probabilidad logarítmica para aumentar automáticamente la temperatura hasta que ciertos umbrales se alcancen.
  Se establece por defecto en 0.
  Opcional.

- **incluirla** _string[]_
  Información adicional para incluir en la respuesta de transcripción.

### Capacidad del Modelo

| Modelo                    | Transcripción       | Duración            | Segmentos            | Idioma            |
| ------------------------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper-1`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-mini-transcribe` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `gpt-4o-transcribe`      | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

## Modelos de Habla

Puedes crear modelos que llamen a la [API de habla de OpenAI](https://platform.openai.com/docs/api-reference/audio/speech)
usando el método de fábrica `.speech()`.

El primer argumento es el id del modelo, por ejemplo `tts-1`.

```ts
const modelo = openai.speech('tts-1');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrando una voz para utilizar en el audio generado.

```ts highlight="6"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';

const resultado = await generateSpeech({
  modelo: openai.speech('tts-1'),
  texto: 'Hola, mundo!',
  providerOptions: { openai: {} },
});
```

- **instrucciones** _cadena de texto_
  Controla la voz de tu audio generado con instrucciones adicionales, por ejemplo "Habla en un tono lento y constante".
  No funciona con `tts-1` o `tts-1-hd`.
  Opcional.

- **formato_de_la_respuesta** _cadena de texto_
  El formato del audio.
  Los formatos soportados son `mp3`, `opus`, `aac`, `flac`, `wav` y `pcm`.
  Por defecto es `mp3`.
  Opcional.

- **velocidad** _número_
  La velocidad del audio generado.
  Selecciona un valor entre 0.25 y 4.0.
  Por defecto es 1.0.
  Opcional.

### Capabilidades del Modelo

| Modelo             | Instrucciones        |
| ----------------- | ------------------- |
| `tts-1`           | <Check size={18} /> |
| `tts-1-hd`        | <Check size={18} /> |
| `gpt-4o-mini-tts` | <Check size={18} /> |

---
title: Proveedor de Azure OpenAI
description: Aprende a utilizar el proveedor de Azure OpenAI para el SDK de AI.
---

# Proveedor de Azure OpenAI

El [Proveedor de Azure OpenAI](https://azure.microsoft.com/es-es/products/ai-services/openai-service) contiene soporte para modelos de lenguaje del servicio de chat de Azure OpenAI.

## Configuración

El proveedor de Azure OpenAI está disponible en el módulo `@ai-sdk/azure`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/azure" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/azure" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/azure" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia del proveedor predeterminada `azure` de `@ai-sdk/azure`:

```ts
import { azure } from '@ai-sdk/azure';
```

Si necesitas una configuración personalizada, puedes importar `createAzure` de `@ai-sdk/azure` y crear una instancia del proveedor con tus ajustes:

```ts
import { createAzure } from '@ai-sdk/azure';

const azure = createAzure({
  resourceName: 'tu-nombre-de-recurso-azure', // Nombre del recurso de Azure
  apiKey: 'tu-clave-api',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor de OpenAI:

- **resourceName** _cadena_

  Nombre del recurso de Azure.
  Por defecto se utiliza el valor de la variable de entorno `AZURE_RESOURCE_NAME`.

  El nombre del recurso se utiliza en la URL ensamblada: `https://{resourceName}.openai.azure.com/openai/deployments/{modelId}{path}`.
  Puedes utilizar `baseURL` en su lugar para especificar el prefijo de la URL.

- **apiKey** _cadena_

  Clave API que se envía utilizando el encabezado `api-key`.
  Por defecto se utiliza el valor de la variable de entorno `AZURE_API_KEY`.

- **apiVersion** _cadena_

  Establece una versión personalizada de la [API](https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation).
  Por defecto es `2024-10-01-preview`.

- **baseURL** _cadena_

  Utiliza un prefijo de URL diferente para las llamadas a la API, por ejemplo, para utilizar servidores de proxy.

  O bien este o `resourceName` se pueden utilizar.
  Cuando se proporciona una baseURL, el resourceName se ignora.

  Con una baseURL, la URL resuelta es `{baseURL}/{modelId}{path}`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

## Modelos de Lenguaje

La instancia del proveedor de Azure OpenAI es una función que puedes invocar para crear un modelo de lenguaje:

```ts
const model = azure('tu-nombre-de-despliegue');
```

Necesitas pasar el nombre de tu despliegue como el primer argumento.

### Modelos de Razonamiento

Azure expone el pensamiento de `DeepSeek-R1` en el texto generado utilizando la etiqueta `<think>`.
Puedes utilizar el `extractReasoningMiddleware` para extraer esta razonamiento y exponerlo como una propiedad `reasoning` en el resultado:

```ts
import { azure } from '@ai-sdk/azure';
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const modeloMejorado = wrapLanguageModel({
  model: azure('tu-nombre-de-despliegue-de-deepseek-r1'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Puedes utilizar ese modelo mejorado en funciones como `generateText` y `streamText`.

### Ejemplo

Puedes utilizar modelos de lenguaje de OpenAI para generar texto con la función `generateText`:

```ts
import { azure } from '@ai-sdk/azure';
import { generateText } from 'ai';

const { texto } = await generateText({
  model: azure('tu-nombre-de-despliegue'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de OpenAI también se pueden utilizar en las funciones `streamText`, `generateObject` y `streamObject` (ver [AI SDK Core](/docs/ai-sdk-core)).

<Nota>
  Azure OpenAI envía trozos más grandes que OpenAI. Esto puede llevar a la percepción de que la respuesta es más lenta. Consulta [Solucionar Problemas: Azure OpenAI Lento Para Transmitir](/docs/troubleshooting/common-issues/azure-stream-slow)
</Nota>

### Opciones del Proveedor

Al utilizar modelos de lenguaje de OpenAI en Azure, puede configurar opciones específicas del proveedor utilizando `providerOptions.openai`. Más información sobre las opciones de configuración disponibles se encuentra en [la página del proveedor de OpenAI](/providers/ai-sdk-providers/openai#modelos-de-lenguaje).

```ts highlight="12-14,22-24"
const mensajes = [
  {
    rol: 'user',
    contenido: [
      {
        tipo: 'text',
        texto: '¿Cuál es la capital de la luna?',
      },
      {
        tipo: 'imagen',
        imagen: 'https://example.com/image.png',
        providerOptions: {
          openai: { imagenDetalle: 'bajo' },
        },
      },
    ],
  },
];

const { texto } = await generarTexto({
  modelo: azure('nombre-de-deploy'),
  providerOptions: {
    openai: {
      esfuerzoDeRazonamiento: 'bajo',
    },
  },
});
```

### Modelos de Chat

<Nota>
  La URL para llamar a los modelos de chat de Azure se construirá de la siguiente manera:
  `https://RESOURCE_NAME.openai.azure.com/openai/deployments/DEPLOYMENT_NAME/chat/completions?api-version=API_VERSION`
</Nota>

Los modelos de chat de Azure OpenAI también admiten algunas configuraciones específicas del modelo que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const model = azure('your-deployment-name', {
  logitBias: {
    // valor de probabilidad opcional para tokens específicos
    '50256': -100,
  },
  user: 'test-user', // identificador de usuario único opcional
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de chat de OpenAI:

- **logitBias** _Registro&lt;number, number&gt;_

  Modifica la probabilidad de que los tokens específicos aparezcan en la completación.

  Acepta un objeto JSON que mapea tokens (especificados por su ID de token en el tokenizador GPT) a un valor de sesgo asociado entre -100 y 100. Puedes usar esta herramienta de tokenizador para convertir texto a IDs de token. Matemáticamente, el sesgo se suma a los logits generados por el modelo antes de la muestra. El efecto exacto variará por modelo, pero valores entre -1 y 1 deberían disminuir o aumentar la probabilidad de selección; valores como -100 o 100 deberían resultar en una prohibición o selección exclusiva del token relevante.

  Por ejemplo, puedes pasar `{"50256": -100}` para evitar que el token se genere.

- **logprobs** _boolean | number_

  Devuelve las probabilidades logarítmicas de los tokens. Incluir logprobs aumentará el tamaño de la respuesta y puede ralentizar los tiempos de respuesta. Sin embargo, puede ser útil para comprender mejor cómo se está comportando el modelo.

  Establecer a true devolverá las probabilidades logarítmicas de los tokens que se generaron.

  Establecer a un número devolverá las probabilidades logarítmicas de los n tokens más relevantes que se generaron.

- **parallelToolCalls** _boolean_

- **usuario** _string_

  Un identificador único que representa a tu usuario final, lo que puede ayudar a OpenAI a
  monitorear y detectar abuso. Aprende más.

### Modelos de Respuesta

Puedes utilizar la API de respuestas de OpenAI de Azure con el método de fábrica `azure.responses(deploymentName)`.

```ts
const model = azure.responses('nombre-de-tu-despliegue');
```

Se puede realizar una configuración adicional utilizando opciones del proveedor de OpenAI.
Puedes validar las opciones del proveedor utilizando el tipo `OpenAIResponsesProviderOptions`.

```ts
import { azure, OpenAIResponsesProviderOptions } from '@ai-sdk/azure';
import { generateText } from 'ai';

const result = await generateText({
  model: azure.responses('nombre-de-tu-despliegue'),
  providerOptions: {
    openai: {
      parallelToolCalls: false,
      store: false,
      user: 'user_123',
      // ...
    } satisfies OpenAIResponsesProviderOptions,
  },
  // ...
});
```

Las siguientes opciones del proveedor están disponibles:

- **parallelToolCalls** _boolean_
  Si se deben realizar llamadas paralelas a herramientas. Por defecto es `true`.

- **store** _boolean_
  Si se debe almacenar la generación. Por defecto es `true`.

- **metadata** _Registro&lt;string, string&gt;_
  Metadatos adicionales para almacenar con la generación.

- **previousResponseId** _string_
  El ID de la respuesta anterior. Puedes utilizarlo para continuar una conversación. Por defecto es `undefined`.

- **instructions** _string_
  Instrucciones para el modelo.
  Pueden utilizarse para cambiar el mensaje del sistema o del desarrollador cuando se continua una conversación utilizando la opción `previousResponseId`.
  Por defecto es `undefined`.

- **user** _string_
  Un identificador único que representa a tu usuario final, lo que puede ayudar a OpenAI a monitorear y detectar abuso. Por defecto es `undefined`.

- **esfuerzoDeRazonamiento** _'bajo' | 'medio' | 'alto'_
  Esfuerzo de razonamiento para modelos de razonamiento. Por defecto, es `medio`. Si utiliza `providerOptions` para establecer la opción `reasoningEffort`, este ajuste del modelo se ignorará.

- **esquemasEstrictos** _boolean_
  Si se deben utilizar esquemas JSON estrictos en herramientas y al generar salidas JSON. Por defecto, es `true`.

El proveedor de respuestas de Azure OpenAI también devuelve metadatos específicos del proveedor:

```ts
const { providerMetadata } = await generateText({
  model: azure.responses('nombre-de-su-despliegue'),
});

const openaiMetadata = providerMetadata?.openai;
```

Los siguientes metadatos específicos de OpenAI se devuelven:

- **responseId** _cadena_
  El ID de la respuesta. Puede usarse para continuar una conversación.

- **tokensDePromptCachados** _número_
  El número de tokens de promoción que fueron un golpe de caché.

- **tokensDeRazonamiento** _número_
  El número de tokens de razonamiento que el modelo generó.

#### Soporte de PDF

La API de Respuestas de OpenAI de Azure admite la lectura de archivos PDF.
Puedes pasar archivos PDF como parte del contenido del mensaje utilizando el tipo `file`:

```ts
const result = await generateText({
  model: azure.responses('your-deployment-name'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Qué es un modelo de inmersión?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
          filename: 'ai.pdf', // opcional
        },
      ],
    },
  ],
});
```

El modelo tendrá acceso a los contenidos del archivo PDF y
respondrá a preguntas sobre él.
El archivo PDF debe ser pasado utilizando el campo `data`,
y el `mimeType` debe estar configurado en `'application/pdf'`.

### Modelos de Completación

Puedes crear modelos que llamen a la API de completación utilizando el método de fábrica `.completion()`.
El primer argumento es el id del modelo.
Actualmente solo se admite `gpt-35-turbo-instruct`.

```ts
const modelo = azure.completion('tu-deploy-gpt-35-turbo-instruct');
```

Los modelos de completación de OpenAI admiten también algunas configuraciones específicas del modelo que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const modelo = azure.completion('tu-deploy-gpt-35-turbo-instruct', {
  echo: true, // opcional, devuelve el prompt en lugar de la completación
  logitBias: {
    // opcional, modifica la probabilidad de aparición de tokens específicos
    '50256': -100,
  },
  suffix: 'texto adicional', // opcional, texto que se agrega después de una completación de texto insertado
  user: 'test-user', // opcional, identificador de usuario único
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de completación de Azure OpenAI:

- **echo**: _boolean_

  Devuelve el prompt en lugar de la completación.

- **logitBias** _Registro&lt;number, number&gt;_

  Modifica la probabilidad de aparición de tokens específicos en la completación.

  Acepta un objeto JSON que mapea tokens (especificados por su id de token en el tokenizador GPT) a un valor de sesgo asociado entre -100 y 100. Puedes utilizar esta herramienta de tokenizador para convertir texto a ids de token. Matemáticamente, el sesgo se agrega a los logits generados por el modelo antes de la muestra. El efecto exacto variará por modelo, pero valores entre -1 y 1 deberían disminuir o aumentar la probabilidad de selección; valores como -100 o 100 deberían resultar en una prohibición o selección exclusiva del token relevante.

  Por ejemplo, puedes pasar `{"50256": -100}` para evitar que el token &lt;|endoftext|&gt; se genere.

- **logprobs** _boolean | number_

Devuelve las probabilidades logarítmicas de los tokens. Incluir logprobs aumenta el tamaño de la respuesta y puede ralentizar los tiempos de respuesta. Sin embargo, puede ser útil para comprender mejor cómo se comporta el modelo.

Establecer a true devolverá las probabilidades logarítmicas de los tokens que se generaron.

Establecer a un número devolverá las probabilidades logarítmicas de los n tokens más altos que se generaron.

- **suffix** _cadena_

  La sufija que viene después de una completación de texto insertado.

- **user** _cadena_

  Un identificador único que representa a su usuario final, lo que puede ayudar a OpenAI a monitorear y detectar abuso. Aprende más.

## Integrando Modelos

Puedes crear modelos que llamen a la API de embeddings de Azure OpenAI utilizando el método de fabricación `.embedding()`.

```ts
const modelo = azure.embedding('tu-despliegue-de-embeddings');
```

Los modelos de embeddings de Azure OpenAI admiten varias configuraciones adicionales. Puedes pasarlas como un argumento de opciones:

```ts
const modelo = azure.embedding('tu-despliegue-de-embeddings', {
  dimensiones: 512 // opcional, número de dimensiones para el embedding
  usuario: 'test-user' // identificador único del usuario, opcional
})
```

Las siguientes configuraciones opcionales están disponibles para los modelos de embeddings de Azure OpenAI:

- **dimensiones**: _número_

  El número de dimensiones que deben tener los embeddings de salida resultantes.
  Solo se admite en modelos de texto con nombre `text-embedding-3` y posteriores.

- **usuario** _cadena_

  Un identificador único que representa a tu usuario final, lo que puede ayudar a OpenAI a monitorear y detectar el abuso. Aprende más.

## Modelos de Imágenes

Puedes crear modelos que llamen a la API de generación de imágenes de Azure OpenAI (DALL-E) utilizando el método de fabricación `.imageModel()`.

```ts
const modelo = azure.imageModel('tu-nombre-de-despliegue-del-modelo-DALL-E');
```

Los modelos de imágenes de Azure OpenAI admiten varias configuraciones adicionales. Puedes pasarlas como un argumento de opciones:

```ts
const modelo = azure.imageModel('tu-nombre-de-despliegue-del-modelo-DALL-E', {
  usuario: 'test-user', // identificador único del usuario, opcional
  formatoDeRespuesta: 'url', // 'url' o 'b64_json', predeterminado es 'url'
});
```

### Ejemplo

Puedes utilizar modelos de imágenes de Azure OpenAI para generar imágenes con la función `generateImage`:

```ts
import { azure } from '@ai-sdk/azure';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: azure.imageModel('nombre-de-deploy-para-dalle-tu'),
  prompt: 'Una imagen fotorealista de un gato astronauta flotando en el espacio',
  size: '1024x1024', // '1024x1024', '1792x1024', o '1024x1792' para DALL-E 3
});

// image contiene la URL o datos base64 de la imagen generada
console.log(image);
```

### Capacidad del Modelo

Azure OpenAI admite modelos DALL-E 2 y DALL-E 3 a través de despliegues. Las capacidades dependen de la versión del modelo que esté utilizando su despliegue:

| Versión del Modelo | Tamaños                          |
| ------------------ | ---------------------------------- |
| DALL-E 3           | 1024x1024, 1792x1024, 1024x1792  |
| DALL-E 2           | 256x256, 512x512, 1024x1024      |

<Nota>
  Los modelos DALL-E no admiten el parámetro `aspectRatio`. Utiliza el parámetro `size` en su lugar.
</Nota>

<Nota>
  Al crear su despliegue de Azure OpenAI, asegúrese de establecer la versión del modelo DALL-E que desee utilizar.
</Nota>

## Modelos de Transcripción

Puedes crear modelos que llamen a la API de transcripción de Azure OpenAI utilizando el método de fábrica `.transcription()`.

El primer argumento es el identificador del modelo, por ejemplo `whisper-1`.

```ts
const modelo = azure.transcription('whisper-1');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo, `en`) mejorará la precisión y la latencia.

```ts highlight="6"
import { experimental_transcribe as transcribir } from 'ai';
import { azure } from '@ai-sdk/azure';
import { readFile } from 'fs/promises';

const resultado = await transcribir({
  modelo: azure.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
  providerOptions: { azure: { idioma: 'en' } },
});
```

Las siguientes opciones de proveedor están disponibles:

- **timestampGranularities** _string[]_
  La granularidad de los tiempos en la transcripción.
  Por defecto, es `['segment']`.
  Los valores posibles son `['palabra']`, `['segment']` y `['palabra', 'segment']`.
  Nota: No hay latencia adicional para los tiempos de segmento, pero generar tiempos de palabra incurre en latencia adicional.

- **idioma** _string_
  El idioma del audio de entrada. Suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo, 'en') mejorará la precisión y la latencia.
  Opcional.

- **prompt** _string_
  Un texto opcional para guiar el estilo o continuar un segmento de audio previo. El prompt debe coincidir con el idioma del audio.
  Opcional.

- **temperatura** _number_
  La temperatura de muestreo, entre 0 y 1. Valores más altos como 0,8 harán que el resultado sea más aleatorio, mientras que valores más bajos como 0,2 lo harán más enfocado y determinista. Si se establece en 0, el modelo utilizará la probabilidad logarítmica para aumentar automáticamente la temperatura hasta ciertos umbrales.
  Por defecto, es 0.
  Opcional.

- **include** _cadena[]_
  Información adicional para incluir en la respuesta de transcripción.

### Capabilities del Modelo

| Modelo                    | Transcripción       | Duración            | Segmentos            | Idioma            |
| ------------------------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper-1`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-mini-transcribe` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `gpt-4o-transcribe`      | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

---
title: Anthropic
description: Aprende a utilizar el proveedor Anthropic para el SDK de IA.
---

# Proveedor Anthropic

El [proveedor Anthropic](https://www.anthropic.com/) contiene soporte para modelos de lenguaje en la [API de Mensajes de Anthropic](https://docs.anthropic.com/claude/reference/messages_post).

## Configuración

El proveedor Anthropic está disponible en el módulo `@ai-sdk/anthropic`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/anthropic" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/anthropic" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/anthropic" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `anthropic` desde `@ai-sdk/anthropic`:

```ts
import { anthropic } from '@ai-sdk/anthropic';
```

Si necesitas una configuración personalizada, puedes importar `createAnthropic` desde `@ai-sdk/anthropic` y crear una instancia de proveedor con tus ajustes:

```ts
import { createAnthropic } from '@ai-sdk/anthropic';

const anthropic = createAnthropic({
  // ajustes personalizados
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Anthropic:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para las llamadas a la API, por ejemplo, para utilizar servidores de proxy.
  El prefijo predeterminado es `https://api.anthropic.com/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `x-api-key`.
  Por defecto, utiliza la variable de entorno `ANTHROPIC_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para pruebas, por ejemplo.

## Modelos de Lenguaje

Puedes crear modelos que llamen a la [API de Mensajes de Anthropic](https://docs.anthropic.com/claude/reference/messages_post) utilizando la instancia del proveedor.
El primer argumento es el id del modelo, por ejemplo `claude-3-haiku-20240307`.
Algunos modelos tienen capacidades multi-modales.

```ts
const model = anthropic('claude-3-haiku-20240307');
```

Puedes utilizar modelos de lenguaje de Anthropic para generar texto con la función `generateText`:

```ts
import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

const { text } = await generateText({
  model: anthropic('claude-3-haiku-20240307'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Anthropic también se pueden utilizar en las funciones `streamText`, `generateObject` y `streamObject` (ver [AI SDK Core](/docs/ai-sdk-core)).

<Nota>
  La API de Anthropic devuelve llamadas a herramientas de flujo de datos todas a la vez después de un retraso. Esto
  causa que la función `streamObject` genere el objeto completamente después de un retraso
  en lugar de enviarlo de forma incremental.
</Nota>

Los siguientes ajustes opcionales están disponibles para modelos de Anthropic:

- `sendReasoning` _boolean_

  Opcional. Incluir contenido de razonamiento en las solicitudes enviadas al modelo. Por defecto es `true`.

  Si estás experimentando problemas con el modelo al manejar solicitudes que involucran contenido de razonamiento, puedes establecer esto en `false` para omitirlo de la solicitud.

### Razonamiento

Anthropic tiene soporte para razonamiento para los modelos `claude-4-opus-20250514`, `claude-4-sonnet-20250514`, y `claude-3-7-sonnet-20250219`.

Puedes habilitarlo utilizando la opción de proveedor `thinking` y especificando un presupuesto de tokens.

```ts
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

const { text, reasoning, reasoningDetails } = await generateText({
  model: anthropic('claude-4-opus-20250514'),
  prompt: '¿Cuántas personas vivirán en el mundo en 2040?',
  providerOptions: {
    anthropic: {
      thinking: { type: 'enabled', budgetTokens: 12000 },
    } satisfies AnthropicProviderOptions,
  },
});

console.log(reasoning); // texto de razonamiento
console.log(reasoningDetails); // detalles del razonamiento incluyendo razonamiento restringido
console.log(text); // respuesta de texto
```

Consulte [AI SDK UI: Chatbot](/docs/ai-sdk-ui/chatbot#razonamiento) para obtener más detalles
sobre cómo integrar el razonamiento en tu chatbot.

### Control de Cache

<Nota>
  El control de cache de Anthropic originalmente era una característica beta y requería pasar una configuración de `cacheControl` opt-in al crear la instancia del modelo. Ahora está Generalmente Disponible y está habilitado por defecto. La configuración `cacheControl` ya no es necesaria y se eliminará en una futura versión.
</Nota>

En los mensajes y partes de mensaje, puedes utilizar la propiedad `providerOptions` para establecer puntos de ruptura de control de cache.
Debes establecer la propiedad `anthropic` en el objeto `providerOptions` a `{ cacheControl: { type: 'ephemeral' } }` para establecer un punto de ruptura de control de cache.

Los tokens de creación de cache se devuelven en el objeto `providerMetadata` para `generateText` y `generateObject`, nuevamente bajo la propiedad `anthropic`.
Cuando utilizas `streamText` o `streamObject`, la respuesta contiene una promesa que se resuelve al metadata. Alternativamente, puedes recibirlo en el callback `onFinish`.

```ts highlight="8,18-20,29-30"
import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

const errorMessage = '... largo mensaje de error ...';
```

```javascript
const resultado = await generarTexto({
  modelo: anthropic('claude-3-5-sonnet-20240620'),
  mensajes: [
    {
      rol: 'usuario',
      contenido: [
        { tipo: 'texto', texto: 'Eres un experto en JavaScript.' },
        {
          tipo: 'texto',
          texto: `Mensaje de error: ${errorMessage}`,
          opcionesProveedor: {
            anthropic: { cacheControl: { tipo: 'transitorio' } },
          },
        },
        { tipo: 'texto', texto: 'Explica el mensaje de error.' },
      ],
    },
  ],
});

console.log(resultado.texto);
console.log(resultado.providerMetadata?.anthropic);
// e.g. { cacheCreationInputTokens: 2118, cacheReadInputTokens: 0 }
```

También puedes utilizar el control de caché en mensajes del sistema proporcionando múltiples mensajes del sistema al comienzo de tu arreglo de mensajes:

```ts highlight="3,7-9"
const resultado = await generarTexto({
  modelo: anthropic('claude-3-5-sonnet-20240620'),
  mensajes: [
    {
      rol: 'sistema',
      contenido: 'Parte de mensaje del sistema en caché',
      opcionesDelProveedor: {
        anthropic: { controlDeCaché: { tipo: 'ephemeral' } },
      },
    },
    {
      rol: 'sistema',
      contenido: 'Parte de mensaje del sistema no en caché',
    },
    {
      rol: 'usuario',
      contenido: 'Pregunta del usuario',
    },
  ],
});
```

La longitud mínima de la pregunta cachable es:

- 1024 tokens para Claude 3.7 Sonnet, Claude 3.5 Sonnet y Claude 3 Opus
- 2048 tokens para Claude 3.5 Haiku y Claude 3 Haiku

Las preguntas más cortas no pueden ser almacenadas en caché, incluso si se marcan con `cacheControl`. Cualquier solicitud para almacenar en caché un número menor de tokens se procesará sin caché.

Para más información sobre el almacenamiento en caché de preguntas con Anthropic, consulte la [documentación de control de caché de Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching).

<Nota tipo="advertencia">
  Debido a que el tipo `UIMessage` (utilizado por las llamadas a hooks de UI de SDK de IA como `useChat`) no admite la propiedad `providerOptions`, puede utilizar `convertToCoreMessages` primero antes de pasar los mensajes a funciones como `generateText` o `streamText`. Para obtener más detalles sobre el uso de `providerOptions`, consulte [aquí](/docs/foundations/prompts)

# Opciones-del-proveedor).

</Nota>

### Uso del Ordenador

Anthropic proporciona tres herramientas integradas que se pueden utilizar para interactuar con sistemas externos:

1. **Herramienta de Bash**: Permite ejecutar comandos de Bash.
2. **Herramienta de Editor de Texto**: Proporciona funcionalidad para ver y editar archivos de texto.
3. **Herramienta del Ordenador**: Habilita el control de acciones de teclado y mouse en un ordenador.

Están disponibles a través de la propiedad `tools` de la instancia del proveedor.

#### Herramienta de Bash

La Herramienta de Bash permite ejecutar comandos de Bash. Aquí está cómo crear y utilizarla:

```ts
const bashTool = anthropic.tools.bash_20241022({
  execute: async ({ command, restart }) => {
    // Implementa la lógica de ejecución de comandos de Bash aquí
    // Devuelve el resultado de la ejecución del comando
  },
});
```

Parámetros:

- `command` (cadena de texto): El comando de Bash a ejecutar. Requerido a menos que la herramienta esté siendo reiniciada.
- `restart` (booleano, opcional): Especificar verdadero reiniciará esta herramienta.

#### Herramienta de Editor de Texto

La Herramienta de Editor de Texto proporciona funcionalidad para visualizar y editar archivos de texto:

```ts
const textEditorTool = anthropic.tools.textEditor_20241022({
  execute: async ({
    command,
    path,
    file_text,
    insert_line,
    new_str,
    old_str,
    view_range,
  }) => {
    // Implemente la lógica de edición de texto aquí
    // Devuelva el resultado de la operación de edición de texto
  },
});
```

Parámetros:

- `command` ('view' | 'create' | 'str_replace' | 'insert' | 'undo_edit'): La orden a ejecutar.
- `path` (string): Ruta absoluta al archivo o directorio, por ejemplo `/repo/file.py` o `/repo`.
- `file_text` (string, opcional): Requerido para la orden `create`, con el contenido del archivo a crear.
- `insert_line` (number, opcional): Requerido para la orden `insert`. El número de línea después de la cual insertar la nueva cadena.
- `new_str` (string, opcional): Nueva cadena para las órdenes `str_replace` o `insert`.
- `old_str` (string, opcional): Requerido para la orden `str_replace`, conteniendo la cadena a reemplazar.
- `view_range` (number[], opcional): Opcional para la orden `view` para especificar el rango de líneas a mostrar.

Al utilizar la Herramienta de Editor de Texto, asegúrese de nombrar la clave en el objeto de herramientas `str_replace_editor`.

```ts
const response = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  prompt:
    "Cree un nuevo archivo llamado ejemplo.txt, escriba 'Hola Mundo' en él y ejecute 'cat ejemplo.txt' en la terminal",
  tools: {
    str_replace_editor: textEditorTool,
  },
});
```

#### Herramienta de Computadora

La Herramienta de Computadora permite el control de acciones de teclado y ratón en una computadora:

```ts
const computerTool = anthropic.tools.computer_20241022({
  anchoDePantallaPx: 1920,
  altoDePantallaPx: 1080,
  numeroDePantalla: 0, // Opcional, para entornos X11

  execute: async ({ acción, coordenada, texto }) => {
    // Implemente la lógica de control de la computadora aquí
    // Devuelva el resultado de la acción

    // Código de ejemplo:
    switch (acción) {
      case 'capturaDePantalla': {
        // resultado multipart:
        return {
          tipo: 'imagen',
          data: fs
            .readFileSync('./data/screenshot-editor.png')
            .toString('base64'),
        };
      }
      default: {
        console.log('Acción:', acción);
        console.log('Coordenada:', coordenada);
        console.log('Texto:', texto);
        return `se ejecutó ${acción}`;
      }
    }
  },

  // mapa a contenido de resultado de herramienta para consumo de LLM:
  experimental_toToolResultContent(result) {
    return typeof result === 'string'
      ? [{ tipo: 'texto', texto: result }]
      : [{ tipo: 'imagen', data: result.data, mimeType: 'image/png' }];
  },
});
```

Parámetros:

- `action` ('key' | 'type' | 'mouse_move' | 'left_click' | 'left_click_drag' | 'right_click' | 'middle_click' | 'double_click' | 'screenshot' | 'cursor_position'): La acción a realizar.
- `coordinate` (number[], opcional): Requerido para las acciones `mouse_move` y `left_click_drag`. Specifica las coordenadas (x, y).
- `text` (string, opcional): Requerido para las acciones `type` y `key`.

Estas herramientas pueden utilizarse conjuntamente con el modelo `sonnet-3-5-sonnet-20240620` para habilitar interacciones y tareas más complejas.

### Soporte de PDF

Anthropic Sonnet `claude-3-5-sonnet-20241022` admite la lectura de archivos PDF.
Puedes pasar archivos PDF como parte del contenido del mensaje utilizando el tipo `file`:

Opción 1: Documento PDF basado en URL

```ts
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Cuál es el modelo de inmersión según este documento?',
        },
        {
          type: 'file',
          data: new URL(
            'https://github.com/vercel/ai/blob/main/examples/ai-core/data/ai.pdf?raw=true',
          ),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
});
```

Opción 2: Documento PDF codificado en Base64

```typescript
const resultado = await generarTexto({
  modelo: anthropic('claude-3-5-sonnet-20241022'),
  mensajes: [
    {
      rol: 'user',
      contenido: [
        {
          tipo: 'text',
          texto: '¿Qué es un modelo de embedding según este documento?',
        },
        {
          tipo: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
});
```

El modelo tendrá acceso al contenido del archivo PDF y responderá a preguntas sobre él.
El archivo PDF debe ser pasado utilizando el campo `data` y el `mimeType` debe estar configurado en `application/pdf`.

### Capacidad del Modelo

### Resumen

| Modelo                        | Entrada de imagen         | Generación de objetos   | Uso de herramientas          | Uso de computadora        |
| ---------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `claude-4-opus-20250514`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-4-sonnet-20250514`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-7-sonnet-20250219` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-5-sonnet-20241022` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-5-sonnet-20240620` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-5-haiku-20241022`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-opus-20240229`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-sonnet-20240229`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

| `claude-3-haiku-20240307`    | <Verifica tamaño={18} /> | <Verifica tamaño={18} /> | <Verifica tamaño={18} /> | <Cruce tamaño={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. Consulte los [docs de Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) para obtener una lista completa de modelos disponibles. La tabla anterior muestra modelos populares. También puede pasar como cadena el ID del modelo de proveedor disponible si es necesario.
</Nota>

---
titulo: Amazon Bedrock
descripcion: Aprenda a usar el proveedor Amazon Bedrock.
---

# Proveedor de Amazon Bedrock

El proveedor de Amazon Bedrock para el [SDK de Inteligencia Artificial](/docs) contiene soporte para modelos de lenguaje en las API de [Amazon Bedrock](https://aws.amazon.com/bedrock).

## Configuración

El proveedor de Bedrock está disponible en el módulo `@ai-sdk/amazon-bedrock`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/amazon-bedrock" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/amazon-bedrock" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/amazon-bedrock" dark />
  </Tab>
</Tabs>

### Requisitos previos

El acceso a los modelos de fundación de Amazon Bedrock no se concede por defecto. Para obtener acceso a un modelo de fundación, un usuario IAM con permisos suficientes debe solicitar acceso a través de la consola. Una vez que se proporciona acceso a un modelo, está disponible para todos los usuarios de la cuenta.

Consulte los [Documentos de Acceso a Modelos](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) para obtener más información.

### Autenticación

#### Utilizando la Clave de Acceso IAM y la Clave Secreta

**Paso 1: Crear Clave de Acceso AWS y Clave Secreta**

Para empezar, necesitarás crear una clave de acceso AWS y una clave secreta. Aquí está cómo hacerlo:

**Iniciar sesión en la Consola de Administración de AWS**

- Ve a la [Consola de Administración de AWS](https://console.aws.amazon.com/) y inicia sesión con tus credenciales de cuenta AWS.

**Crear un Usuario IAM**

- Navega a la [pantalla de inicio de IAM](https://console.aws.amazon.com/iam/home) y haz clic en "Usuarios" en el menú de navegación de la izquierda.
- Haz clic en "Crear usuario" y rellena los detalles necesarios para crear un nuevo usuario IAM.
- Asegúrate de seleccionar "Acceso programático" como tipo de acceso.
- La cuenta de usuario necesita la política `AmazonBedrockFullAccess` adjunta a ella.

**Crear Clave de Acceso**

- Haz clic en la pestaña "Credenciales de seguridad" y luego haz clic en "Crear clave de acceso".
- Haz clic en "Crear clave de acceso" para generar una nueva pareja de clave de acceso.
- Descarga el archivo `.csv` que contiene la ID de clave de acceso y la clave secreta de acceso.

**Paso 2: Configurando la Clave de Acceso y la Clave Secreta**

Dentro de tu proyecto, agrega un archivo `.env` si no lo tienes ya. Este archivo se utilizará para establecer la clave de acceso y la clave secreta como variables de entorno. Añade las siguientes líneas al archivo `.env`:

```makefile
AWS_ACCESS_KEY_ID=TU_CLAVE_DE_ACCESO_ID
AWS_SECRET_ACCESS_KEY=TU_CLAVE_SECRETA_DE_ACCESO
AWS_REGION=TU_REGION
```

<Nota>
  Muchas frameworks como [Next.js](https://nextjs.org/) cargan automáticamente el archivo `.env`.
  Si estás utilizando una framework diferente, es posible que debas cargar el archivo `.env` manualmente utilizando un paquete como
  [`dotenv`](https://github.com/motdotla/dotenv).
</Nota>

Recuerda reemplazar `TU_CLAVE_DE_ACCESO_ID`, `TU_CLAVE_SECRETA_DE_ACCESO` y `TU_REGION` con los valores reales de tu cuenta de AWS.

#### Usando la Cadena de Credenciales de AWS SDK (perfiles de instancia, roles de instancia, roles de ECS, cuentas de servicio de EKS, etc.)

Cuando se utiliza AWS SDK, el SDK utilizará automáticamente la cadena de credenciales para determinar las credenciales a utilizar. Esto incluye perfiles de instancia, roles de instancia, roles de ECS, cuentas de servicio de EKS, etc. Un comportamiento similar es posible utilizando el SDK de AI al no especificar las propiedades `accessKeyId` y `secretAccessKey`, `sessionToken` en la configuración del proveedor y en su lugar pasar una propiedad `credentialProvider`.

_Usos:_

El paquete `@aws-sdk/credential-providers` proporciona una serie de proveedores de credenciales que se pueden utilizar para crear una cadena de proveedores de credenciales.

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @aws-sdk/credential-providers" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @aws-sdk/credential-providers" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @aws-sdk/credential-providers" dark />
  </Tab>
</Tabs>

```ts
import { createAmazonBedrock } from '@ai-sdk/amazon-bedrock';
import { fromNodeProviderChain } from '@aws-sdk/credential-providers';

const bedrock = createAmazonBedrock({
  region: 'us-east-1',
  credentialProvider: fromNodeProviderChain(),
});
```

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `bedrock` desde `@ai-sdk/amazon-bedrock`:

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
```

Si necesitas una configuración personalizada, puedes importar `createAmazonBedrock` desde `@ai-sdk/amazon-bedrock` y crear una instancia de proveedor con tus ajustes:

```ts
import { createAmazonBedrock } from '@ai-sdk/amazon-bedrock';

const bedrock = createAmazonBedrock({
  region: 'us-east-1',
  accessKeyId: 'xxxxxxxxx',
  secretAccessKey: 'xxxxxxxxx',
  sessionToken: 'xxxxxxxxx',
});
```

<Nota>
  Los ajustes de credenciales se reemplazan por los valores por defecto de las variables de entorno descritos
  a continuación. Estos pueden estar configurados por tu entorno serverless sin tu conocimiento,
  lo que puede provocar valores de credenciales combinados/ conflictivos y errores de proveedor alrededor de la autenticación fallida.
  Si estás experimentando problemas, asegúrate de especificar explícitamente todos los ajustes (incluso los `undefined`) para evitar cualquier valor por defecto.
</Nota>

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor de Amazon Bedrock:

- **region** _cadena_

  La región de AWS que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `AWS_REGION` por defecto.

- **accessKeyId** _cadena_

  La clave de acceso de AWS que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `AWS_ACCESS_KEY_ID` por defecto.

- **secretAccessKey** _cadena_

  La clave de acceso secreta de AWS que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `AWS_SECRET_ACCESS_KEY` por defecto.

- **sessionToken** _cadena_

  Opcional. El token de sesión de AWS que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `AWS_SESSION_TOKEN` por defecto.

- **credentialProvider** _() =&gt; Promise&lt;

#123; accessKeyId: string; secretAccessKey: string; sessionToken?: string; &#125;&gt;_

  Opcional. La cadena de proveedores de credenciales de AWS que deseas utilizar para las llamadas a la API.
  Utiliza las credenciales especificadas por defecto.

## Modelos de Lenguaje

Puedes crear modelos que llamen a la API de Bedrock utilizando la instancia del proveedor.
El primer argumento es el identificador del modelo, por ejemplo `meta.llama3-70b-instruct-v1:0`.

```ts
const model = bedrock('meta.llama3-70b-instruct-v1:0');
```

Los modelos de Amazon Bedrock también admiten algunas configuraciones específicas del modelo que no forman parte de los [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const model = bedrock('anthropic.claude-3-sonnet-20240229-v1:0', {
  additionalModelRequestFields: { top_k: 350 },
});
```

La documentación para configuraciones adicionales basadas en el modelo seleccionado se puede encontrar dentro de la [documentación de parámetros de inferencia de Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html).

Puedes utilizar modelos de lenguaje de Amazon Bedrock para generar texto con la función `generateText`:

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const { text } = await generateText({
  model: bedrock('meta.llama3-70b-instruct-v1:0'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Amazon Bedrock también se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

### Entradas de Archivos

<Nota tipo="advertencia">
  El proveedor Amazon Bedrock admite entradas de archivos en combinación con modelos específicos,
  por ejemplo, `anthropic.claude-3-haiku-20240307-v1:0`.
</Nota>

El proveedor Amazon Bedrock admite entradas de archivos, por ejemplo, archivos PDF.

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const result = await generateText({
  model: bedrock('anthropic.claude-3-haiku-20240307-v1:0'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Describa el PDF con detalle.' },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
});
```

### Guardrails

Puedes utilizar las opciones del proveedor `bedrock` para aprovechar [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/):

```ts
const result = await generateText({
  bedrock('anthropic.claude-3-sonnet-20240229-v1:0'),
  providerOptions: {
    bedrock: {
      guardrailConfig: {
        guardrailIdentifier: '1abcd2ef34gh',
        guardrailVersion: '1',
        trace: 'enabled' as const,
        streamProcessingMode: 'async',
      },
    },
  },
});
```

La información de seguimiento se devolverá en el metadato del proveedor si tienes el seguimiento habilitado.

```ts
if (result.providerMetadata?.bedrock.trace) {
  // ...
}
```

Consulte la [documentación de Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) para obtener más información.

### Puntos de Caché

<Nota>
  El caché de promt de Amazon Bedrock está actualmente en versión de prueba. Para solicitar acceso, visite la [página de caché de promt de Amazon Bedrock](https://aws.amazon.com/bedrock/prompt-caching/).
</Nota>

En mensajes, puede utilizar la propiedad `providerOptions` para establecer puntos de caché. Establezca la propiedad `bedrock` en el objeto `providerOptions` a `{ cachePoint: { type: 'default' } }` para crear un punto de caché.

La información sobre el uso del caché se devuelve en el objeto `providerMetadata`. Consulte los ejemplos a continuación.

<Nota>
  Los puntos de caché tienen límites y requisitos de token específicos para cada modelo. Por ejemplo, Claude 3.5 Sonnet v2 requiere al menos 1.024 tokens para un punto de caché y permite hasta 4 puntos de caché. Consulte la [documentación de caché de promt de Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) para obtener detalles sobre los modelos admitidos, regiones y límites.
</Nota>

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const analisisCibercultural =
  '... análisis literario de temas y conceptos ciberculturales ...';

const resultado = await generateText({
  modelo: bedrock('anthropic.claude-3-5-sonnet-20241022-v2:0'),
  mensajes: [
    {
      rol: 'sistema',
      contenido: `Usted es un experto en la literatura cibercultural de William Gibson y temas. Tiene acceso al siguiente análisis académico: ${analisisCibercultural}`,
      opcionesDeProveedor: {
        bedrock: { cachePoint: { type: 'default' } },
      },
    },
    {
      rol: 'usuario',
      contenido:
        '¿Cuáles son los temas ciberculturales clave que Gibson explora en Neuromancer?',
    },
  ],
});
```

```javascript
console.log(result.text);
console.log(result.providerMetadata?.bedrock?.usage);
// Muestra el uso de tokens de lectura/grabado en caché, por ejemplo:
// {
//   cacheReadInputTokens: 1337,
//   cacheWriteInputTokens: 42,
// }
```

Puntos de caché también funcionan con respuestas de flujo:

```typescript
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamText } from 'ai';

const analisisCyberpunko =
  '... análisis literario de temas y conceptos de cyberpunk ...';

const result = streamText({
  model: bedrock('anthropic.claude-3-5-sonnet-20241022-v2:0'),
  messages: [
    {
      role: 'asistente',
      content: [
        { type: 'texto', text: 'Eres un experto en literatura de cyberpunk.' },
        { type: 'texto', text: `Análisis académico: ${analisisCyberpunko}` },
      ],
      providerOptions: { bedrock: { puntoDeCaché: { tipo: 'default' } } },
    },
    {
      role: 'usuario',
      content:
        '¿Cómo explora Gibson la relación entre la humanidad y la tecnología?',
    },
  ],
});

for await (const parteDeTexto of result.textStream) {
  process.stdout.write(parteDeTexto);
}

console.log(
  'Uso de tokens de caché:',
  (await result.providerMetadata)?.bedrock?.usage,
);
// Muestra el uso de tokens de lectura/grabado en caché, por ejemplo:
// {
//   cacheReadInputTokens: 1337,
//   cacheWriteInputTokens: 42,
// }
```

## Razonamiento

Amazon Bedrock admite el soporte de razonamiento para el modelo `claude-3-7-sonnet-20250219`.

Puedes habilitarlo utilizando la opción de configuración `reasoning_config` y especificando un presupuesto de pensamiento en tokens (mínimo: `1024`, máximo: `64000`).

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const { text, reasoning, reasoningDetails } = await generateText({
  model: bedrock('us.anthropic.claude-3-7-sonnet-20250219-v1:0'),
  prompt: '¿Cuánta gente vivirá en el mundo en 2040?',
  providerOptions: {
    bedrock: {
      reasoningConfig: { type: 'enabled', budgetTokens: 1024 },
    },
  },
});

console.log(reasoning); // texto de razonamiento
console.log(reasoningDetails); // detalles del razonamiento, incluyendo el razonamiento redactado
console.log(text); // respuesta de texto
```

Consulte [SDK de IA UI: Chatbot](/docs/ai-sdk-ui/chatbot#razonamiento) para obtener más detalles sobre cómo integrar el razonamiento en tu chatbot.

### Capacidad del Modelo

### Resumen

| Modelo                                       | Entrada de imagen         | Generación de objetos   | Uso de herramienta          | Streaming de herramienta      |
| ------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `amazon.titan-tg1-large`                    | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `amazon.titan-text-express-v1`              | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `amazon.nova-micro-v1:0`                    | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `amazon.nova-lite-v1:0`                     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `amazon.nova-pro-v1:0`                      | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-4-sonnet-20250514-v1:0`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `anthropic.claude-4-opus-20250514-v1:0`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-7-sonnet-20250219-v1:0` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-5-sonnet-20241022-v2:0` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-5-sonnet-20240620-v1:0` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-5-haiku-20241022-v1:0`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `anthropic.claude-3-opus-20240229-v1:0`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-sonnet-20240229-v1:0`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-haiku-20240307-v1:0`    | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `anthropic.claude-v2:1`                     | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `cohere.command-r-v1:0`                     | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `cohere.command-r-plus-v1:0`                | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `deepseek.r1-v1:0`                          | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama2-13b-chat-v1`                   | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama2-70b-chat-v1`                   | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-8b-instruct-v1:0`              | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `meta.llama3-70b-instruct-v1:0`             | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-1-8b-instruct-v1:0`            | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-1-70b-instruct-v1:0`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-1-405b-instruct-v1:0`          | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-2-1b-instruct-v1:0`            | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-2-3b-instruct-v1:0`            | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta.llama3-2-11b-instruct-v1:0`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `meta.llama3-2-90b-instruct-v1:0`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `mistral.mistral-7b-instruct-v0:2`          | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `mistral.mixtral-8x7b-instruct-v0:1`        | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `mistral.mistral-large-2402-v1:0`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `mistral.mistral-small-2402-v1:0`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  La tabla anterior enumera modelos populares. Consulte los [docs de Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-supported-models-features.html)
  para obtener una lista completa de modelos disponibles. La tabla anterior enumera modelos populares. También puedes pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Incorporando Modelos

Puedes crear modelos que llamen a la API de Bedrock [Bedrock API](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
usando el método de fabricación `.embedding()`.

```ts
const modelo = bedrock.embedding('amazon.titan-embed-text-v1');
```

El modelo de incorporación de Bedrock Titan `amazon.titan-embed-text-v2:0` admite varias configuraciones adicionales.
Puedes pasarlas como un argumento de opciones:

```ts
const modelo = bedrock.embedding('amazon.titan-embed-text-v2:0', {
  dimensiones: 512 // opcional, número de dimensiones para la incorporación
  normalizar: true // opcional, normaliza las incorporaciones de salida
})
```

Las siguientes configuraciones opcionales están disponibles para los modelos de incorporación de Bedrock Titan:

- **dimensiones**: _número_

  El número de dimensiones que deberían tener las incorporaciones de salida. Los siguientes valores se aceptan: 1024 (por defecto), 512, 256.

- **normalizar** _boolean_

  Bandera que indica si se normalizan o no las incorporaciones de salida. Por defecto, es true.

### Capabilities del Modelo

| Modelo                          | Dimensiones por defecto | Dimensiones personalizadas   |
| ------------------------------ | ------------------ | ------------------- |
| `amazon.titan-embed-text-v1`   | 1536               | <Cross size={18} /> |
| `amazon.titan-embed-text-v2:0` | 1024               | <Check size={18} /> |

## Modelos de Imágenes

Puedes crear modelos que llamen a la API de Bedrock [API de Bedrock](https://docs.aws.amazon.com/nova/latest/userguide/image-generation.html)
usando el método de fábrica `.image()`.

Para obtener más información sobre el modelo de imagen de Amazon Nova Canvas, consulta la [Visión General de Nova Canvas](https://docs.aws.amazon.com/ai/responsible-ai/nova-canvas/overview.html).

<Nota>
  El modelo `amazon.nova-canvas-v1:0` está disponible en la región `us-east-1`.
</Nota>

```ts
const model = bedrock.image('amazon.nova-canvas-v1:0');
```

Puedes generar imágenes con la función `experimental_generateImage`:

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: bedrock.imageModel('amazon.nova-canvas-v1:0'),
  prompt: 'Un atardecer hermoso sobre un océano calmado',
  size: '512x512',
  seed: 42,
});
```

También puedes pasar el objeto `providerOptions` a la función `generateImage` para personalizar el comportamiento de la generación:

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: bedrock.imageModel('amazon.nova-canvas-v1:0'),
  prompt: 'Un atardecer hermoso sobre un océano calmado',
  size: '512x512',
  seed: 42,
  providerOptions: { bedrock: { quality: 'premium' } },
});
```

La documentación para ajustes adicionales se puede encontrar dentro de la [Guía del Usuario de Amazon Bedrock para Amazon Nova
Documentación](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-req-resp-structure.html).

### Configuración de Modelos de Imágenes

Al crear un modelo de imágenes, puedes personalizar el comportamiento de generación con configuraciones opcionales:

```ts
const model = bedrock.imageModel('amazon.nova-canvas-v1:0', {
  maxImagesPerCall: 1, // Número máximo de imágenes generadas por llamada a la API
});
```

- **maxImagesPerCall** _número_

  Sustituye el número máximo de imágenes generadas por llamada a la API. El valor por defecto puede variar según el modelo, con 5 como un valor común por defecto.

### Capacidad del Modelo

El modelo Amazon Nova Canvas admite tamaños personalizados con restricciones como sigue:

- Cada lado debe medir entre 320-4096 píxeles, inclusive.
- Cada lado debe ser divisible por 16.
- La relación de aspecto debe medir entre 1:4 y 4:1. Es decir, uno de los lados no puede ser más de 4 veces más largo que el otro lado.
- La cuenta total de píxeles debe ser menor que 4,194,304.

Para más información, consulta [Acceso y uso de la generación de imágenes](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-access.html).

| Modelo                     | Tamaños                                                                                                 |
| ------------------------- | ----------------------------------------------------------------------------------------------------- |
| `amazon.nova-canvas-v1:0` | Tamaños personalizados: 320-4096px por lado (debe ser divisible por 16), relación de aspecto 1:4 a 4:1, max 4.2M píxeles |

## Encabezados de respuesta

El proveedor de Amazon Bedrock devolverá los encabezados de respuesta asociados con las solicitudes de red realizadas a los servidores de Bedrock.

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const { text } = await generateText({
  model: bedrock('meta.llama3-70b-instruct-v1:0'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});

console.log(result.response.headers);
```

A continuación, se muestra un ejemplo de salida donde se puede ver el encabezado `x-amzn-requestid`. Esto puede ser útil para correlacionar las llamadas a la API de Bedrock con las solicitudes realizadas por el SDK de IA:

```js highlight="6"
{
  connection: 'keep-alive',
  'content-length': '2399',
  'content-type': 'application/json',
  date: 'Fri, 07 Feb 2025 04:28:30 GMT',
  'x-amzn-requestid': 'c9f3ace4-dd5d-49e5-9807-39aedfa47c8e'
}
```

Esta información también está disponible con `streamText`:

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamText } from 'ai';

const result = streamText({
  model: bedrock('meta.llama3-70b-instruct-v1:0'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
for await (const textPart of result.textStream) {
  process.stdout.write(textPart);
}
console.log('Encabezados de respuesta:', (await result.response).headers);
```

Con un ejemplo de salida como:

```js highlight="6"
{
  connection: 'keep-alive',
  'content-type': 'application/vnd.amazon.eventstream',
  date: 'vie, 07 feb 2025 04:33:37 GMT',
  'transfer-encoding': 'chunked',
  '

## Migrando a `@ai-sdk/amazon-bedrock` 2.x

El proveedor de Amazon Bedrock se reescribió en la versión 2.x para eliminar la dependencia del paquete `@aws-sdk/client-bedrock-runtime`.

El ajuste de proveedor `bedrockOptions` disponible anteriormente ha sido eliminado. Si estabas utilizando el objeto `bedrockOptions`, ahora debes utilizar los ajustes `region`, `accessKeyId`, `secretAccessKey` y `sessionToken` directamente en su lugar.

Ten en cuenta que es posible que debas establecer todos estos explícitamente, por ejemplo, incluso si no estás utilizando `sessionToken`, establecélo en `undefined`. Si estás ejecutando en un entorno serverless, es posible que haya variables de entorno predeterminadas establecidas por tu entorno contenedor que el proveedor de Amazon Bedrock luego capturará y podría conflictar con las que estás intentando utilizar.

---
titulo: Groq
descripción: Aprende a utilizar Groq.
---

# Proveedor de Groq

El [proveedor de Groq](https://groq.com/) contiene soporte para modelos de lenguaje para la API de Groq.

## Configuración

El proveedor de Groq está disponible a través del módulo `@ai-sdk/groq`.
Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/groq" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/groq" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/groq" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `groq` desde `@ai-sdk/groq`:

```ts
import { groq } from '@ai-sdk/groq';
```

Si necesitas una configuración personalizada, puedes importar `createGroq` desde `@ai-sdk/groq`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createGroq } from '@ai-sdk/groq';

const groq = createGroq({
  // ajustes personalizados
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Groq:

- **baseURL** _cadena_

  Utiliza una URL diferente como prefijo para las llamadas a API, por ejemplo, para utilizar servidores de proxy.
  El prefijo por defecto es `https://api.groq.com/openai/v1`.

- **apiKey** _cadena_

  Llave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, utiliza la variable de entorno `GROQ_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

## Modelos de Lenguaje

Puedes crear [modelos Groq](https://console.groq.com/docs/models) utilizando una instancia de proveedor.
El primer argumento es el ID del modelo, por ejemplo, `gemma2-9b-it`.

```ts
const model = groq('gemma2-9b-it');
```

### Modelos de Razón

Groq ofrece varios modelos de razón como `qwen-qwq-32b` y `deepseek-r1-distill-llama-70b`.
Puedes configurar cómo se expone la razón en el texto generado utilizando la opción `reasoningFormat`.
Soporta las opciones `parsed`, `hidden` y `raw`.

```ts
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const result = await generateText({
  model: groq('qwen-qwq-32b'),
  providerOptions: {
    groq: { reasoningFormat: 'parsed' },
  },
  prompt: '¿Cuántas "r"s hay en la palabra "fresa"?',
});
```

<Nota> Solo los modelos de razón de Groq admiten la opción `reasoningFormat`.</Nota>

### Ejemplo

Puedes utilizar los modelos de lenguaje Groq para generar texto con la función `generateText`:

```ts
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const { texto } = await generateText({
  model: groq('gemma2-9b-it'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

## Capabilidades del Modelo

| Modelo                                       | Entrada de Imagen         | Generación de Objetos   | Uso de Herramientas          | Streaming de Herramientas      |
| ------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `meta-llama/llama-4-scout-17b-16e-instruct` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemma2-9b-it`                              | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama-3.3-70b-versatile`                   | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama-3.1-8b-instant`                      | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama-guard-3-8b`                          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `llama3-70b-8192`                           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama3-8b-8192`                            | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mixtral-8x7b-32768`                        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `qwen-qwq-32b`                              | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistral-saba-24b`                          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `qwen-2.5-32b`                              | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `deepseek-r1-distill-qwen-32b`              | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `deepseek-r1-distill-llama-70b`             | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Nota>
  La tabla anterior enumera modelos populares. Consulte la documentación de Groq en [https://console.groq.com/docs/models](https://console.groq.com/docs/models) para obtener una lista completa de modelos disponibles. La tabla anterior enumera modelos populares. También puedes pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de Groq](https://console.groq.com/docs/speech-to-text)
utilizando el método de fábrica `.transcription()`.

El primer argumento es el ID del modelo, por ejemplo `whisper-large-v3`.

```ts
const model = groq.transcription('whisper-large-v3');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo `en`) mejorará la precisión y la latencia.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { groq } from '@ai-sdk/groq';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: groq.transcription('whisper-large-v3'),
  audio: await readFile('audio.mp3'),
  providerOptions: { groq: { language: 'en' } },
});
```

Las siguientes opciones del proveedor están disponibles:

- **timestampGranularities** _string[]_
  La granularidad de los tiempos de transcripción.
  Por defecto es `['segment']`.
  Los valores posibles son `['word']`, `['segment']` y `['word', 'segment']`.
  Nota: No hay latencia adicional para los tiempos de segmento, pero generar tiempos de palabra incurre en latencia adicional.

- **language** _string_
  El idioma del audio de entrada. Suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo 'en') mejorará la precisión y la latencia.
  Opcional.

- **prompt** _string_
  Un texto opcional para guiar el estilo del modelo o continuar un segmento de audio previo. El prompt debe coincidir con el idioma del audio.
  Opcional.

- **temperatura** _número_
  La temperatura de muestreo, entre 0 y 1. Valores más altos como 0,8 harán que el resultado sea más aleatorio, mientras que valores más bajos como 0,2 harán que sea más enfocado y determinístico. Si se establece en 0, el modelo utilizará la probabilidad logarítmica para aumentar automáticamente la temperatura hasta que ciertos umbrales se alcancen.
  Se establece por defecto en 0.
  Opcional.

### Capabilities del Modelo

| Modelo                        | Transcripción       | Duración            | Segmentos            | Idioma            |
| ---------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper-large-v3`           | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `whisper-large-v3-turbo`     | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `distil-whisper-large-v3-en` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

---
titulo: Fal
descripcion: Aprende a utilizar modelos Fal AI con la SDK de AI.
---

# Proveedor Fal

[Fal AI](https://fal.ai/) proporciona una plataforma de medios generativos para desarrolladores con capacidades de inferencia de iluminación. Su plataforma ofrece rendimiento optimizado para ejecutar modelos de difusión, con velocidades hasta 4x más rápidas que las alternativas.

## Configuración

El proveedor Fal está disponible a través del módulo `@ai-sdk/fal`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/fal" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/fal" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/fal" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `fal` desde `@ai-sdk/fal`:

```ts
import { fal } from '@ai-sdk/fal';
```

Si necesitas una configuración personalizada, puedes importar `createFal` y crear una instancia de proveedor con tus ajustes:

```ts
import { createFal } from '@ai-sdk/fal';

const fal = createFal({
  apiKey: 'tu-clave-api', // opcional, utiliza la variable de entorno FAL_API_KEY por defecto, cayendo en FAL_KEY
  baseURL: 'url-customizada', // opcional
  headers: {
    /* encabezados personalizados */
  }, // opcional
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Fal:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para las llamadas a la API, por ejemplo, para utilizar servidores proxy.
  El prefijo predeterminado es `https://fal.run`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto utiliza la variable de entorno `FAL_API_KEY`, cayendo en `FAL_KEY`.

- **headers** _Registro&lt;cadena,cadena&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Imágenes

Puedes crear modelos de imágenes Fal utilizando el método de fábrica `.image()`.
Para más información sobre la generación de imágenes con el SDK de IA, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

### Uso Básico

```ts
import { fal } from '@ai-sdk/fal';
import { experimental_generateImage as generateImage } from 'ai';
import fs from 'fs';

const { image } = await generateImage({
  model: fal.image('fal-ai/fast-sdxl'),
  prompt: 'Un paisaje montañoso sereno al atardecer',
});

const filename = `image-${Date.now()}.png`;
fs.writeFileSync(filename, image.uint8Array);
console.log(`La imagen se ha guardado en ${filename}`);
```

### Capacidad del Modelo

Fal ofrece muchos modelos optimizados para diferentes casos de uso. A continuación, se presentan algunos ejemplos populares. Para obtener una lista completa de modelos, consulte la [documentación de Fal AI](https://fal.ai/models).

| Modelo                               | Descripción                                                                                                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fal-ai/fast-sdxl`                  | Modelo SDXL de alta velocidad optimizado para inferencia rápida con hasta 4x velocidades más altas                                                                               |
| `fal-ai/flux-pro/kontext`           | FLUX.1 Kontext [pro] maneja tanto imágenes de texto como de referencia como entradas, permitiendo ediciones y transformaciones de escenas complejas de manera fluida y local |
| `fal-ai/flux-pro/kontext/max`       | FLUX.1 Kontext [max] con una gran mejora en la adherencia a las solicitudes y la generación de tipografía, cumpliendo con la consistencia premium para la edición sin comprometer la velocidad |
| `fal-ai/flux-lora`                  | Punto final rápido para el modelo FLUX.1 [dev] con soporte de LoRA, que permite la generación de imágenes de alta calidad y rápida utilizando adaptaciones pre-entrenadas de LoRA.        |

| `fal-ai/flux-pro/v1.1-ultra`        | Generación de imágenes de alta gama con resolución hasta 2K y realismo fotográfico mejorado                                                                        |
| `fal-ai/ideogram/v2`                | Especializado en carteles y logotipos de alta calidad con manejo excepcional de tipografía                                                                            |
| `fal-ai/recraft-v3`                 | SOTA en la generación de imágenes con arte vectorial y capacidades de estilo de marca                                                                                         |
| `fal-ai/stable-diffusion-3.5-large` | Modelo MMDiT avanzado con tipografía mejorada y comprensión de solicitudes complejas                                                                                |

| `fal-ai/hyper-sdxl`                 | Variante de SDXL optimizada para rendimiento con capacidades creativas mejoradas                                                                                       |

Los modelos de Fal admiten las siguientes relaciones de aspecto:

- 1:1 (HD cuadrado)
- 16:9 (paisaje)
- 9:16 (retoro)
- 4:3 (paisaje)
- 3:4 (retoro)
- 16:10 (1280x800)
- 10:16 (800x1280)
- 21:9 (2560x1080)
- 9:21 (1080x2560)

Características clave de los modelos de Fal incluyen:

- Velocidades de inferencia hasta 4 veces más rápido en comparación con alternativas
- Optimizado por el Fal Inference Engine™
- Soporte para infraestructura en tiempo real
- Escalado rentable con precios por uso
- Capacidad de entrenamiento LoRA para personalización de modelos

#### Modificar Imagen

Transformar imágenes existentes utilizando promotos de texto.

```ts
// Ejemplo: Modificar imagen existente
await generateImage({
  model: fal.image('fal-ai/flux-pro/kontext'),
  prompt: 'Coloca un donut junto al harina.',
  providerOptions: {
    fal: {
      image_url:
        'https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png',
    },
  },
});
```

### Características Avanzadas

La plataforma de Fal ofrece varias capacidades avanzadas:

- **Inferencia de Modelos Privados**: Ejecutar tus propios modelos de transformador de difusión con una inferencia hasta 50% más rápida
- **Entrenamiento de LoRA**: Entrenar y personalizar modelos en menos de 5 minutos
- **Infraestructura en Tiempo Real**: Habilitar nuevas experiencias de usuario con tiempos de inferencia rápidos
- **Arquitectura Escalable**: Escalar a miles de GPUs cuando sea necesario

Para obtener más detalles sobre las capacidades y características de Fal, visita la [documentación de Fal AI](https://fal.ai/docs).

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de Fal](https://docs.fal.ai/guides/convert-speech-to-text)
utilizando el método de fábrica `.transcription()`.

El primer argumento es el ID del modelo sin el prefijo `fal-ai/` por ejemplo `wizper`.

```ts
const model = fal.transcription('wizper');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar la opción `batchSize` aumentará el número de trozos de audio procesados en paralelo.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { fal } from '@ai-sdk/fal';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: fal.transcription('wizper'),
  audio: await readFile('audio.mp3'),
  providerOptions: { fal: { batchSize: 10 } },
});
```

Las siguientes opciones del proveedor están disponibles:

- **lenguaje** _cadena_
  Idioma del archivo de audio. Si se establece en null, el idioma se detectará automáticamente.
  Acepta códigos de idioma ISO como 'en', 'fr', 'zh', etc.
  Opcional.

- **diarizar** _booleano_
  Si se diariza el archivo de audio (identificar a diferentes hablantes).
  Por defecto, true.
  Opcional.

- **nivelDeChunk** _cadena_
  Nivel de los trozos a devolver. O 'segmento' o 'palabra'.
  Valor por defecto: "palabra"
  Opcional.

- **versión** _cadena_
  Versión del modelo a utilizar. Todos los modelos son variantes grandes de Whisper.
  Valor por defecto: "3"
  Opcional.

- **tamanoDeLote** _número_
  Tamaño del lote para el procesamiento.
  Valor por defecto: 64
  Opcional.

- **numHablantes** _número_
  Número de hablantes en el archivo de audio. Si no se proporciona, el número de hablantes se detectará automáticamente.
  Opcional.

### Capabilidades del Modelo

| Modelo     | Transcripción       | Duración            | Segmentos            | Idioma            |
| --------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `wizper`  | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titulo: AssemblyAI
descripción: Aprende a utilizar el proveedor de AssemblyAI para el SDK de IA.
---

# Proveedor de AssemblyAI

El [proveedor de AssemblyAI](https://assemblyai.com/) contiene soporte para modelos de lenguaje del API de transcripción de AssemblyAI.

## Configuración

El proveedor de AssemblyAI está disponible en el módulo `@ai-sdk/assemblyai`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/assemblyai" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/assemblyai" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/assemblyai" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `assemblyai` desde `@ai-sdk/assemblyai`:

```ts
import { assemblyai } from '@ai-sdk/assemblyai';
```

Si necesitas una configuración personalizada, puedes importar `createAssemblyAI` desde `@ai-sdk/assemblyai` y crear una instancia de proveedor con tus ajustes:

```ts
import { createAssemblyAI } from '@ai-sdk/assemblyai';

const assemblyai = createAssemblyAI({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor AssemblyAI:

- **apiKey** _cadena_

  La clave API que se envía utilizando el encabezado `Authorization`.
  Por defecto, es la variable de entorno `ASSEMBLYAI_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, es la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Transcripción

Puedes crear modelos que utilicen la API de transcripción de [AssemblyAI](https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file/typescript)
mediante el método de fábrica `.transcription()`.

El primer argumento es el id del modelo, por ejemplo `best`.

```ts
const model = assemblyai.transcription('best');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar la opción `contentSafety` habilitará la filtración de contenido seguro.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { assemblyai } from '@ai-sdk/assemblyai';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: assemblyai.transcription('best'),
  audio: await readFile('audio.mp3'),
  providerOptions: { assemblyai: { contentSafety: true } },
});
```

Las siguientes opciones de proveedor están disponibles:

- **audioEndAt** _number_

  Tiempo final del audio en milisegundos.
  Opcional.

- **audioStartFrom** _number_

  Tiempo inicial del audio en milisegundos.
  Opcional.

- **autoChapters** _boolean_

  Si se deben generar automáticamente capítulos para la transcripción.
  Opcional.

- **autoHighlights** _boolean_

  Si se deben generar automáticamente resaltados para la transcripción.
  Opcional.

- **boostParam** _enum_

  Parámetro de aumento para la transcripción.
  Valores permitidos: `'low'`, `'default'`, `'high'`.
  Opcional.

- **contentSafety** _boolean_

  Si se debe habilitar la filtración de contenido seguro.
  Opcional.

- **contentSafetyConfidence** _number_

  Umbral de confianza para la filtración de contenido seguro (25-100).
  Opcional.

- **customSpelling** _array of objetos_

  Reglas de ortografía personalizadas para la transcripción.
  Cada objeto tiene propiedades `from` (array de cadenas) y `to` (cadena).
  Opcional.

- **disfluencies** _boolean_

¿Incluir disfluencias (um, uh, etc.) en la transcripción.
  Opcional.

- **entityDetection** _boolean_

  Si detectar entidades en la transcripción.
  Opcional.

- **filterProfanity** _boolean_

  Si filtrar lenguaje soez en la transcripción.
  Opcional.

- **formatText** _boolean_

  Si formatear el texto en la transcripción.
  Opcional.

- **iabCategories** _boolean_

  Si incluir categorías de IAB en la transcripción.
  Opcional.

- **languageCode** _string_

  Código de idioma para el audio.
  Soporta numerosos códigos de idioma ISO-639-1 y ISO-639-3.
  Opcional.

- **languageConfidenceThreshold** _number_

  Umbral de confianza para la detección de idioma.
  Opcional.

- **languageDetection** _boolean_

  Si habilitar la detección de idioma.
  Opcional.

- **multichannel** _boolean_

  Si procesar múltiples canales de audio por separado.
  Opcional.

- **punctuate** _boolean_

  Si agregar puntuación a la transcripción.
  Opcional.

- **redactPii** _boolean_

  Si suprimir información personalmente identificable.
  Opcional.

- **redactPiiAudio** _boolean_

  Si suprimir PII en el archivo de audio.
  Opcional.

- **redactPiiAudioQuality** _enum_

  Calidad del archivo de audio suprimido.
  Valores permitidos: `'mp3'`, `'wav'`.
  Opcional.

- **redactPiiPolicies** _array of enums_

  Políticas para la supresión de PII, especificando qué tipos de información suprimir.
  Soporta numerosos tipos como `'nombre_de_persona'`, `'número_de_telefono'`, etc.
  Opcional.

- **redactPiiSub** _enum_

  Método de sustitución para la PII suprimida.
  Valores permitidos: `'nombre_de_entidad'`, `'hash'`.
  Opcional.

- **sentimentAnalysis** _boolean_

  Si realizar análisis de sentimiento en la transcripción.
  Opcional.

- **speakerLabels** _boolean_

¿Etiquetar a diferentes hablantes en la transcripción.
  Opcional.

- **speakersExpected** _número_

  Número esperado de hablantes en el audio.
  Opcional.

- **speechThreshold** _número_

  Umbral para la detección de habla (0-1).
  Opcional.

- **summarization** _boolean_

  Si se debe generar un resumen de la transcripción.
  Opcional.

- **summaryModel** _enum_

  Modelo a utilizar para la resumen.
  Valores permitidos: `'informative'`, `'conversational'`, `'catchy'`.
  Opcional.

- **summaryType** _enum_

  Tipo de resumen a generar.
  Valores permitidos: `'bullets'`, `'bullets_verbose'`, `'gist'`, `'headline'`, `'paragraph'`.
  Opcional.

- **topics** _array de cadenas_

  Lista de temas a detectar en la transcripción.
  Opcional.

- **webhookAuthHeaderName** _cadena_

  Nombre del encabezado de autenticación para solicitudes de webhook.
  Opcional.

- **webhookAuthHeaderValue** _cadena_

  Valor del encabezado de autenticación para solicitudes de webhook.
  Opcional.

- **webhookUrl** _cadena_

  URL a la que enviar notificaciones de webhook.
  Opcional.

- **wordBoost** _array de cadenas_

  Lista de palabras a aumentar en la transcripción.
  Opcional.

### Capabilidades del Modelo

| Modelo  | Transcripción       | Duración            | Segmentos            | Idioma            |
| ------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `best` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `nano` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titulo: DeepInfra
descripcion: Aprende a utilizar los modelos de DeepInfra con la SDK de IA.
---

# Proveedor DeepInfra

El [proveedor DeepInfra](https://deepinfra.com) contiene soporte para modelos de estado de la arte a través de la API de DeepInfra, incluyendo Llama 3, Mixtral, Qwen y muchos otros modelos de código abierto populares.

## Configuración

El proveedor DeepInfra está disponible a través del módulo `@ai-sdk/deepinfra`. Puedes instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/deepinfra" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/deepinfra" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/deepinfra" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor por defecto `deepinfra` desde `@ai-sdk/deepinfra`:

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
```

Si necesitas una configuración personalizada, puedes importar `createDeepInfra` desde `@ai-sdk/deepinfra` y crear una instancia de proveedor con tus ajustes:

```ts
import { createDeepInfra } from '@ai-sdk/deepinfra';

const deepinfra = createDeepInfra({
  apiKey: process.env.DEEPINFRA_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor de DeepInfra:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para llamadas a la API, por ejemplo, para utilizar servidores de proxy.
  El prefijo predeterminado es `https://api.deepinfra.com/v1/openai`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`. Por defecto se utiliza la variable de entorno `DEEPINFRA_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch) personalizada.
  Por defecto se utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para pruebas, por ejemplo.

## Modelos de Lenguaje

Puedes crear modelos de lenguaje utilizando una instancia de proveedor. El primer argumento es el ID del modelo, por ejemplo:

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
import { generateText } from 'ai';

const { text } = await generateText({
  model: deepinfra('meta-llama/Meta-Llama-3.1-70B-Instruct'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de DeepInfra también se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

## Capabilidades del Modelo

| Modelo                                               | Entrada de Imagen         | Generación de Objetos   | Uso de Herramienta          | Transmisión de Herramienta      |
| --------------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct`         | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo`           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Llama-3.3-70B-Instruct`                 | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Meta-Llama-3.1-405B-Instruct`           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`      | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `meta-llama/Meta-Llama-3.1-70B-Instruct`            | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`       | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `meta-llama/Meta-Llama-3.1-8B-Instruct`             | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Llama-3.2-11B-Vision-Instruct`          | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Llama-3.2-90B-Vision-Instruct`          | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `mistralai/Mixtral-8x7B-Instruct-v0.1`              | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `deepseek-ai/DeepSeek-V3`                           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `deepseek-ai/DeepSeek-R1`                           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`         | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `deepseek-ai/DeepSeek-R1-Turbo`                     | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `nvidia/Llama-3.1-Nemotron-70B-Instruct`            | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `Qwen/Qwen2-7B-Instruct`                            | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `Qwen/Qwen2.5-72B-Instruct`                         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `Qwen/Qwen2.5-Coder-32B-Instruct`                   | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `Qwen/QwQ-32B-Preview`                              | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `google/codegemma-7b-it`                            | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `google/gemma-2-9b-it`                              | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `microsoft/WizardLM-2-8x22B`                        | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  La tabla anterior enumera modelos populares. Consulte los [documentos de DeepInfra](https://deepinfra.com) para obtener una lista completa de modelos disponibles. También puede pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Modelos de Imágenes

Puedes crear modelos de imágenes de DeepInfra utilizando el método de fábrica `.image()`.
Para más información sobre la generación de imágenes con el SDK de AI, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: deepinfra.image('stabilityai/sd3.5'),
  prompt: 'Una ciudad futurista al atardecer',
  aspectRatio: '16:9',
});
```

<Nota>
  El soporte de modelos para los parámetros `size` y `aspectRatio` varía por modelo. Por favor,
  revisa la documentación individual del modelo en la página de modelos de [DeepInfra](https://deepinfra.com/models/text-to-image) para opciones admitidas y parámetros adicionales.
</Nota>

### Opciones específicas del modelo

Puedes pasar parámetros específicos del modelo utilizando el campo `providerOptions.deepinfra`:

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: deepinfra.image('stabilityai/sd3.5'),
  prompt: 'Una ciudad futurista al atardecer',
  aspectRatio: '16:9',
  providerOptions: {
    deepinfra: {
      num_inference_steps: 30, // Controla el número de pasos de denoising (1-50)
    },
  },
});
```

### Capacidad del Modelo

Para modelos que admiten relaciones de aspecto, las siguientes relaciones de aspecto suelen ser admitidas:
`1:1 (por defecto), 16:9, 1:9, 3:2, 2:3, 4:5, 5:4, 9:16, 9:21`

Para modelos que admiten parámetros de tamaño, las dimensiones deben ser típicamente:

- Multiplos de 32
- Ancho y alto entre 256 y 1440 píxeles
- El tamaño por defecto es 1024x1024

| Modelo                              | Especificación de Dimensiones | Notas                                                    |
| ---------------------------------- | ------------------------ | -------------------------------------------------------- |
| `stabilityai/sd3.5`                | Relación de Aspecto             | Modelo base de alta calidad, 8B parámetros                |
| `black-forest-labs/FLUX-1.1-pro`   | Tamaño                     | Modelo de estado del arte más reciente con seguimiento de solicitudes superior |
| `black-forest-labs/FLUX-1-schnell` | Tamaño                     | Generación rápida en 1-4 pasos                             |
| `black-forest-labs/FLUX-1-dev`     | Tamaño                     | Optimizado para precisión anatómica                        |
| `black-forest-labs/FLUX-pro`       | Tamaño                     | Modelo de referencia de Flux                                 |

| `stabilityai/sd3.5-medium`         | Relación de aspecto       | Modelo con parámetros balanceados de 2.5B                |
| `stabilityai/sdxl-turbo`           | Relación de aspecto       | Optimizado para la generación rápida                   

Para obtener más detalles y información de precios, consulte la [página de modelos de texto-a-imagen de DeepInfra](https://deepinfra.com/models/text-to-image).

---
titulo: Deepgram
descripción: Aprenda a usar el proveedor Deepgram para el SDK de Inteligencia Artificial.
---

# Proveedor de Deepgram

El [proveedor de Deepgram](https://deepgram.com/) contiene soporte para modelos de lenguaje para la API de transcripción de Deepgram.

## Configuración

El proveedor de Deepgram está disponible en el módulo `@ai-sdk/deepgram`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/deepgram" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/deepgram" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/deepgram" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `deepgram` desde `@ai-sdk/deepgram`:

```ts
import { deepgram } from '@ai-sdk/deepgram';
```

Si necesitas una configuración personalizada, puedes importar `createDeepgram` desde `@ai-sdk/deepgram` y crear una instancia de proveedor con tus ajustes:

```ts
import { createDeepgram } from '@ai-sdk/deepgram';

const deepgram = createDeepgram({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Deepgram:

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, se utiliza la variable de entorno `DEEPGRAM_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, se utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de Deepgram](https://developers.deepgram.com/docs/pre-recorded-audio)
usando el método de fábrica `.transcription()`.

El primer argumento es el ID del modelo, por ejemplo, `nova-3`.

```ts
const model = deepgram.transcription('nova-3');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrando la opción `summarize` habilitará resúmenes para secciones de contenido.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { deepgram } from '@ai-sdk/deepgram';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: deepgram.transcription('nova-3'),
  audio: await readFile('audio.mp3'),
  providerOptions: { deepgram: { summarize: true } },
});
```

Las siguientes opciones del proveedor están disponibles:

- **idioma** _cadena_

  Código de idioma para el audio.
  Soporta numerosos códigos de idioma ISO-639-1 y ISO-639-3.
  Opcional.

- **formatoInteligente** _boolean_

  Si se debe aplicar formato inteligente a la transcripción.
  Opcional.

- **puntuar** _boolean_

  Si se debe agregar puntuación a la transcripción.
  Opcional.

- **parrafos** _boolean_

  Si se debe formatear la transcripción en párrafos.
  Opcional.

- **resumir** _enum | boolean_

  Si se debe generar un resumen de la transcripción.
  Valores permitidos: `'v2'`, `false`.
  Opcional.

- **temas** _boolean_

  Si se deben detectar temas en la transcripción.
  Opcional.

- **intenciones** _boolean_

  Si se deben detectar intenciones en la transcripción.
  Opcional.

- **sentimiento** _boolean_

  Si se debe realizar análisis de sentimiento en la transcripción.
  Opcional.

- **detectarEntidades** _boolean_

  Si se deben detectar entidades en la transcripción.
  Opcional.

- **redact** _cadena | array de cadenas_

  Especifica qué contenido eliminar de la transcripción.
  Opcional.

- **replace** _cadena_

  Cadena de reemplazo para el contenido eliminado.
  Opcional.

- **search** _cadena_

  Término de búsqueda para encontrar en la transcripción.
  Opcional.

- **keyterm** _cadena_

  Términos clave para identificar en la transcripción.
  Opcional.

- **diarize** _boolean_

  Si identificar a diferentes hablantes en la transcripción.
  Por defecto `true`.
  Opcional.

- **utterances** _boolean_

  Si segmentar la transcripción en oraciones.
  Opcional.

- **uttSplit** _número_

  Umbral para dividir oraciones.
  Opcional.

- **fillerWords** _boolean_

  Si incluir palabras de llenado (um, uh, etc.) en la transcripción.
  Opcional.

### Capabilidades del Modelo

| Modelo                                                                                              | Transcripción       | Duración            | Segmentos            | Idioma            |
| -------------------------------------------------------------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `nova-3` (+ [variantes](https://developers.deepgram.com/docs/models-lenguajes-overview#nova-3))     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `nova-2` (+ [variantes](https://developers.deepgram.com/docs/models-lenguajes-overview#nova-2))     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `nova` (+ [variantes](https://developers.deepgram.com/docs/models-lenguajes-overview#nova))         | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `mejorado` (+ [variantes](https://developers.deepgram.com/docs/models-lenguajes-overview#mejorado)) | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `base` (+ [variantes](https://developers.deepgram.com/docs/models-lenguajes-overview

# base))         | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

---
titulo: Gladia
descripcion: Aprende a utilizar el proveedor Gladia para la SDK de IA.
---

# Proveedor Gladia

El [Gladia](https://gladia.io/) provee soporte para modelos de lenguaje en la API de transcripción de Gladia.

## Configuración

El proveedor Gladia está disponible en el módulo `@ai-sdk/gladia`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/gladia" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/gladia" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/gladia" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor por defecto `gladia` desde `@ai-sdk/gladia`:

```ts
import { gladia } from '@ai-sdk/gladia';
```

Si necesitas una configuración personalizada, puedes importar `createGladia` desde `@ai-sdk/gladia` y crear una instancia de proveedor con tus ajustes:

```ts
import { createGladia } from '@ai-sdk/gladia';

const gladia = createGladia({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor Gladia:

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto es la variable de entorno `DEEPGRAM_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto es la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de Gladia](https://docs.gladia.io/chapters/pre-recorded-stt/getting-started)
utilizando el método de fábrica `.transcription()`.

```ts
const model = gladia.transcription();
```

También puedes pasar opciones adicionales específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrando la opción `summarize` habilitará resúmenes para secciones de contenido.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { gladia } from '@ai-sdk/gladia';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: gladia.transcription(),
  audio: await readFile('audio.mp3'),
  providerOptions: { gladia: { summarize: true } },
});
```

<Nota>
  Gladia no tiene varios modelos, por lo que puedes omitir el parámetro de identificador de modelo estándar.
</Nota>

Las siguientes opciones de proveedor están disponibles:

- **contextPrompt** _cadena_

  Contexto para alimentar el modelo de transcripción con para una posible mejor precisión.
  Opcional.

- **customVocabulary** _boolean | any[]_

  Vocabulario personalizado para mejorar la precisión de la transcripción.
  Opcional.

- **customVocabularyConfig** _objeto_

  Configuración para el vocabulario personalizado.
  Opcional.

  - **vocabulary** _Array&lt;cadena | { value: cadena, intensity?: número, pronunciations?: cadena[], language?: cadena }&gt;_
  - **defaultIntensity** _número_

- **detectLanguage** _boolean_

  Si se debe detectar automáticamente el idioma.
  Opcional.

- **enableCodeSwitching** _boolean_

  Habilitar el cambio de código para audio multilingüe.
  Opcional.

- **codeSwitchingConfig** _objeto_

  Configuración para el cambio de código.
  Opcional.

  - **languages** _cadena[]_

- **language** _cadena_

  Especificar el idioma del audio.
  Opcional.

- **callback** _boolean_

Habilite la llamada a función cuando la transcripción esté completa.
  Opcional.

- **callbackConfig** _object_

  Configuración para la llamada a función.
  Opcional.

  - **url** _string_
  - **method** _'POST' | 'PUT'_

- **subtitles** _boolean_

  Generar subtítulos desde la transcripción.
  Opcional.

- **subtitlesConfig** _object_

  Configuración para los subtítulos.
  Opcional.

  - **formats** _Array&lt;'srt' | 'vtt'&gt;_
  - **minimumDuration** _number_
  - **maximumDuration** _number_
  - **maximumCharactersPerRow** _number_
  - **maximumRowsPerCaption** _number_
  - **style** _'default' | 'compliance'_

- **diarization** _boolean_

  Habilitar la diarización de hablantes.
  Predeterminado a `true`.
  Opcional.

- **diarizationConfig** _object_

  Configuración para la diarización.
  Opcional.

  - **numberOfSpeakers** _number_
  - **minSpeakers** _number_
  - **maxSpeakers** _number_
  - **enhanced** _boolean_

- **translation** _boolean_

  Habilitar la traducción de la transcripción.
  Opcional.

- **translationConfig** _object_

  Configuración para la traducción.
  Opcional.

  - **targetLanguages** _string[]_
  - **model** _'base' | 'enhanced'_
  - **matchOriginalUtterances** _boolean_

- **summarization** _boolean_

  Habilitar la resumen de la transcripción.
  Opcional.

- **summarizationConfig** _object_

  Configuración para la resumen.
  Opcional.

  - **type** _'general' | 'bullet_points' | 'concise'_

- **moderation** _boolean_

  Habilitar la moderación de contenido.
  Opcional.

- **namedEntityRecognition** _boolean_

  Habilitar la reconocimiento de entidades

- **nameConsistencia** _boolean_

  Habilitar la consistencia de nombres en la transcripción.
  Opcional.

- **palabrasPersonalizadas** _boolean_

  Habilitar palabras personalizadas.
  Opcional.

- **palabrasPersonalizadasConfig** _object_

  Configuración para palabras personalizadas.
  Opcional.

  - **diccionarioDePalabras** _Registro&lt;string, string[]&gt;_

- **extracciónDeDatosEstructurados** _boolean_

  Habilitar la extracción de datos estructurados.
  Opcional.

- **extracciónDeDatosEstructuradosConfig** _object_

  Configuración para la extracción de datos estructurados.
  Opcional.

  - **clases** _string[]_

- **análisisDeSentimiento** _boolean_

  Habilitar el análisis de sentimiento.
  Opcional.

- **audioParaLlm** _boolean_

  Habilitar el procesamiento de audio para LLM.
  Opcional.

- **audioParaLlmConfig** _object_

  Configuración para el procesamiento de audio para LLM.
  Opcional.

  - **prompts** _string[]_

- **metadatosPersonalizados** _Registro&lt;string, any&gt;_

  Metadatos personalizados para incluir con la solicitud.
  Opcional.

- **oraciones** _boolean_

  Habilitar la detección de oraciones

### Capabilidades del Modelo

| Modelo     | Transcripción       | Duración            | Segmentos            | Idioma            |
| --------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `Default` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titulo: LMNT
descripcion: Aprende a usar el proveedor LMNT para el SDK de IA.
---

# Proveedor LMNT

El [LMNT](https://lmnt.com/) provee soporte para modelos de lenguaje a través de la API de transcripción de LMNT.

## Configuración

El proveedor LMNT está disponible en el módulo `@ai-sdk/lmnt`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/lmnt" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/lmnt" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/lmnt" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia predeterminada del proveedor `lmnt` desde `@ai-sdk/lmnt`:

```ts
import { lmnt } from '@ai-sdk/lmnt';
```

Si necesitas una configuración personalizada, puedes importar `createLMNT` desde `@ai-sdk/lmnt` y crear una instancia del proveedor con tus ajustes:

```ts
import { createLMNT } from '@ai-sdk/lmnt';

const lmnt = createLMNT({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor LMNT:

- **apiKey** _cadena_

  Clave API que se envía utilizando el encabezado `Authorization`.
  Por defecto, es la variable de entorno `LMNT_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, es la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Habla

Puedes crear modelos que llamen a la API de habla de [LMNT](https://docs.lmnt.com/api-reference/speech/synthesize-speech-bytes) utilizando el método de fábrica `.speech()`.

El primer argumento es el identificador del modelo, por ejemplo `aurora`.

```ts
const modelo = lmnt.speech('aurora');
```

También puedes pasar opciones adicionales específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar una voz para utilizar en el audio generado.

```ts highlight="6"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { lmnt } from '@ai-sdk/lmnt';

const resultado = await generateSpeech({
  modelo: lmnt.speech('aurora'),
  texto: 'Hola, mundo!',
  providerOptions: { lmnt: { idioma: 'en' } },
});
```

### Opciones del Proveedor

El proveedor LMNT acepta las siguientes opciones:

- **modelo** _'aurora' | 'blizzard'_

  El modelo LMNT a utilizar. Por defecto, es `'aurora'`.

- **idioma** _'auto' | 'en' | 'es' | 'pt' | 'fr' | 'de' | 'zh' | 'ko' | 'hi' | 'ja' | 'ru' | 'it' | 'tr'_

  El idioma a utilizar para la síntesis de habla. Por defecto, es `'auto'`.

- **formato** _'aac' | 'mp3' | 'mulaw' | 'raw' | 'wav'_

  El formato de audio a devolver. Por defecto, es `'mp3'`.

- **sampleRate** _número_

  La frecuencia de muestreo del audio en Hz. Por defecto, es `24000`.

- **velocidad** _número_

  La velocidad de la voz. Debe ser entre 0,25 y 2. Por defecto, es `1`.

- **semilla** _número_

  Una semilla opcional para la generación determinista.

- **conversacional** _boolean_

  Si se debe utilizar un estilo conversacional. Por defecto, es `false`.

- **longitud** _número_

  La longitud máxima del audio en segundos. El valor máximo es 300.

- **topP** _número_

  El parámetro de muestreo top-p. Debe ser entre 0 y 1. Por defecto, es `1`.

- **temperatura** _número_

  El parámetro de temperatura para la muestreza. Debe ser al menos 0. Por defecto, es `1`.

### Capabilities del Modelo

| Modelo      | Instrucciones        |
| ---------- | ------------------- |
| `aurora`   | <Check size={18} /> |
| `blizzard` | <Check size={18} /> |

---
title: Google Generative AI
description: Aprende a utilizar el proveedor de Google Generative AI.
---

# Proveedor de IA Generativa de Google

El [Proveedor de IA Generativa de Google](https://ai.google/discover/generativeai/) contiene soporte para modelos de lenguaje y de embeddings para las API de [IA Generativa de Google](https://ai.google.dev/api/rest).

## Configuración

El proveedor de Google está disponible en el módulo `@ai-sdk/google`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/google" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/google" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/google" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `google` desde `@ai-sdk/google`:

```ts
import { google } from '@ai-sdk/google';
```

Si necesitas una configuración personalizada, puedes importar `createGoogleGenerativeAI` desde `@ai-sdk/google` y crear una instancia de proveedor con tus ajustes:

```ts
import { createGoogleGenerativeAI } from '@ai-sdk/google';

const google = createGoogleGenerativeAI({
  // ajustes personalizados
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor de Google Generative AI:

- **baseURL** _cadena_

  Utiliza una dirección URL diferente para prefixar las llamadas a API, por ejemplo, para utilizar servidores proxy.
  La dirección URL predeterminada es `https://generativelanguage.googleapis.com/v1beta`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `x-goog-api-key`.
  Se establece en la variable de entorno `GOOGLE_GENERATIVE_AI_API_KEY` por defecto.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(entrada: RequestInfo, init?: RequestInit) => Promesa&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Se establece en la función global `fetch` por defecto.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Lenguaje

Puedes crear modelos que llamen a la [API de Inteligencia Artificial Generativa de Google](https://ai.google.dev/api/rest) utilizando la instancia del proveedor.
El primer argumento es el id del modelo, por ejemplo `gemini-1.5-pro-latest`.
Los modelos admiten llamadas a herramientas y algunos tienen capacidades multi-modales.

```ts
const model = google('gemini-1.5-pro-latest');
```

<Nota>
  Puedes utilizar modelos fine-tuneados prefijando el id del modelo con `tunedModels/`,
  por ejemplo `tunedModels/my-model`.
</Nota>

La Inteligencia Artificial Generativa de Google también admite algunas configuraciones de modelo específicas que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const model = google('gemini-1.5-pro-latest', {
  safetySettings: [
    { category: 'HARM_CATEGORY_UNSPECIFIED', threshold: 'BLOCK_LOW_AND_ABOVE' },
  ],
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de Inteligencia Artificial Generativa de Google:

- **cachedContent** _cadena_

  Opcional. El nombre del contenido cacheado utilizado como contexto para servir la predicción.
  Formato: cachedContents/\{cachedContent\}

- **structuredOutputs** _boolean_

  Opcional. Habilitar salida estructurada. Por defecto es true.

  Esto es útil cuando el esquema JSON contiene elementos que no están soportados por la versión del esquema OpenAPI que utiliza la Inteligencia Artificial Generativa de Google. Puedes utilizar esto para deshabilitar las salidas estructuradas si lo necesitas.

  Consulta [Solucionando Problemas: Limitaciones de Esquema](

# Limitaciones del Esquema) para obtener más detalles.

- **safetySettings** _Array\<\{ categoria: string; threshold: string \}\>_

  Opcional. Configuraciones de seguridad para el modelo.

  - **categoria** _string_

    La categoría de la configuración de seguridad. Puede ser uno de los siguientes:

    - `HARM_CATEGORY_HATE_SPEECH`
    - `HARM_CATEGORY_DANGEROUS_CONTENT`
    - `HARM_CATEGORY_HARASSMENT`
    - `HARM_CATEGORY_SEXUALLY_EXPLICIT`

  - **threshold** _string_

    El umbral de la configuración de seguridad. Puede ser uno de los siguientes:

    - `HARM_BLOCK_THRESHOLD_UNSPECIFIED`
    - `BLOCK_LOW_AND_ABOVE`
    - `BLOCK_MEDIUM_AND_ABOVE`
    - `BLOCK_ONLY_HIGH`
    - `BLOCK_NONE`

Se pueden realizar configuraciones adicionales utilizando opciones del proveedor de Google Generative AI. Puede validar las opciones del proveedor utilizando el tipo `GoogleGenerativeAIProviderOptions`.

```ts
import { google } from '@ai-sdk/google';
import { GoogleGenerativeAIProviderOptions } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text } = await generateText({
  model: google('gemini-1.5-pro-latest'),
  providerOptions: {
    google: {
      responseModalities: ['TEXT', 'IMAGE'],
    } satisfies GoogleGenerativeAIProviderOptions,
  },
  // ...
});
```

Otro ejemplo que muestra el uso de opciones de proveedor para especificar el presupuesto de pensamiento para un modelo de pensamiento de Google Generative AI:

```ts
import { google } from '@ai-sdk/google';
import { GoogleGenerativeAIProviderOptions } from '@ai-sdk/google';
import { generateText } from 'ai';
```

```javascript
const { text } = await generateText({
  model: google('gemini-2.5-flash-preview-04-17'),
  providerOptions: {
    google: {
      thinkingConfig: {
        thinkingBudget: 2048,
      },
    } satisfies GoogleGenerativeAIProviderOptions,
  },
  // ...
});
```

Las siguientes opciones de proveedor están disponibles:

- **modalidadesDeRespuesta** _string[]_
  Las modalidades a utilizar para la respuesta. Las siguientes modalidades están soportadas: `TEXTO`, `IMAGEN`. Cuando no se define o está vacío, el modelo devuelve solo texto por defecto.

- **configuracionDePensamiento** _\{ presupuestoDePensamiento: número; \}_

  Opcional. Configuración para el proceso de pensamiento del modelo. Solo está soportado por modelos de [Google Generative AI específicos](https://ai.google.dev/gemini-api/docs/thinking).

  - **presupuestoDePensamiento** _número_

    Opcional. Da al modelo orientación sobre el número de tokens de pensamiento que puede utilizar al generar una respuesta. Debe ser un número entero en el rango de 0 a 24576. Establecerlo en 0 deshabilita el pensamiento. Presupuestos de 1 a 1024 tokens se establecerán en 1024.
    Para obtener más información, consulte la [documentación de Google Generative AI](https://ai.google.dev/gemini-api/docs/thinking).

Puede utilizar modelos de lenguaje de Google Generative AI para generar texto con la función `generateText`:

```typescript
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text } = await generateText({
  model: google('gemini-1.5-pro-latest'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Google Generative AI también se pueden utilizar en las funciones `streamText`, `generateObject` y `streamObject` (consulte [AI SDK Core](/docs/ai-sdk-core)).

### Entradas de archivo

El proveedor de IA generativa de Google admite entradas de archivo, por ejemplo, archivos PDF.

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const result = await generateText({
  model: google('gemini-1.5-flash'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Cuál es el modelo de inmersión según este documento?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
});
```

<Nota>
  El SDK de IA descargará automáticamente URLs si las pasas como datos, excepto
  por `https://generativelanguage.googleapis.com/v1beta/files/`. Puedes usar la API de archivos de IA generativa de Google para subir archivos más grandes a esa ubicación.
</Nota>

Consulta [Partes de archivo](/docs/fundamentos/prompts#partes-de-archivo) para obtener detalles sobre cómo utilizar archivos en solicitudes.

### Contenido Cachado

Puedes utilizar modelos de lenguaje generativos de Google para cachar contenido:

```ts
import { google } from '@ai-sdk/google';
import { GoogleAICacheManager } from '@google/generative-ai/server';
import { generateText } from 'ai';

const cacheManager = new GoogleAICacheManager(
  process.env.GOOGLE_GENERATIVE_AI_API_KEY,
);

// A partir del 23 de agosto de 2024, estos son los únicos modelos que admiten cachado
type GoogleModelCacheableId =
  | 'models/gemini-1.5-flash-001'
  | 'models/gemini-1.5-pro-001';

const model: GoogleModelCacheableId = 'models/gemini-1.5-pro-001';

const { name: cachedContent } = await cacheManager.create({
  model,
  contents: [
    {
      role: 'user',
      parts: [{ text: '1000 Recetas de Lasaña...' }],
    },
  ],
  ttlSeconds: 60 * 5,
});

const { text: recetaDeLasañaVegetariana } = await generateText({
  model: google(model, { cachedContent }),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});

const { text: recetaDeLasañaDeCarne } = await generateText({
  model: google(model, { cachedContent }),
  prompt: 'Escribe una receta de lasaña de carne para 12 personas.',
});
```

### Buscador de Fundamentación

Con [buscador de fundamentación](https://ai.google.dev/gemini-api/docs/grounding),
el modelo tiene acceso a la información más reciente utilizando Google Search.
El buscador de fundamentación se puede utilizar para proporcionar respuestas sobre eventos actuales:

```ts highlight="7,14-20"
import { google } from '@ai-sdk/google';
import { GoogleGenerativeAIProviderMetadata } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text, providerMetadata } = await generateText({
  model: google('gemini-1.5-pro', {
    useSearchGrounding: true,
  }),
  prompt:
    'List the top 5 noticias de San Francisco de la semana pasada.' +
    'Debes incluir la fecha de cada artículo.',
});

// accede a los metadatos de fundamentación. El casting al tipo de metadatos del proveedor
// es opcional pero proporciona autocompletado y seguridad de tipo.
const metadata = providerMetadata?.google as
  | GoogleGenerativeAIProviderMetadata
  | undefined;
const groundingMetadata = metadata?.groundingMetadata;
const safetyRatings = metadata?.safetyRatings;
```

Los metadatos de fundamentación incluyen información detallada sobre cómo se utilizaron los resultados de búsqueda para fundamentar la respuesta del modelo. A continuación, se presentan los campos disponibles:

- **`webSearchQueries`** (`string[] | null`)

  - Arreglo de consultas de búsqueda utilizadas para recuperar información
  - Ejemplo: `["¿Cuál es el tiempo en Chicago este fin de semana?"]`

- **`searchEntryPoint`** (`{ renderedContent: string } | null`)

  - Contiene el contenido principal del resultado de búsqueda utilizado como punto de entrada
  - El campo `renderedContent` contiene el contenido formateado

- **`groundingSupports`** (Array de objetos de soporte | null)
  - Contiene detalles sobre cómo específicas partes de la respuesta están respaldadas por los resultados de búsqueda
  - Cada objeto de soporte incluye:
    - **`segment`**: Información sobre el segmento de texto anclado
      - `text`: El texto segmentado real
      - `startIndex`: Posición de inicio en la respuesta
      - `endIndex`: Posición de fin en la respuesta
    - **`groundingChunkIndices`**: Referencias a los chunk de soporte de resultados de búsqueda
    - **`confidenceScores`**: Puntuaciones de confianza (0-1) para cada chunk de soporte

Ejemplo de respuesta:

```json
{
  "groundingMetadata": {
    "webSearchQueries": ["¿Cuál es el tiempo en Chicago este fin de semana?"],
    "searchEntryPoint": {
      "renderedContent": "..."
    },
    "groundingSupports": [
      {
        "segment": {
          "startIndex": 0,
          "endIndex": 65,
          "text": "El tiempo en Chicago cambia rápidamente, por lo que los capas te permiten ajustar fácilmente."
        },
        "groundingChunkIndices": [0],
        "confidenceScores": [0.99]
      }
    ]
  }
}
```

#### Recuperación Dinámica

Con [recuperación dinámica](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-with-google-search#dynamic-retrieval), puedes configurar cómo el modelo decide cuándo activar Grounding con Google Search. Esto te da más control sobre cuándo y cómo el modelo fundamenta sus respuestas.

```ts highlight="7-10"
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text, providerMetadata } = await generateText({
  model: google('gemini-1.5-flash', {
    useSearchGrounding: true,
    dynamicRetrievalConfig: {
      mode: 'MODE_DYNAMIC',
      dynamicThreshold: 0.8,
    },
  }),
  prompt: '¿Quién ganó el último Gran Premio de F1?',
});
```

La configuración `dynamicRetrievalConfig` describe las opciones para personalizar la recuperación dinámica:

- `mode`: El modo del predictor a ser utilizado en la recuperación dinámica. Los siguientes modos están soportados:

  - `MODE_DYNAMIC`: Realizar la recuperación solo cuando el sistema decida que es necesario
  - `MODE_UNSPECIFIED`: Activar siempre la recuperación

- `dynamicThreshold`: El umbral a ser utilizado en la recuperación dinámica (si no se establece, se utiliza un valor por defecto del sistema).

<Nota>
  La recuperación dinámica solo está disponible con modelos Gemini 1.5 Flash y no está soportada con variantes de 8B.
</Nota>

### Fuentes

Cuando utilices [Grounding con Búsqueda](

# Búsqueda de fuentes
Cuando se active la opción `search-grounding)`, el modelo incluirá las fuentes en la respuesta.
Puedes acceder a ellas utilizando la propiedad `sources` del resultado:

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const { sources } = await generateText({
  model: google('gemini-2.0-flash-exp', { useSearchGrounding: true }),
  prompt: 'Lista los 5 principales noticias de San Francisco de la semana pasada.',
});
```

### Salidas de Imágenes

El modelo `gemini-2.0-flash-exp` admite la generación de imágenes. Las imágenes se exponen como archivos en la respuesta.
Necesitas habilitar la salida de imágenes en las opciones del proveedor utilizando la opción `responseModalities`.

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const result = await generateText({
  model: google('gemini-2.0-flash-exp'),
  providerOptions: {
    google: { responseModalities: ['TEXT', 'IMAGE'] },
  },
  prompt: 'Genera una imagen de un gato cómico',
});

for (const file of result.files) {
  if (file.mimeType.startsWith('image/')) {
    // muestra la imagen
  }
}
```

### Clasificaciones de Seguridad

Las clasificaciones de seguridad proporcionan información sobre la seguridad de la respuesta del modelo.
Consulte la [documentación de Google AI sobre ajustes de seguridad](https://ai.google.dev/gemini-api/docs/safety-settings).

Ejemplo de fragmento de respuesta:

```json
{
  "evaluacionesDeSeguridad": [
    {
      "categoria": "HARM_CATEGORY_HATE_SPEECH",
      "probabilidad": "NEGLIGIBLE",
      "puntuacionDeProbabilidad": 0.11027937,
      "gravedad": "HARM_SEVERITY_LOW",
      "puntuacionDeGravedad": 0.28487435
    },
    {
      "categoria": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "probabilidad": "HIGH",
      "bloqueado": true,
      "puntuacionDeProbabilidad": 0.95422274,
      "gravedad": "HARM_SEVERITY_MEDIUM",
      "puntuacionDeGravedad": 0.43398145
    },
   

### Resolución de Problemas

#### Limitaciones del Esquema

El API de Inteligencia Artificial Generativa de Google utiliza un subconjunto del esquema OpenAPI 3.0,
que no admite características como las uniones.
Los errores que obtienes en este caso se parecen a los siguientes:

`GenerateContentRequest.generation_config.response_schema.properties[occupation].type: must be specified`

Por defecto, los resultados estructurados están habilitados (y para llamadas a herramientas son obligatorios).
Puedes deshabilitar los resultados estructurados para la generación de objetos como un trabajo alrededor:

```ts highlight="3,8"
const result = await generateObject({
  model: google('gemini-1.5-pro-latest', {
    structuredOutputs: false,
  }),
  schema: z.object({
    name: z.string(),
    age: z.number(),
    contact: z.union([
      z.object({
        type: z.literal('email'),
        value: z.string(),
      }),
      z.object({
        type: z.literal('phone'),
        value: z.string(),
      }),
    ]),
  }),
  prompt: 'Genera un ejemplo de persona para la prueba.',
});
```

Las siguientes características de Zod se conocen que no funcionan con Google Generative AI:

- `z.union`
- `z.record`

### Capacidad del Modelo

### Resumen

| Modelo                          | Entrada de imagen      | Generación de objetos | Uso de herramienta       | Streaming de herramienta |
| ------------------------------- | --------------------- | --------------------- | ----------------------- | ----------------------- |
| `gemini-2.5-pro-preview-05-06`  | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.5-flash-preview-04-17` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.5-pro-exp-03-25`      | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.0-flash`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-pro`                | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-pro-latest`         | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-flash`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `gemini-1.5-flash-latest`        | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-flash-8b`            | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-flash-8b-latest`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Nota>
  La tabla anterior enumera modelos populares. Consulte la [documentación de
  AI Generativo de Google](https://ai.google.dev/gemini-api/docs/models/gemini)
  para obtener una lista completa de modelos disponibles. La tabla anterior enumera
  modelos populares. También puede pasar cualquier ID de modelo de proveedor disponible
  como una cadena si es necesario.
</Nota>

## Incorporando Modelos

Puedes crear modelos que llamen a la [API de embebedores de Google Generative AI](https://ai.google.dev/api/embeddings)
usando el método de fábrica `textEmbeddingModel()`.

```ts
const modelo = google.textEmbeddingModel('text-embedding-004');
```

Los modelos de embebedores de Google Generative AI admiten ajustes adicionales. Puedes pasarlos como un argumento de opciones:

```ts
const modelo = google.textEmbeddingModel('text-embedding-004', {
  outputDimensionality: 512, // opcional, número de dimensiones para el embebedor
  taskType: 'SIMILARIDAD_SEMÁNTICA', // opcional, especifica el tipo de tarea para generar embebedores
});
```

Los siguientes ajustes opcionales están disponibles para los modelos de embebedores de Google Generative AI:

- **outputDimensionality**: _número_

  Dimension reducida opcional para el embebedor de salida. Si se establece, los valores excesivos en el embebedor de salida se truncan desde el final.

- **taskType**: _cadena_

  Opcional. Especifica el tipo de tarea para generar embebedores. Los tipos de tarea admitidos incluyen:

  - `SIMILARIDAD_SEMÁNTICA`: Optimizado para la similitud de texto.
  - `CLASIFICACIÓN`: Optimizado para la clasificación de texto.
  - `AGrupación`: Optimizado para agrupar textos según similitud.
  - `RETRIEVE_DOCUMENTO`: Optimizado para la recuperación de documentos.
  - `RETRIEVE_BÚSQUEDA`: Optimizado para la búsqueda de recuperación.
  - `RESPONDER_PREGUNTAS`: Optimizado para responder preguntas.
  - `VERIFICACIÓN_HECHOS`: Optimizado para verificar información de hecho.
  - `RETRIEVE_BLOQUE_CODIGO`: Optimizado para recuperar bloques de código según consultas de lenguaje natural.

### Capacidad del Modelo

| Modelo                | Dimensiones por Defecto | Dimensiones Personalizadas   |
| -------------------- | ------------------ | ------------------- |
| `text-embedding-004` | 768                | <Check size={18} /> |

---
titulo: Hume
descripcion: Aprende a utilizar el proveedor Hume para el SDK de Inteligencia Artificial.
---

# Proveedor Hume

El [Hume](https://hume.ai/) provee soporte para modelos de lenguaje en la API de transcripción de Hume.

## Configuración

El proveedor Hume está disponible en el módulo `@ai-sdk/hume`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/hume" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/hume" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/hume" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `hume` desde `@ai-sdk/hume`:

```ts
import { hume } from '@ai-sdk/hume';
```

Si necesitas una configuración personalizada, puedes importar `createHume` desde `@ai-sdk/hume` y crear una instancia de proveedor con tus ajustes:

```ts
import { createHume } from '@ai-sdk/hume';

const hume = createHume({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Hume:

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Se establece en la variable de entorno `HUME_API_KEY` por defecto.

- **headers** _Registro&lt;cadena,cadena&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(entrada: Información de solicitud, init?: Inicialización de solicitud) => Promesa&lt;Respuesta&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Se establece en la función global `fetch` por defecto.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Discurso

Puedes crear modelos que llamen a la [API de habla de Hume](https://dev.hume.ai/docs/text-to-speech-tts/overview)
usando el método de fábrica `.speech()`.

```ts
const modelo = hume.speech();
```

También puedes pasar opciones adicionales específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrando una voz para utilizar en el audio generado.

```ts highlight="6"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { hume } from '@ai-sdk/hume';

const resultado = await generateSpeech({
  modelo: hume.speech(),
  texto: 'Hola, mundo!',
  voz: 'd8ab67c6-953d-4bd8-9370-8fa53a0f1453',
  providerOptions: { hume: {} },
});
```

Las siguientes opciones de proveedor están disponibles:

- **context** _objeto_

  O:

  - `{ generationId: string }` - Un ID de generación para utilizar en el contexto.
  - `{ utterances: HumeUtterance[] }` - Un array de objetos de emisiones para el contexto.

### Capabilities del Modelo

| Modelo     | Instrucciones        |
| --------- | ------------------- |
| `default` | <Check size={18} /> |

---
title: Google Vertex AI
description: Aprende a utilizar el proveedor de Google Vertex AI.
---

# Proveedor de Google Vertex

El proveedor de Google Vertex para el [SDK de Inteligencia Artificial](/docs) contiene soporte para modelos de lenguaje en los [APIs de Google Vertex AI](https://cloud.google.com/vertex-ai). Esto incluye soporte para [modelos Gemini de Google](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models) y [modelos socios de Anthropic Claude](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).

<Nota>
  El proveedor de Google Vertex es compatible con tanto el entorno de ejecución de Node.js como con el entorno de ejecución de Edge.
  El entorno de ejecución de Edge se soporta a través del sub-módulo `@ai-sdk/google-vertex/edge`.
  Más detalles pueden encontrarse en las secciones [Google Vertex Edge Runtime](#google-vertex-edge-runtime) y [Google Vertex Anthropic Edge Runtime](#google-vertex-anthropic-edge-runtime) a continuación.
</Nota>

## Configuración

El proveedor de Google Vertex y el proveedor de Google Vertex Anthropic están disponibles ambos en el módulo `@ai-sdk/google-vertex`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/google-vertex" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/google-vertex" dark />
  </Tab>
  <Tab>
    <Snippet
      text="yarn add @ai-sdk/google-vertex @google-cloud/vertexai"
      dark
    />
  </Tab>
</Tabs>

## Uso del Proveedor de Google Vertex

La instancia del proveedor de Google Vertex se utiliza para crear instancias de modelo que llamen a la API de Vertex AI. Los modelos disponibles con este proveedor incluyen [modelos de Gemini de Google](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models). Si está buscando utilizar [modelos de Claude de Anthropic](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude), consulte la sección [Uso del proveedor de Google Vertex Anthropic](#uso-del-proveedor-de-google-vertex-anthropic) a continuación.

### Instancia del Proveedor

Puede importar la instancia del proveedor predeterminada `vertex` de `@ai-sdk/google-vertex`:

```ts
import { vertex } from '@ai-sdk/google-vertex';
```

Si necesita una configuración personalizada, puede importar `createVertex` de `@ai-sdk/google-vertex` y crear una instancia del proveedor con sus configuraciones:

```ts
import { createVertex } from '@ai-sdk/google-vertex';

const vertex = createVertex({
  proyecto: 'mi-proyecto', // opcional
  ubicación: 'us-central1', // opcional
});
```

Google Vertex admite dos implementaciones de autenticación diferentes dependiendo de su entorno de tiempo de ejecución.

#### Entorno de tiempo de ejecución de Node.js

El entorno de tiempo de ejecución de Node.js es el entorno de tiempo de ejecución predeterminado admitido por el SDK de IA. Soporta todas las opciones de autenticación estándar de Google Cloud a través de la biblioteca `google-auth-library` <https://github.com/googleapis/google-auth-library-nodejs?tab=readme-ov-file

# Formas de autenticar). El uso típico implica configurar un camino a un archivo de credenciales json en la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS`. El archivo de credenciales se puede obtener desde el [Console de Cloud de Google](https://console.cloud.google.com/apis/credentials).

Si deseas personalizar las opciones de autenticación de Google, puedes pasarlas como opciones a la función `createVertex`, por ejemplo:

```ts
import { createVertex } from '@ai-sdk/google-vertex';

const vertex = createVertex({
  googleAuthOptions: {
    credentials: {
      client_email: 'my-email',
      private_key: 'my-private-key',
    },
  },
});
```

##### Configuración de ajustes de proveedor opcionales

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor:

- **project** _cadena_

  El ID del proyecto de Cloud de Google que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `GOOGLE_VERTEX_PROJECT` por defecto.

- **location** _cadena_

  La ubicación de Cloud de Google que deseas utilizar para las llamadas a la API, por ejemplo `us-central1`.
  Utiliza la variable de entorno `GOOGLE_VERTEX_LOCATION` por defecto.

- **googleAuthOptions** _objeto_

  Opcional. Las opciones de autenticación utilizadas por la [Biblioteca de autenticación de Google](https://github.com/googleapis/google-auth-library-nodejs/). Consulta también la [GoogleAuthOptions](https://github.com/googleapis/google-auth-library-nodejs/blob/08978822e1b7b5961f0e355df51d738e012be392/src/auth/googleauth.ts)

# L87C18-L87C35) interfaz.

  - **authClient** _objeto_
    Un objeto `AuthClient` para usar.

  - **keyFilename** _cadena de texto_
    Ruta a un archivo de clave .json, .pem o .p12.

  - **keyFile** _cadena de texto_
    Ruta a un archivo de clave .json, .pem o .p12.

  - **credentials** _objeto_
    Objeto que contiene las propiedades `client_email` y `private_key`, o las opciones de cliente de cuenta externa.

  - **clientOptions** _objeto_
    Objeto de opciones pasado al constructor del cliente.

  - **scopes** _cadena de texto | cadena de texto[]_
    Ámbitos requeridos para la solicitud de API deseada.

  - **projectId** _cadena de texto_
    Tu ID de proyecto.

  - **universeDomain** _cadena de texto_
    El dominio de servicio predeterminado para un universo de Cloud.

- **cabeceras** _Resolvable&lt;Registro&lt;cadena de texto, cadena de texto | indefinido&gt;&gt;_

  Cabeceras para incluir en las solicitudes. Pueden proporcionarse en múltiples formatos:

  - Un registro de pares clave-valor de cabecera: `Record<string, string | undefined>`
  - Una función que devuelve cabeceras: `() => Record<string, string | undefined>`
  - Una función asíncrona que devuelve cabeceras: `async () => Record<string, string | undefined>`
  - Una promesa que se resuelve en cabeceras: `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). 
  Por defecto utiliza la función global `fetch`. 
  Puedes utilizarla como middleware para interceptar solicitudes, 
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

- **baseURL** _cadena de texto_

Opcional. URL base para las llamadas a la API de Google Vertex, por ejemplo, para utilizar servidores proxy. Por defecto, se construye utilizando la ubicación y el proyecto:
  `https://${location}-aiplatform.googleapis.com/v1/projects/${project}/locations/${location}/publishers/google`

<a id="google-vertex-edge-runtime"></a>

#### Runtime de Edge

Los runtimes de Edge (como Vercel Edge Functions y Cloudflare Workers) son entornos de JavaScript ligeros que se ejecutan más cerca de los usuarios en la orilla de la red.
Sólo proporcionan un subconjunto de las API estándar de Node.js.
Por ejemplo, el acceso directo al sistema de archivos no está disponible, y muchas bibliotecas específicas de Node.js
(incluyendo la biblioteca de autenticación de Google estándar) no son compatibles.

La versión del proveedor de Vertex de Google para el runtime de Edge de Edge admite las [Credenciales de Defecto de Aplicación de Google](https://github.com/googleapis/google-auth-library-nodejs?tab=readme-ov-file) de Google.

# Credenciales por defecto del aplicación) a través de variables de entorno. Los valores pueden obtenerse de un archivo de credenciales JSON desde el [Console de Cloud de Google](https://console.cloud.google.com/apis/credentials).

Puedes importar la instancia del proveedor predeterminado `vertex` desde `@ai-sdk/google-vertex/edge`:

```ts
import { vertex } from '@ai-sdk/google-vertex/edge';
```

<Nota>
  El submódulo `/edge` se incluye en el paquete `@ai-sdk/google-vertex`, por lo que
  no necesitas instalarlo por separado. Debes importar desde
  `@ai-sdk/google-vertex/edge` para diferenciarlo del proveedor de Node.js.
</Nota>

Si necesitas una configuración personalizada, puedes importar `createVertex` desde `@ai-sdk/google-vertex/edge` y crear una instancia de proveedor con tus ajustes:

```ts
import { createVertex } from '@ai-sdk/google-vertex/edge';

const vertex = createVertex({
  proyecto: 'mi-proyecto', // opcional
  ubicación: 'us-central1', // opcional
});
```

Para la autenticación de tiempo de ejecución de Edge, necesitarás establecer estas variables de entorno desde el archivo JSON de credenciales predeterminadas de la aplicación de Google:

- `GOOGLE_CLIENT_EMAIL`
- `GOOGLE_PRIVATE_KEY`
- `GOOGLE_PRIVATE_KEY_ID` (opcional)

Estos valores pueden obtenerse desde un archivo JSON de cuenta de servicio desde el [Console de Cloud de Google](https://console.cloud.google.com/apis/credentials).

##### Configuración de Proveedor Opcional

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor:

- **project** _cadena_

  El ID del proyecto de Google Cloud que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `GOOGLE_VERTEX_PROJECT` por defecto.

- **location** _cadena_

  La ubicación de Google Cloud que deseas utilizar para las llamadas a la API, por ejemplo `us-central1`.
  Utiliza la variable de entorno `GOOGLE_VERTEX_LOCATION` por defecto.

- **googleCredentials** _objeto_

  Opcional. Las credenciales utilizadas por el proveedor de Edge para la autenticación. Estas credenciales se establecen típicamente a través de variables de entorno y se derivan de un archivo JSON de cuenta de servicio.

  - **clientEmail** _cadena_
    El correo electrónico del cliente del archivo JSON de cuenta de servicio. Por defecto, utiliza el contenido de la variable de entorno `GOOGLE_CLIENT_EMAIL`.

  - **privateKey** _cadena_
    La clave privada del archivo JSON de cuenta de servicio. Por defecto, utiliza el contenido de la variable de entorno `GOOGLE_PRIVATE_KEY`.

  - **privateKeyId** _cadena_
    El ID de la clave privada del archivo JSON de cuenta de servicio (opcional). Por defecto, utiliza el contenido de la variable de entorno `GOOGLE_PRIVATE_KEY_ID`.

- **headers** _Resolvable&lt;Registro&lt;cadena, cadena | indefinido&gt;&gt;_

  Encabezados para incluir en las solicitudes. Pueden proporcionarse en múltiples formatos:

  - Un registro de pares clave-valor de encabezado: `Registro&lt;cadena, cadena | indefinido&gt;`
  - Una función que devuelve encabezados: `() => Registro&lt;cadena, cadena | indefinido&gt;`
  - Una función asíncrona que devuelve encabezados: `async () => Registro&lt;cadena, cadena | indefinido&gt;`
  - Una promesa que se resuelve con encabezados: `Promise&lt;Registro&lt;cadena, cadena | indefinido&gt;&gt;`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch)
  Se basa por defecto en la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

### Modelos de Lenguaje

Puedes crear modelos que llamen a la API de Vertex utilizando la instancia del proveedor.
El primer argumento es el id del modelo, por ejemplo `gemini-1.5-pro`.

```ts
const model = vertex('gemini-1.5-pro');
```

<Nota>
  Si estás utilizando [modelos propios](https://cloud.google.com/vertex-ai/docs/training-overview), el nombre de tu modelo necesita empezar con `projects/`.
</Nota>

Los modelos de Vertex de Google también admiten algunas configuraciones específicas del modelo que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings). Puedes pasarlas como un argumento de opciones:

```ts
const model = vertex('gemini-1.5-pro', {
  safetySettings: [
    { category: 'HARM_CATEGORY_UNSPECIFIED', threshold: 'BLOCK_LOW_AND_ABOVE' },
  ],
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de Google Vertex:

- **structuredOutputs** _boolean_

  Opcional. Habilitar salida estructurada. Predeterminado es true.

  Esto es útil cuando el esquema JSON contiene elementos que no están soportados por la versión de esquema OpenAPI que utiliza Vertex de Google. Puedes utilizar esto para deshabilitar la salida estructurada si lo necesitas.

  Ver [Resolución de problemas: Limitaciones de esquema](

# Limitaciones del Esquema) para obtener más detalles.

- **safetySettings** _Array\<\{ categoria: string; threshold: string \}\>_

  Opcional. Configuraciones de seguridad para el modelo.

  - **categoria** _string_

    La categoría de la configuración de seguridad. Puede ser uno de los siguientes:

    - `HARM_CATEGORY_UNSPECIFIED`
    - `HARM_CATEGORY_DISCURSO_DE_HATE`
    - `HARM_CATEGORY_CONTENIDO_PELIGROSO`
    - `HARM_CATEGORY_ACOSO`
    - `HARM_CATEGORY_EXPLICACIÓN_SEXUAL`
    - `HARM_CATEGORY_INTEGRIDAD_CÍVICA`

  - **threshold** _string_

    El umbral de la configuración de seguridad. Puede ser uno de los siguientes:

    - `HARM_BLOCK_THRESHOLD_UNSPECIFIED`
    - `BLOCK_LOW_AND_ABOVE`
    - `BLOCK_MEDIUM_AND_ABOVE`
    - `BLOCK_ONLY_HIGH`
    - `BLOCK_NONE`

- **useSearchGrounding** _boolean_

  Opcional. Cuando está habilitado, el modelo utilizará [búsqueda de Google para fijar la respuesta](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview).

- **audioTimestamp** _boolean_

  Opcional. Habilita la comprensión de timestamp para archivos de audio. Por defecto, es falso.

  Esto es útil para generar transcripciones con timestamps precisos.
  Consulta [la documentación de Google](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/audio-understanding) para obtener detalles de uso.

Puedes utilizar modelos de lenguaje de Google Vertex para generar texto con la función `generateText`:

```ts highlight="1,4"
import { vertex } from '@ai-sdk/google-vertex';
import { generateText } from 'ai';
```

```javascript
const { texto } = await generarTexto({
  modelo: vertex('gemini-1.5-pro'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Google Vertex también se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

#### Razonamiento (Tokens de Pensamiento)

Google Vertex AI, a través de su soporte para modelos Gemini, también puede emitir "tokens de pensamiento", que representan el proceso de razonamiento del modelo. El SDK de AI expone estos como información de razonamiento.

Para habilitar los tokens de pensamiento para modelos Gemini compatibles a través de Vertex, establezca `includeThoughts: true` en la opción de proveedor `thinkingConfig`. Dado que el proveedor de Vertex utiliza el modelo de lenguaje subyacente del proveedor de Google, estas opciones se pasan a través de `providerOptions.google`:

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { GoogleGenerativeAIProviderOptions } from '@ai-sdk/google'; // Nota: importando desde @ai-sdk/google
import { generateText, streamText } from 'ai';

// Para generateText:
const { text, razonamiento, detallesDeRazonamiento } = await generateText({
  modelo: vertex('gemini-2.5-flash-preview-04-17'), // O cualquier otro modelo compatible a través de Vertex
  opcionesDelProveedor: {
    google: {
      // Las opciones están anidadas bajo 'google' para el proveedor de Vertex
      thinkingConfig: {
        includeThoughts: true,
        // thinkingBudget: 2048, // Opcional
      },
    } satisface GoogleGenerativeAIProviderOptions,
  },
  prompt: 'Explique el cálculo cuántico en términos simples.',
});

console.log('Razonamiento:', razonamiento);
console.log('Detalles de Razonamiento:', detallesDeRazonamiento);
console.log('Texto Final:', text);
```

```markdown
// Para streamText:
const resultado = streamText({
  modelo: vertex('gemini-2.5-flash-preview-04-17'), // O bien otro modelo admitido a través de Vertex
  opcionesProveedor: {
    google: {
      // Las opciones están anidadas bajo 'google' para el proveedor de Vertex
      thinkingConfig: {
        includeThoughts: true,
        // thinkingBudget: 2048, // Opcional
      },
    } satisface GoogleGenerativeAIProviderOptions,
  },
  prompt: 'Explique el cálculo cuántico en términos simples.',
});

for await (const parte of resultado.fullStream) {
  if (parte.type === 'razonamiento') {
    process.stdout.write(`PENSAMIENTO: ${parte.textDelta}\n`);
  } else if (parte.type === 'delta-de-texto') {
    process.stdout.write(parte.textDelta);
  }
}
```

Cuando `includeThoughts` es true, las partes de la respuesta de la API marcadas con `thought: true` se procesarán como razonamiento.

- En `generateText`, estos contribuyen a los campos `razonamiento` (cadena) y `razonamientoDetalles` (array).
- En `streamText`, se emiten como partes de flujo `razonamiento`.

<Nota>
  Consulte la [documentación de Vertex AI de Google sobre "pensamiento"](https://cloud.google.com/vertex-ai/generative-ai/docs/thinking)
  para compatibilidad de modelos y detalles adicionales.
</Nota>

#### Entradas de Archivos

El proveedor de Google Vertex admite entradas de archivos, por ejemplo, archivos PDF.

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { generateText } from 'ai';

const { text } = await generateText({
  model: vertex('gemini-1.5-pro'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Cuál es el modelo de embeddings según este documento?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
});
```

<Nota>
  El SDK de AI descargará automáticamente URLs si las pasas como datos, excepto
  para `gs://` URLs. Puedes usar la API de Google Cloud Storage para subir archivos
  más grandes a esa ubicación.
</Nota>

Consulte [Partes de Archivos](/docs/fundamentos/prompts#partes-de-archivos) para obtener detalles sobre cómo utilizar archivos en promt.

#### Buscador de Fundamentación

Con [buscador de fundamentación](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview),
el modelo tiene acceso a la información más reciente utilizando Google Search.
El buscador de fundamentación se puede utilizar para proporcionar respuestas sobre eventos actuales:

```ts highlight="7,14-20"
import { vertex } from '@ai-sdk/google-vertex';
import { GoogleGenerativeAIProviderMetadata } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text, providerMetadata } = await generateText({
  model: vertex('gemini-1.5-pro', {
    useSearchGrounding: true,
  }),
  prompt:
    'List the top 5 San Francisco news from the past week.' +
    'You must include the date of each article.',
});

// acceso a los metadatos de fundamentación. La conversión al tipo de metadatos del proveedor
// es opcional pero proporciona autocompletado y seguridad de tipos.
const metadata = providerMetadata?.google as
  | GoogleGenerativeAIProviderMetadata
  | undefined;
const groundingMetadata = metadata?.groundingMetadata;
const safetyRatings = metadata?.safetyRatings;
```

Los metadatos de fundamentación incluyen información detallada sobre cómo se utilizaron los resultados de búsqueda para fundamentar la respuesta del modelo. A continuación, se muestran los campos disponibles:

- **`webSearchQueries`** (`string[] | null`)

  - Arreglo de consultas de búsqueda utilizadas para recuperar información
  - Ejemplo: `["¿Cuál es el tiempo en Chicago este fin de semana?"]`

- **`searchEntryPoint`** (`{ renderedContent: string } | null`)

  - Contiene el contenido principal del resultado de búsqueda utilizado como punto de entrada
  - El campo `renderedContent` contiene el contenido formateado

- **`soportesDeFondo`** (Array de objetos de soporte | null)
  - Contiene detalles sobre cómo ciertas partes de la respuesta están respaldadas por los resultados de búsqueda
  - Cada objeto de soporte incluye:
    - **`segmento`**: Información sobre el segmento de texto aterrazado
      - `texto`: El segmento de texto real
      - `startIndex`: Posición de inicio en la respuesta
      - `endIndex`: Posición de fin en la respuesta
    - **`índicesDeChunkDeAterrazado`**: Referencias a los chunk de búsqueda que respaldan
    - **`puntuacionesDeConfianza`**: Puntuaciones de confianza (0-1) para cada chunk respaldante

Ejemplo de fragmento de respuesta:

```json
{
  "metadataDeAterrazado": {
    "consultasDeRecuperación": ["¿Cuál es el tiempo en Chicago este fin de semana?"],
    "puntoDeEntradaDeBúsqueda": {
      "contenidoRendido": "..."
    },
    "soportesDeFondo": [
      {
        "segmento": {
          "startIndex": 0,
          "endIndex": 65,
          "texto": "El tiempo en Chicago cambia rápidamente, por lo que los capas te permiten ajustar fácilmente."
        },
        "índicesDeChunkDeAterrazado": [0],
        "puntuacionesDeConfianza": [0.99]
      }
    ]
  }
}
```

<Nota>
  El proveedor de Google Vertex no respalda aún el [modo de recuperación dinámica y el umbral](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-gemini

# Recuperación Dinámica).
</Note>

### Fuentes

Cuando utilices [Buscador de Referencias](#buscador-de-referencias), el modelo incluirá fuentes en la respuesta.
Puedes acceder a ellas utilizando la propiedad `sources` del resultado:

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { generateText } from 'ai';

const { sources } = await generateText({
  model: vertex('gemini-1.5-pro', { useSearchGrounding: true }),
  prompt: 'List the top 5 San Francisco news from the past week.',
});
```

### Clasificaciones de Seguridad

Las clasificaciones de seguridad proporcionan información sobre la seguridad de la respuesta del modelo.
Consulte la [documentación de Google Vertex AI sobre la configuración de filtros de seguridad](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters).

Ejemplo de fragmento de respuesta:

```json
{
  "calificacionesDeSeguridad": [
    {
      "categoria": "CATEGORIA_DE_DANIO_HABLAR_CON_TÓXICO",
      "probabilidad": "NEGLIGIBLE",
      "puntuaciónDeProbabilidad": 0.11027937,
      "gravedad": "GRAVEDAD_DE_DANIO_BAJA",
      "puntuaciónDeGravedad": 0.28487435
    },
    {
      "categoria": "CATEGORIA_DE_DANIO_CONTENIDO_PELIGROSO",
      "probabilidad": "ALTO",
      "bloqueado": true,
      "puntuaciónDeProbabilidad": 0.95422274,
      "gravedad": "GRAVEDAD_DE_DANIO_MED

Para obtener más detalles, consulte la [documentación de Google Vertex AI sobre Grounding con Google Search](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground

# (Desde el suelo a la búsqueda).

### Solución de Problemas

#### Limitaciones del Esquema

El API de Vertex de Google utiliza un subconjunto del esquema OpenAPI 3.0,
que no admite características como las uniones.
Los errores que obtienes en este caso se ven así:

`GenerateContentRequest.generation_config.response_schema.properties[occupation].type: must be specified`

Por defecto, los resultados estructurados están habilitados (y para las llamadas a herramientas son requeridos).
Puedes deshabilitar los resultados estructurados para la generación de objetos como una solución alternativa:

```ts highlight="3,8"
const result = await generateObject({
  model: vertex('gemini-1.5-pro', {
    structuredOutputs: false,
  }),
  schema: z.object({
    name: z.string(),
    age: z.number(),
    contact: z.union([
      z.object({
        type: z.literal('email'),
        value: z.string(),
      }),
      z.object({
        type: z.literal('phone'),
        value: z.string(),
      }),
    ]),
  }),
  prompt: 'Genera un ejemplo de persona para probar.',
});
```

Las siguientes características de Zod se conocen que no funcionan con Google Vertex:

- `z.union`
- `z.record`

### Capacidad del Modelo

| Modelo                  | Entrada de Imagen         | Generación de Objetos   | Uso de Herramienta          | Streaming de Herramienta      |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `gemini-2.0-flash-001` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.0-flash-exp` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-flash`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-pro`       | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. Consulte la documentación de [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#supported-models) para obtener una lista completa de modelos disponibles. La tabla anterior muestra modelos populares. También puedes pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

### Incorporando Modelos

Puedes crear modelos que llamen a la API de embebiendo de Google Vertex AI utilizando el método de fabricación `.textEmbeddingModel()`:

```ts
const modelo = vertex.textEmbeddingModel('text-embedding-004');
```

Los modelos de embebiendo de Google Vertex AI admiten ajustes adicionales. Puedes pasarlos como un argumento de opciones:

```ts
const modelo = vertex.textEmbeddingModel('text-embedding-004', {
  outputDimensionality: 512, // opcional, número de dimensiones para el embebiendo
});
```

Los siguientes ajustes opcionales están disponibles para los modelos de embebiendo de Google Vertex AI:

- **outputDimensionality**: _número_

  Dimensión reducida opcional para el embebiendo de salida. Si se establece, los valores excesivos en el embebiendo de salida se truncan desde el final.

#### Capacidad del Modelo

| Modelo                | Máximo Valor Por Llamada | Llamadas Paralelas      |
| -------------------- | ------------------- | ------------------- |
| `text-embedding-004` | 2048                | <Check size={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. También puedes pasar cualquier modelo ID de proveedor disponible como una cadena si es necesario.
</Nota>

### Modelos de Imágenes

Puedes crear modelos de [Imagen](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview) que llamen a la API [Imagen en Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images)
usando el método de fábrica `.image()`. Para obtener más información sobre la generación de imágenes con el SDK de AI, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: vertex.image('imagen-3.0-generate-002'),
  prompt: 'Una ciudad futurista al atardecer',
  aspectRatio: '16:9',
});
```

Se pueden realizar configuraciones adicionales utilizando opciones del proveedor de Google Vertex. Puedes validar las opciones del proveedor utilizando el tipo `GoogleVertexImageProviderOptions`.

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { GoogleVertexImageProviderOptions } from '@ai-sdk/google-vertex';
import { generateImage } from 'ai';

const { image } = await generateImage({
  model: vertex.image('imagen-3.0-generate-002'),
  providerOptions: {
    vertex: {
      negativePrompt: 'píxeles desenfocados, baja calidad',
    } satisfies GoogleVertexImageProviderOptions,
  },
  // ...
});
```

Las siguientes opciones del proveedor están disponibles:

- **negativePrompt** _cadena_
  Una descripción de qué desalentar en las imágenes generadas.

- **personGeneration** `allow_adult` | `allow_all` | `dont_allow`
  ¿Permitir la generación de personas? Por defecto, `allow_adult`.

- **safetySetting** `block_low_and_above` | `block_medium_and_above` | `block_only_high` | `block_none`
  ¿Bloquear contenido inseguro. Por defecto, `block_medium_and_above`.

- **addWatermark** _boolean_
  ¿Agregar un marcador invisible a las imágenes generadas. Por defecto, `true`.

- **storageUri** _string_
  URI de almacenamiento en la nube para almacenar las imágenes generadas.

<Nota>
  Los modelos de imagen no admiten el parámetro `size`. Utilice el parámetro `aspectRatio` en su lugar.
</Nota>

#### Capacidad del Modelo

| Modelo                          | Aspectos de Ratas             |
| ------------------------------ | ------------------------- |
| `imagen-3.0-generate-002`      | 1:1, 3:4, 4:3, 9:16, 16:9 |
| `imagen-3.0-fast-generate-001` | 1:1, 3:4, 4:3, 9:16, 16:9 |

## Uso del Proveedor de Google Vertex Anthropic

El proveedor de Google Vertex Anthropic para la [SDK de Inteligencia Artificial](/docs) ofrece soporte para los modelos de Anthropic Claude a través de las API de Google Vertex AI. Esta sección proporciona detalles sobre cómo configurar y utilizar el proveedor de Google Vertex Anthropic.

### Instancia del Proveedor

Puedes importar la instancia del proveedor por defecto `vertexAnthropic` de `@ai-sdk/google-vertex/anthropic`:

```typescript
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
```

Si necesitas una configuración personalizada, puedes importar `createVertexAnthropic` de `@ai-sdk/google-vertex/anthropic` y crear una instancia del proveedor con tus ajustes:

```typescript
import { createVertexAnthropic } from '@ai-sdk/google-vertex/anthropic';

const vertexAnthropic = createVertexAnthropic({
  proyecto: 'mi-proyecto', // opcional
  ubicación: 'us-central1', // opcional
});
```

#### Entorno de Ejecución de Node.js

Para entornos de Node.js, el proveedor de Google Vertex Anthropic admite todas las opciones de autenticación estándar de Google Cloud a través de la `google-auth-library`. Puedes personalizar las opciones de autenticación pasándolas a la función `createVertexAnthropic`:

```typescript
import { createVertexAnthropic } from '@ai-sdk/google-vertex/anthropic';

const vertexAnthropic = createVertexAnthropic({
  googleAuthOptions: {
    credentials: {
      client_email: 'my-email',
      private_key: 'my-private-key',
    },
  },
});
```

##### Configuraciones de Proveedor Opcionales

Puedes utilizar las siguientes configuraciones opcionales para personalizar la instancia del proveedor de Google Vertex Anthropic:

- **project** _cadena_

  El ID del proyecto de Google Cloud que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `GOOGLE_VERTEX_PROJECT` por defecto.

- **location** _cadena_

  La ubicación de Google Cloud que deseas utilizar para las llamadas a la API, por ejemplo, `us-central1`.
  Utiliza la variable de entorno `GOOGLE_VERTEX_LOCATION` por defecto.

- **googleAuthOptions** _objeto_

  Opcional. Las opciones de autenticación utilizadas por la [Biblioteca de Autenticación de Google](https://github.com/googleapis/google-auth-library-nodejs/). Consulta también la [GoogleAuthOptions](https://github.com/googleapis/google-auth-library-nodejs/blob/08978822e1b7b5961f0e355df51d738e012be392/src/auth/googleauth.ts)

# L87C18-L87C35) interfaz.

  - **authClient** _objeto_
    Un `AuthClient` para usar.

  - **keyFilename** _cadena_
    Ruta a un archivo de clave .json, .pem o .p12.

  - **keyFile** _cadena_
    Ruta a un archivo de clave .json, .pem o .p12.

  - **credentials** _objeto_
    Objeto que contiene las propiedades `client_email` y `private_key`, o las opciones de cliente de cuenta externa.

  - **clientOptions** _objeto_
    Objeto de opciones pasado al constructor del cliente.

  - **scopes** _cadena | cadena[]_
    Escopos requeridos para la solicitud de API deseada.

  - **projectId** _cadena_
    Tu ID de proyecto.

  - **universeDomain** _cadena_
    El dominio de servicio predeterminado para un universo de Cloud.

- **cabeceras** _Resolvable&lt;Registro&lt;cadena, cadena | indefinido&gt;&gt;_

  Cabeceras para incluir en las solicitudes. Pueden proporcionarse en múltiples formatos:

  - Un registro de pares clave-valor de cabecera: `Record<string, string | undefined>`
  - Una función que devuelve cabeceras: `() => Record<string, string | undefined>`
  - Una función asíncrona que devuelve cabeceras: `async () => Record<string, string | undefined>`
  - Una promesa que se resuelve en cabeceras: `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). 
  Por defecto utiliza la función global `fetch`. 
  Puedes utilizarla como middleware para interceptar solicitudes, 
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

<a id="google-vertex-anthropic-edge-runtime"></a>

#### Runtime de Edge

Los runtimes de Edge (como Vercel Edge Functions y Cloudflare Workers) son entornos de JavaScript ligeros que se ejecutan más cerca de los usuarios en la orilla de la red.
 Solo proporcionan un subconjunto de las APIs de Node.js estándar.
 Por ejemplo, el acceso directo al sistema de archivos no está disponible, y muchas bibliotecas de Node.js específicas (incluida la biblioteca de autenticación de Google estándar) no son compatibles.

 La versión de runtime de Edge del proveedor de Google Vertex Anthropic admite las [credenciales de aplicación predeterminadas de Google](https://github.com/googleapis/google-auth-library-nodejs?tab=readme-ov-file#application-default-credentials) a través de variables de entorno. Los valores se pueden obtener desde un archivo de credenciales JSON desde la [Consola de Google Cloud](https://console.cloud.google.com/apis/credentials).

 Para los runtimes de Edge, puedes importar la instancia del proveedor desde `@ai-sdk/google-vertex/anthropic/edge`:

```typescript
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic/edge';
```

 Para personalizar la configuración, utiliza `createVertexAnthropic` del mismo módulo:

```typescript
import { createVertexAnthropic } from '@ai-sdk/google-vertex/anthropic/edge';

const vertexAnthropic = createVertexAnthropic({
  proyecto: 'mi-proyecto', // opcional
  ubicación: 'us-central1', // opcional
});
```

 Para la autenticación de runtime de Edge, establece estas variables de entorno desde tu archivo JSON de credenciales de aplicación de Google por defecto:

- `GOOGLE_CLIENT_EMAIL`
- `GOOGLE_PRIVATE_KEY`
- `GOOGLE_PRIVATE_KEY_ID` (opcional)

##### Configuración de Proveedores Opcionales

Puedes utilizar las siguientes configuraciones opcionales para personalizar la instancia del proveedor:

- **proyecto** _cadena_

  El ID del proyecto de Google Cloud que deseas utilizar para las llamadas a la API.
  Utiliza la variable de entorno `GOOGLE_VERTEX_PROJECT` por defecto.

- **ubicación** _cadena_

  La ubicación de Google Cloud que deseas utilizar para las llamadas a la API, por ejemplo `us-central1`.
  Utiliza la variable de entorno `GOOGLE_VERTEX_LOCATION` por defecto.

- **googleCredentials** _objeto_

  Opcional. Las credenciales utilizadas por el proveedor Edge para la autenticación. Estas credenciales se establecen típicamente a través de variables de entorno y se derivan de un archivo JSON de cuenta de servicio.

  - **clientEmail** _cadena_
    El correo electrónico del cliente desde el archivo JSON de cuenta de servicio. Por defecto, utiliza el contenido de la variable de entorno `GOOGLE_CLIENT_EMAIL`.

  - **privateKey** _cadena_
    La clave privada desde el archivo JSON de cuenta de servicio. Por defecto, utiliza el contenido de la variable de entorno `GOOGLE_PRIVATE_KEY`.

  - **privateKeyId** _cadena_
    El ID de la clave privada desde el archivo JSON de cuenta de servicio (opcional). Por defecto, utiliza el contenido de la variable de entorno `GOOGLE_PRIVATE_KEY_ID`.

- **cabeceras** _Resolvable&lt;Registro&lt;cadena, cadena | indefinido&gt;&gt;_

  Cabeceras para incluir en las solicitudes. Pueden proporcionarse en múltiples formatos:

  - Un registro de pares clave-valor de cabecera: `Record<string, string | undefined>`
  - Una función que devuelve cabeceras: `() => Record<string, string | undefined>`
  - Una función asíncrona que devuelve cabeceras: `async () => Record<string, string | undefined>`
  - Una promesa que se resuelve en cabeceras: `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

### Modelos de Lenguaje

Puedes crear modelos que llamen a la [API de Mensajes de Anthropic](https://docs.anthropic.com/claude/reference/messages_post) utilizando la instancia del proveedor.
El primer argumento es el id del modelo, por ejemplo `claude-3-haiku-20240307`.
Algunos modelos tienen capacidades multi-modales.

```ts
const model = anthropic('claude-3-haiku-20240307');
```

Puedes utilizar modelos de lenguaje de Anthropic para generar texto con la función `generateText`:

```ts
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
import { generateText } from 'ai';

const { text } = await generateText({
  model: vertexAnthropic('claude-3-haiku-20240307'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Modelos de lenguaje de Anthropic también se pueden utilizar en las funciones `streamText`, `generateObject` y `streamObject` (ver [AI SDK Core](/docs/ai-sdk-core)).

<Nota>
  La API de Anthropic devuelve llamadas de herramientas de streaming todas a la vez después de un retardo. Esto causa que la función `streamObject` genere el objeto completamente después de un retardo
  en lugar de transmitirlo incrementalmente.
</Nota>

Los siguientes ajustes opcionales están disponibles para modelos de Anthropic:

- `sendReasoning` _boolean_

  Opcional. Incluye contenido de razonamiento en solicitudes enviadas al modelo. Por defecto es `true`.

  Si estás experimentando problemas con el modelo al manejar solicitudes que involucran contenido de razonamiento, puedes establecer esto en `false` para omitirlo de la solicitud.

### Razonamiento

Anthropic tiene soporte para razonamiento para el modelo `claude-3-7-sonnet@20250219`.

Puedes habilitarlo utilizando la opción `thinking` del proveedor y especificando un presupuesto de tokens.

```ts
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
import { generateText } from 'ai';

const { text, reasoning, reasoningDetails } = await generateText({
  model: vertexAnthropic('claude-3-7-sonnet@20250219'),
  prompt: '¿Cuántas personas vivirán en el mundo en 2040?',
  providerOptions: {
    anthropic: {
      thinking: { type: 'enabled', budgetTokens: 12000 },
    },
  },
});

console.log(reasoning); // texto de razonamiento
console.log(reasoningDetails); // detalles del razonamiento incluyendo razonamiento redactado
console.log(text); // respuesta de texto
```

Consulte [SDK de IA: UI de Chatbot](/docs/ai-sdk-ui/chatbot#razonamiento) para obtener más detalles sobre cómo integrar el razonamiento en tu chatbot.

#### Control de Cache

<Nota>
  El control de cache Anthropic está en un estado Pre-Disponible Generalmente (GA) en Google Vertex. Para más información, consulte la [documentación de control de cache de Anthropic de Google Vertex](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude-prompt-caching).
</Nota>

En los mensajes y partes de mensajes, puedes utilizar la propiedad `providerOptions` para establecer puntos de ruptura de control de cache.
Debes establecer la propiedad `anthropic` en el objeto `providerOptions` a `{ cacheControl: { type: 'ephemeral' } }` para establecer un punto de ruptura de control de cache.

Los tokens de creación de cache se devuelven en el objeto `providerMetadata` para `generateText` y `generateObject`, nuevamente bajo la propiedad `anthropic`.
Cuando utilices `streamText` o `streamObject`, la respuesta contiene una promesa que se resuelve en el metadatos. Alternativamente, puedes recibirlo en el callback `onFinish`.

```ts highlight="8,18-20,29-30"
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
import { generateText } from 'ai';

const errorMessage = '... mensaje de error largo ...';
```

```javascript
const resultado = await generarTexto({
  modelo: vertexAnthropic('claude-3-5-sonnet-20240620'),
  mensajes: [
    {
      rol: 'usuario',
      contenido: [
        { tipo: 'texto', texto: 'Eres un experto en JavaScript.' },
        {
          tipo: 'texto',
          texto: `Mensaje de error: ${errorMessage}`,
          opcionesDeProveedor: {
            antropico: { cacheControl: { tipo: 'transitorio' } },
          },
        },
        { tipo: 'texto', texto: 'Explica el mensaje de error.' },
      ],
    },
  ],
});

console.log(resultado.text);
console.log(resultado.providerMetadata?.anthropic);
// e.g. { cacheCreationInputTokens: 2118, cacheReadInputTokens: 0 }
```

También puedes utilizar el control de caché en mensajes del sistema proporcionando múltiples mensajes del sistema al principio de tu arreglo `mensajes`:

```ts highlight="3,9-11"
const resultado = await generarTexto({
  modelo: vertexAnthropic('claude-3-5-sonnet-20240620'),
  mensajes: [
    {
      rol: 'sistema',
      contenido: 'Mensaje de sistema almacenado en caché',
      opcionesDeProveedor: {
        antropico: { controlDeCaché: { tipo: 'transitorio' } },
      },
    },
    {
      rol: 'sistema',
      contenido: 'Mensaje de sistema no almacenado en caché',
    },
    {
      rol: 'usuario',
      contenido: 'Prompt del usuario',
    },
  ],
});
```

Para obtener más información sobre el caché de solicitudes con Anthropic, consulte la [documentación del caché de solicitudes de Google Vertex AI's Claude](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude-prompt-caching) y la [documentación de Control

### Uso de Computadora

Anthropic proporciona tres herramientas integradas que se pueden utilizar para interactuar con sistemas externos:

1. **Herramienta de Bash**: Permite ejecutar comandos de Bash.
2. **Herramienta de Editor de Texto**: Proporciona funcionalidad para visualizar y editar archivos de texto.
3. **Herramienta de Computadora**: Habilita el control de acciones de teclado y mouse en una computadora.

Están disponibles a través de la propiedad `tools` de la instancia del proveedor.

Para obtener más información, consulte la [documentación de Uso de Computadora de Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/computer-use).

#### Herramienta de Bash

La Herramienta de Bash permite ejecutar comandos de Bash. Aquí está cómo crear y utilizarla:

```ts
const bashTool = vertexAnthropic.tools.bash_20241022({
  execute: async ({ command, restart }) => {
    // Implemente la lógica de ejecución de comandos de Bash aquí
    // Devuelva el resultado de la ejecución del comando
  },
});
```

Parámetros:

- `command` (string): El comando de Bash a ejecutar. Requerido a menos que la herramienta esté siendo reiniciada.
- `restart` (boolean, opcional): Especificar verdadero reiniciará esta herramienta.

#### Herramienta de Editor de Texto

La Herramienta de Editor de Texto proporciona funcionalidad para visualizar y editar archivos de texto:

```ts
const textEditorTool = vertexAnthropic.tools.textEditor_20241022({
  execute: async ({
    command,
    path,
    file_text,
    insert_line,
    new_str,
    old_str,
    view_range,
  }) => {
    // Implementa la lógica de edición de texto aquí
    // Devuelve el resultado de la operación de edición de texto
  },
});
```

Parámetros:

- `command` ('view' | 'create' | 'str_replace' | 'insert' | 'undo_edit'): La orden a ejecutar.
- `path` (string): Ruta absoluta al archivo o directorio, por ejemplo `/repo/file.py` o `/repo`.
- `file_text` (string, opcional): Obligatorio para la orden `create`, con el contenido del archivo a crear.
- `insert_line` (number, opcional): Obligatorio para la orden `insert`. El número de línea después de la cual insertar la nueva cadena.
- `new_str` (string, opcional): Nueva cadena para las órdenes `str_replace` o `insert`.
- `old_str` (string, opcional): Obligatorio para la orden `str_replace`, que contiene la cadena a reemplazar.
- `view_range` (number[], opcional): Opcional para la orden `view` para especificar el rango de líneas a mostrar.

#### Herramienta de Computadora

La Herramienta de Computadora permite el control de acciones de teclado y mouse en una computadora:

```ts
const computerTool = vertexAnthropic.tools.computer_20241022({
  anchoDePantallaPx: 1920,
  altoDePantallaPx: 1080,
  numeroDePantalla: 0, // Opcional, para entornos X11

  ejecutar: async ({ acción, coordenada, texto }) => {
    // Implemente la lógica de control de la computadora aquí
    // Devuelva el resultado de la acción

    // Código de ejemplo:
    switch (acción) {
      case 'capturaDePantalla': {
        // resultado multipart:
        return {
          tipo: 'imagen',
          datos: fs
            .readFileSync('./data/screenshot-editor.png')
            .toString('base64'),
        };
      }
      default: {
        console.log('Acción:', acción);
        console.log('Coordenada:', coordenada);
        console.log('Texto:', texto);
        return `se ejecutó ${acción}`;
      }
    }
  },

  // mapa a contenido de resultado de herramienta para consumo de LLM:
  experimental_toToolResultContent(result) {
    return typeof result === 'string'
      ? [{ tipo: 'texto', texto: result }]
      : [{ tipo: 'imagen', datos: result.data, mimeType: 'image/png' }];
  },
});
```

Parámetros:

- `acción` ('key' | 'type' | 'mouse_move' | 'left_click' | 'left_click_drag' | 'right_click' | 'middle_click' | 'double_click' | 'screenshot' | 'cursor_position'): La acción a realizar.
- `coordenada` (number[], opcional): Requerido para las acciones `mouse_move` y `left_click_drag`. Especifica las coordenadas (x, y).
- `texto` (string, opcional): Requerido para las acciones `type` y `key`.

Estas herramientas pueden usarse en conjunto con el modelo `claude-3-5-sonnet-v2@20241022` para habilitar interacciones y tareas más complejas.

### Capacidad del Modelo

La lista más reciente de modelos de Anthropic en Vertex AI está disponible [aquí](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude#model-list).
Consulte también [Comparación

# Comparación de modelos).

| Modelo                           | Entrada de imagen         | Generación de objetos   | Uso de herramienta          | Transmisión de herramienta      | Uso de computadora        |
| ------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `claude-3-7-sonnet@20250219`    | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-5-sonnet-v2@20241022` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-5-sonnet@20240620`    | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-5-haiku@20241022`     | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-sonnet@20240229`      | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-haiku@20240307`       | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

| `claude-3-opus@20240229`        | <Ver size={18} /> | <Ver size={18} /> | <Ver size={18} /> | <Ver size={18} /> | <Cruz size={18} /> |

<Nota>
  La tabla anterior enumera modelos populares. También puedes pasar cualquier modelo ID de proveedor disponible como una cadena si es necesario.
</Nota>

---
titulo: Rev.ai
descripcion: Aprende a utilizar el proveedor Rev.ai para el SDK de IA.
---

# Proveedor de Rev.ai

El [proveedor de Rev.ai](https://www.rev.ai/) contiene soporte para modelos de lenguaje para la API de transcripción de Rev.ai.

## Configuración

El proveedor de Rev.ai está disponible en el módulo `@ai-sdk/revai`. Puede instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/revai" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/revai" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/revai" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `revai` desde `@ai-sdk/revai`:

```ts
import { revai } from '@ai-sdk/revai';
```

Si necesitas una configuración personalizada, puedes importar `createRevai` desde `@ai-sdk/revai` y crear una instancia de proveedor con tus ajustes:

```ts
import { createRevai } from '@ai-sdk/revai';

const revai = createRevai({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Rev.ai:

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, se utiliza la variable de entorno `REVAI_API_KEY`.

- **headers** _Registro&lt;cadena,cadena&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, se utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de Rev.ai](https://www.rev.ai/docs/api/transcription)
utilizando el método de fábrica `.transcription()`.

El primer argumento es el ID del modelo, por ejemplo `machine`.

```ts
const modelo = revai.transcription('machine');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, suministrar el idioma de entrada en formato ISO-639-1 (por ejemplo, `en`) puede mejorar el rendimiento de la transcripción si se conoce con anterioridad.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { revai } from '@ai-sdk/revai';
import { readFile } from 'fs/promises';

const resultado = await transcribe({
  modelo: revai.transcription('machine'),
  audio: await readFile('audio.mp3'),
  providerOptions: { revai: { idioma: 'es' } },
});
```

Las siguientes opciones del proveedor están disponibles:

- **metadata** _cadena_

  Opcional metadata que se proporcionó durante la solicitud de trabajo.

- **notification_config** _objeto_

  Configuración opcional para una URL de llamada para invocar cuando se complete el procesamiento.

  - **url** _cadena_ - URL de llamada para invocar cuando se complete el procesamiento.
  - **auth_headers** _objeto_ - Encabezados de autorización opcionales, si se necesitan para invocar la llamada.

- **delete_after_seconds** _entero_

  Cantidad de tiempo después de la finalización del trabajo cuando se elimina automáticamente el trabajo.

- **verbatim** _boolean_

  Configura al transcriptor para transcribir cada sílaba, incluyendo todos los comienzos falsos y disfluencias.

- **rush** _boolean_

  [No soportado por HIPAA] Solo disponible para la opción de transcriptor humano. Cuando se establece en true, se le da prioridad al trabajo.

- **skip_diarization** _boolean_

  Especifica si la diarización de hablantes se saltará por el motor de habla.

- **skip_postprocessing** _boolean_

  Solo disponible para los idiomas inglés y español. Preferencia del usuario sobre si saltar operaciones de post-procesamiento.

- **skip_punctuation** _boolean_

  Especifica si los elementos de tipo "punct" serán omitidos por el motor de voz.

- **remove_disfluencies** _boolean_

  Cuando se establece en true, las disfluencias (como 'ums' y 'uhs') no aparecerán en el transcripto.

- **remove_atmospherics** _boolean_

  Cuando se establece en true, los atmosféricos (como `<laugh>`, `<affirmative>`) no aparecerán en el transcripto.

- **filter_profanity** _boolean_

  Cuando está habilitado, las blasfemias se filtrarán reemplazando caracteres con asteriscos excepto los primeros y últimos.

- **speaker_channels_count** _integer_

  Solo disponible para los idiomas inglés, español y francés. Especifica el número total de canales de hablante únicos en el audio.

- **speakers_count** _integer_

  Solo disponible para los idiomas inglés, español y francés. Especifica el número total de hablantes únicos en el audio.

- **diarization_type** _string_

  Especifica el tipo de diarización. Posibles valores: "standard" (por defecto), "premium".

- **custom_vocabulary_id** _string_

  Proporciona la id de un vocabulario personalizado pre-completado enviado a través de la API de Vocabularios Personalizados.

- **custom_vocabularies** _Array_

  Especifica una colección de vocabularios personalizados para ser utilizados en este trabajo.

- **strict_custom_vocabulary** _boolean_

  Si es true, solo las frases exactas se utilizarán como vocabulario personalizado.

- **summarization_config** _object_

  Especifica las opciones de resumen.

  - **model** _string_ - Tipo de modelo para resumen. Posibles valores: "standard" (por defecto), "premium".
  - **type** _string_ - Tipo de formato de resumen. Posibles valores: "paragraph" (por defecto), "bullets".
  - **prompt** _string_ - Pregunta personalizada para resúmenes flexibles (mutuamente excluyente con type).

- **translation_config** _object_

  Especifica las opciones de traducción.

- **target_languages** _Array_ - Array de idiomas objetivo para la traducción.
  - **model** _string_ - Tipo de modelo para la traducción. Posibles valores: "standard" (por defecto), "premium".

- **language** _string_

  El idioma se proporciona como código de idioma ISO 639-1. Por defecto es "en".

- **forced_alignment** _boolean_

  Cuando está habilitado, proporciona una mayor precisión para los tiempos de marcaje por palabra para un transcripto.
  Por defecto es `false`.

  Idiomas soportados actualmente:

  - Inglés (en, en-us, en-gb)
  - Francés (fr)
  - Italiano (it)
  - Alemán (de)
  - Español (es)

  Nota: Esta opción no está disponible en entorno de bajo costo.

### Capabilidades del Modelo

| Modelo      | Transcripción       | Duración            | Segmentos            | Idioma            |
| ---------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `machine`  | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `human`    | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `low_cost` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `fusion`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titulo: Mistral AI
descripcion: Aprende a utilizar Mistral.
---

# Proveedor de Mistral AI

El [proveedor de Mistral AI](https://mistral.ai/) contiene soporte para modelos de lenguaje del API de chat de Mistral.

## Configuración

El proveedor de Mistral está disponible en el módulo `@ai-sdk/mistral`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/mistral" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/mistral" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/mistral" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `mistral` desde `@ai-sdk/mistral`:

```ts
import { mistral } from '@ai-sdk/mistral';
```

Si necesitas una configuración personalizada, puedes importar `createMistral` desde `@ai-sdk/mistral`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createMistral } from '@ai-sdk/mistral';

const mistral = createMistral({
  // ajustes personalizados
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor de Mistral:

- **baseURL** _cadena_

  Utiliza una dirección URL diferente para las llamadas a la API, por ejemplo, para utilizar servidores de proxy.
  La dirección URL predeterminada es `https://api.mistral.ai/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, se utiliza la variable de entorno `MISTRAL_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, se utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Lenguaje

Puedes crear modelos que llamen a la [API de chat de Mistral](https://docs.mistral.ai/api/

# operación/createChatCompletion) utilizando una instancia de proveedor.
El primer argumento es el ID del modelo, por ejemplo, `mistral-large-latest`.
Algunos modelos de chat de Mistral admiten llamadas a herramientas.

```ts
const model = mistral('mistral-large-latest');
```

Los modelos de chat de Mistral también admiten configuraciones de modelo adicionales que no forman parte de las [configuraciones de llamada estándar](/docs/ai-sdk-core/settings).
Puedes pasarlas como un argumento de opciones:

```ts
const model = mistral('mistral-large-latest', {
  safePrompt: true, // inyección de prompt de seguridad opcional
});
```

Las siguientes configuraciones opcionales están disponibles para los modelos de Mistral:

- **safePrompt** _boolean_

  Si se debe inyectar un prompt de seguridad antes de todas las conversaciones.

  Por defecto, `false`.

### Document OCR

Los modelos de chat de Mistral admiten OCR de documentos para archivos PDF.
Puedes establecer opciones de proveedor de forma opcional para limitar imágenes y páginas.

```ts
const result = await generateText({
  model: mistral('mistral-small-latest'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: '¿Cuál es el modelo de embedding según este documento?',
        },
        {
          type: 'file',
          data: new URL(
            'https://github.com/vercel/ai/blob/main/examples/ai-core/data/ai.pdf?raw=true',
          ),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
  // configuraciones opcionales:
  providerOptions: {
    mistral: {
      documentImageLimit: 8,
      documentPageLimit: 64,
    },
  },
});
```

### Ejemplo

Puedes utilizar modelos de lenguaje de Mistral para generar texto con la función `generateText`:

```ts
import { mistral } from '@ai-sdk/mistral';
import { generateText } from 'ai';

const { text } = await generateText({
  model: mistral('mistral-large-latest'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Mistral también se pueden utilizar en las funciones `streamText`, `generateObject`, y `streamObject` (consulte [AI SDK Core](/docs/ai-sdk-core)).

### Capacidad de Modelos

| Modelo                  | Entrada de Imagen         | Generación de Objetos   | Uso de Herramienta          | Streaming de Herramienta      |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `pixtral-large-latest` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistral-large-latest` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistral-small-latest` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `ministral-3b-latest`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `ministral-8b-latest`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `pixtral-12b-2409`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. Consulte la [documentación de Mistral](https://docs.mistral.ai/getting-started/models/models_overview/) para obtener una lista completa de modelos disponibles. La tabla anterior muestra modelos populares. También puede pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Modelos de Incorporación

Puede crear modelos que llamen a la [API de incorporación de Mistral](https://docs.mistral.ai/api/#operation/createEmbedding) utilizando el método de fábrica `.embedding()`.

```ts
const model = mistral.embedding('mistral-embed');
```

### Capabilidades del Modelo

| Modelo           | Dimensiones por Defecto |
| --------------- | ------------------ |
| `mistral-embed` | 1024               |

---
titulo: Together.ai
descripcion: Aprende a usar los modelos de Together.ai con el SDK de IA.
---

# Proveedor Together.ai

El [proveedor Together.ai](https://together.ai) contiene soporte para 200+ modelos de código abierto a través de la [API de Together.ai](https://docs.together.ai/reference).

## Configuración

El proveedor Together.ai está disponible a través del módulo `@ai-sdk/togetherai`. Puedes
instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/togetherai" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/togetherai" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/togetherai" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor predeterminada `togetherai` de `@ai-sdk/togetherai`:

```ts
import { togetherai } from '@ai-sdk/togetherai';
```

Si necesitas una configuración personalizada, puedes importar `createTogetherAI` de `@ai-sdk/togetherai`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createTogetherAI } from '@ai-sdk/togetherai';

const togetherai = createTogetherAI({
  apiKey: process.env.TOGETHER_AI_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor Together.ai:

- **baseURL** _cadena_

  Utiliza una dirección URL diferente para prefixar las llamadas a la API, por ejemplo, para utilizar servidores de proxy.
  La dirección URL predeterminada es `https://api.together.xyz/v1`.

- **apiKey** _cadena_

  Llave de API que se envía utilizando el encabezado `Authorization`. Por defecto, es la variable de entorno `TOGETHER_AI_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). Por defecto, es la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

## Modelos de Lenguaje

Puedes crear [modelos Together.ai](https://docs.together.ai/docs/serverless-models) utilizando una instancia de proveedor. El primer argumento es el identificador del modelo, por ejemplo `google/gemma-2-9b-it`.

```ts
const model = togetherai('google/gemma-2-9b-it');
```

### Modelos de Razonamiento

Together.ai expone el pensamiento de `deepseek-ai/DeepSeek-R1` en el texto generado utilizando la etiqueta `<think>`.
Puedes utilizar `extractReasoningMiddleware` para extraer este razonamiento y exponerlo como una propiedad `reasoning` en el resultado:

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const enhancedModel = wrapLanguageModel({
  model: togetherai('deepseek-ai/DeepSeek-R1'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Puedes utilizar ese modelo mejorado en funciones como `generateText` y `streamText`.

### Ejemplo

Puedes utilizar modelos de lenguaje de Together.ai para generar texto con la función `generateText`:

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: togetherai('meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Together.ai también se pueden utilizar en la función `streamText` (consulte [AI SDK Core](/docs/ai-sdk-core)).

El proveedor de Together.ai también admite [modelos de completación](https://docs.together.ai/docs/serverless-models#language-models) mediante (siguiendo el código de ejemplo anterior) `togetherai.completionModel()` y [modelos de embebedad](https://docs.together.ai/docs/serverless-models#embedding-models) mediante `togetherai.textEmbeddingModel()`.

## Capacidad del Modelo

| Modelo                                          | Entrada de Imagen         | Generación de Objetos   | Uso de Herramienta          | Streaming de Herramienta      |
| ---------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `meta-llama/Meta-Llama-3.3-70B-Instruct-Turbo` | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`  | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistralai/Mixtral-8x22B-Instruct-v0.1`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistralai/Mistral-7B-Instruct-v0.3`           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `deepseek-ai/DeepSeek-V3`                      | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `google/gemma-2b-it`                           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `Qwen/Qwen2.5-72B-Instruct-Turbo`              | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `databricks/dbrx-instruct`                     | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

---

# Introducción
La siguiente tabla muestra una comparación de las características de

<Nota>
  La tabla anterior muestra modelos populares. Consulte la documentación de
  [Together.ai](https://docs.together.ai/docs/serverless-models) para obtener
  una lista completa de modelos disponibles. También puede pasar cualquier ID de
  modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Modelos de Imágenes

Puedes crear modelos de imágenes de Together.ai utilizando el método de fábrica `.image()`.
Para más información sobre la generación de imágenes con el SDK de AI, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { experimental_generateImage as generateImage } from 'ai';

const { images } = await generateImage({
  model: togetherai.image('black-forest-labs/FLUX.1-dev'),
  prompt: 'Un quetzal resplandeciente delicioso en vuelo entre gotas de lluvia',
});
```

Puedes pasar parámetros de solicitud específicos del proveedor utilizando el argumento `providerOptions`.

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { experimental_generateImage as generateImage } from 'ai';

const { images } = await generateImage({
  model: togetherai.image('black-forest-labs/FLUX.1-dev'),
  prompt: 'Un quetzal resplandeciente delicioso en vuelo entre gotas de lluvia',
  size: '512x512',
  // Parámetros de solicitud adicionales específicos del proveedor (opcional)
  providerOptions: {
    togetherai: {
      steps: 40,
    },
  },
});
```

Para obtener una lista completa de opciones específicas del proveedor disponibles, consulta la [Referencia de la API de Generación de Imágenes de Together.ai](https://docs.together.ai/reference/post_images-generations).

### Capacidad del Modelo

Los modelos de imagen de Together.ai admiten varias dimensiones de imagen que varían según el modelo. Las tamaños comunes incluyen 512x512, 768x768 y 1024x1024, con algunos modelos que admiten hasta 1792x1792. El tamaño por defecto es 1024x1024.

| Modelos Disponibles                           |
| ------------------------------------------ |
| `stabilityai/stable-diffusion-xl-base-1.0` |
| `black-forest-labs/FLUX.1-dev`             |
| `black-forest-labs/FLUX.1-dev-lora`        |
| `black-forest-labs/FLUX.1-schnell`         |
| `black-forest-labs/FLUX.1-canny`           |
| `black-forest-labs/FLUX.1-depth`           |
| `black-forest-labs/FLUX.1-redux`           |
| `black-forest-labs/FLUX.1.1-pro`           |
| `black-forest-labs/FLUX.1-pro`             |
| `black-forest-labs/FLUX.1-schnell-Free`    |

<Nota>
  Por favor, consulte la [página de modelos de Together.ai](https://docs.together.ai/docs/serverless-models#image-models) para obtener una lista completa de modelos de imagen disponibles y sus capacidades.
</Nota>

---
titulo: Cohere
descripcion: Aprende a utilizar el proveedor Cohere para el SDK de IA.
---

# Proveedor Cohere

El [proveedor Cohere](https://cohere.com/) contiene soporte para modelos de

## Configuración

El proveedor de Cohere está disponible en el módulo `@ai-sdk/cohere`. Puede instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/cohere" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/cohere" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/cohere" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `cohere` desde `@ai-sdk/cohere`:

```ts
import { cohere } from '@ai-sdk/cohere';
```

Si necesitas una configuración personalizada, puedes importar `createCohere` desde `@ai-sdk/cohere`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createCohere } from '@ai-sdk/cohere';

const cohere = createCohere({
  // ajustes personalizados
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Cohere:

- **baseURL** _cadena_

  Utiliza una diferente URL prefix para las llamadas a API, por ejemplo, para utilizar servidores proxy.
  La URL predeterminada es `https://api.cohere.com/v2`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, se utiliza la variable de entorno `COHERE_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, se utiliza la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación personalizada de fetch para e.g. pruebas.

## Modelos de Lenguaje

Puedes crear modelos que llamen a la [API de chat de Cohere](https://docs.cohere.com/v2/docs/chat-api) utilizando una instancia de proveedor.
La primera argumento es el identificador del modelo, por ejemplo, `command-r-plus`.
Algunos modelos de chat de Cohere admiten llamadas a herramientas.

```ts
const model = cohere('command-r-plus');
```

### Ejemplo

Puedes utilizar modelos de lenguaje de Cohere para generar texto con la función `generateText`:

```ts
import { cohere } from '@ai-sdk/cohere';
import { generateText } from 'ai';

const { text } = await generateText({
  model: cohere('command-r-plus'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Cohere también pueden utilizarse en las funciones `streamText`, `generateObject` y `streamObject` (consulte [AI SDK Core](/docs/ai-sdk-core).

### Capabilidades del Modelo

| Modelo               | Entrada de Imagen         | Generación de Objetos   | Uso de Herramientas          | Transmisión de Herramientas      |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `command-a-03-2025` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `command-r-plus`    | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `command-r`         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `command-a-03-2025` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `command`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `command-light`     | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  La tabla anterior muestra modelos populares. Consulte los [docs de Cohere](https://docs.cohere.com/v2/docs/models#command) para obtener una lista completa de modelos disponibles. También puede pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

## Incorporando Modelos

Puedes crear modelos que llamen a la [API de embeber de Cohere](https://docs.cohere.com/v2/reference/embed) utilizando el método de fábrica `.embedding()`.

```ts
const modelo = cohere.embedding('embed-english-v3.0');
```

Los modelos de embeber de Cohere admiten ajustes adicionales. Puedes pasarlos como un argumento de opciones:

```ts
const modelo = cohere.embedding('embed-english-v3.0', {
  inputType: 'search_document',
});
```

Los ajustes opcionales disponibles para los modelos de embeber de Cohere son:

- **inputType** _'search_document' | 'search_query' | 'classification' | 'clustering'_

  Especifica el tipo de entrada pasada al modelo. El valor por defecto es `search_query`.

  - `search_document`: Utilizado para embeber almacenados en una base de datos de vectores para casos de uso de búsqueda.
  - `search_query`: Utilizado para embeber de consultas de búsqueda ejecutadas contra una base de datos de vectores para encontrar documentos relevantes.
  - `classification`: Utilizado para embeber pasados a través de un clasificador de texto.
  - `clustering`: Utilizado para embeber ejecutados a través de un algoritmo de agrupamiento.

- **truncate** _'NONE' | 'START' | 'END'_

  Especifica cómo la API manejará las entradas más largas que la longitud máxima de token de entrada.
  El valor por defecto es `END`.

  - `NONE`: Si seleccionado, cuando la entrada excede la longitud máxima de token de entrada, devolverá un error.
  - `START`: Descartará el comienzo de la entrada hasta que el resto de la entrada sea exactamente la longitud máxima de token de entrada para el modelo.
  - `END`: Descartará el final de la entrada hasta que el resto de la entrada sea exactamente la longitud máxima de token de entrada para el modelo.

### Capacidad del Modelo

| Modelo                           | Dimensiones de la Capa de Representación |
| ------------------------------- | -------------------- |
| `embed-english-v3.0`            | 1024                 |
| `embed-multilingual-v3.0`       | 1024                 |
| `embed-english-light-v3.0`      | 384                  |
| `embed-multilingual-light-v3.0` | 384                  |
| `embed-english-v2.0`            | 4096                 |
| `embed-english-light-v2.0`      | 1024                 |
| `embed-multilingual-v2.0`       | 768                  |

---
titulo: Fireworks
descripcion: Aprende a utilizar los modelos Fireworks con la SDK de IA.
---

# Proveedor de Fireworks

[Fireworks](https://fireworks.ai/) es una plataforma para ejecutar y probar LLMs a través de su [API](https://readme.fireworks.ai/).

## Configuración

El proveedor de Fireworks está disponible a través del módulo `@ai-sdk/fireworks`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/fireworks" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/fireworks" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/fireworks" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `fireworks` de `@ai-sdk/fireworks`:

```ts
import { fireworks } from '@ai-sdk/fireworks';
```

Si necesitas una configuración personalizada, puedes importar `createFireworks` de `@ai-sdk/fireworks`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createFireworks } from '@ai-sdk/fireworks';

const fireworks = createFireworks({
  apiKey: process.env.FIREWORKS_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor de Fireworks:

- **baseURL** _cadena_

  Utiliza una dirección URL diferente para prefixar las llamadas a la API, por ejemplo, para utilizar servidores proxy.
  La dirección URL predeterminada es `https://api.fireworks.ai/inference/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`. Por defecto es la variable de entorno `FIREWORKS_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modelos de Lenguaje

Puedes crear [modelos de Fireworks](https://fireworks.ai/models) utilizando una instancia de proveedor.
El primer argumento es el id del modelo, por ejemplo `accounts/fireworks/models/firefunction-v1`:

```ts
const model = fireworks('accounts/fireworks/models/firefunction-v1');
```

### Modelos de Razonamiento

Fireworks expone el pensamiento de `deepseek-r1` en el texto generado utilizando la etiqueta `<think>`.
Puedes utilizar el `extractReasoningMiddleware` para extraer este razonamiento y exponerlo como una propiedad `reasoning` en el resultado:

```ts
import { fireworks } from '@ai-sdk/fireworks';
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const enhancedModel = wrapLanguageModel({
  model: fireworks('accounts/fireworks/models/deepseek-r1'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Puedes utilizar ese modelo mejorado en funciones como `generateText` y `streamText`.

### Ejemplo

Puedes utilizar modelos de lenguaje de Fireworks para generar texto con la función `generateText`:

```ts
import { fireworks } from '@ai-sdk/fireworks';
import { generateText } from 'ai';

const { text } = await generateText({
  model: fireworks('accounts/fireworks/models/firefunction-v1'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Fireworks también se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

### Modelos de Completación

Puedes crear modelos que llamen a la API de completación de Fireworks utilizando el método de fábrica `.completion()`:

```ts
const model = fireworks.completion('accounts/fireworks/models/firefunction-v1');
```

### Capacidad del Modelo

### Introdu

| Modelo                                                     | Entrada de imagen          | Generación de objetos | Uso de herramienta          | Streaming de herramienta      |
| ---------------------------------------------------------- | --------------------------- | ----------------------- | --------------------------- | --------------------------- |
| `accounts/fireworks/models/deepseek-r1`                     | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/deepseek-v3`                     | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p1-405b-instruct`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `accounts/fireworks/models/llama-v3p1-8b-instruct`          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p2-3b-instruct`          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p3-70b-instruct`         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

| `accounts/fireworks/models/mixtral-8x7b-instruct-hf`       | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/mixtral-8x22b-instruct`         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/qwen2p5-coder-32b-instruct`     | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p2-11b-vision-instruct` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/yi-large`                       | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

<Nota>
  La tabla anterior enumera modelos populares. Consulte la [página de modelos de Fireworks](https://fireworks.ai/models) para obtener una lista completa de modelos disponibles.
</Nota>

## Inserción de Modelos

Puedes crear modelos que llamen a la API de embeddings de Fireworks utilizando el método de fábrica `.textEmbeddingModel()`:

```ts
const model = fireworks.textEmbeddingModel(
  'accounts/fireworks/models/nomic-embed-text-v1',
);
```

## Modelos de Imágenes

Puedes crear modelos de imágenes de Fireworks utilizando el método de fábrica `.image()`.
Para obtener más información sobre la generación de imágenes con el SDK de AI, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { fireworks } from '@ai-sdk/fireworks';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: fireworks.image('accounts/fireworks/models/flux-1-dev-fp8'),
  prompt: 'Una ciudad futurista al atardecer',
  aspectRatio: '16:9',
});
```

<Nota>
  El soporte de modelos para los parámetros `size` y `aspectRatio` varía. Consulta la sección [Capacidades de Modelo](#model-capabilities-1) a continuación para obtener las dimensiones admitidas, o revisa la documentación del modelo en la [página de modelos de Fireworks](https://fireworks.ai/models) para obtener más detalles.
</Nota>

### Capacidad del Modelo

Para todos los modelos que admiten ratios de aspecto, los siguientes ratios de aspecto están soportados:

`1:1 (predeterminado), 2:3, 3:2, 4:5, 5:4, 16:9, 9:16, 9:21, 21:9`

Para todos los modelos que admiten tamaño, los siguientes tamaños están soportados:

`640 x 1536, 768 x 1344, 832 x 1216, 896 x 1152, 1024x1024 (predeterminado), 1152 x 896, 1216 x 832, 1344 x 768, 1536 x 640`

| Modelo                                                        | Especificación de Dimensiones |
| ------------------------------------------------------------ | ------------------------ |
| `accounts/fireworks/models/flux-1-dev-fp8`                   | Relación de Aspecto             |
| `accounts/fireworks/models/flux-1-schnell-fp8`               | Relación de Aspecto             |
| `accounts/fireworks/models/playground-v2-5-1024px-aesthetic` | Tamaño                     |
| `accounts/fireworks/models/japanese-stable-diffusion-xl`     | Tamaño                     |
| `accounts/fireworks/models/playground-v2-1024px-aesthetic`   | Tamaño                     |
| `accounts/fireworks/models/SSD-1B`                           | Tamaño                     |
| `accounts/fireworks/models/stable-diffusion-xl-102

#### Estabilidad de los Modelos AI

Fireworks presenta varios modelos de Stability AI respaldados por claves de API y puntos finales de Stability AI. El proveedor de SDK AI de Fireworks no incluye actualmente soporte para estos modelos:

| Identificador del Modelo                               |
| -------------------------------------- |
| `accounts/stability/models/sd3-turbo`  |
| `accounts/stability/models/sd3-medium` |
| `accounts/stability/models/sd3`        |

---
titulo: DeepSeek
descripcion: Aprende a utilizar los modelos de DeepSeek con el SDK AI.
---

# Proveedor de DeepSeek

El [proveedor de DeepSeek](https://www.deepseek.com) ofrece acceso a modelos de lenguaje poderosos a través de la API de DeepSeek, incluyendo su modelo [DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3).

Las claves de API se pueden obtener desde la [Plataforma de DeepSeek](https://platform.deepseek.com/api_keys).

## Configuración

El proveedor de DeepSeek está disponible a través del módulo `@ai-sdk/deepseek`. Puedes instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/deepseek" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/deepseek" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/deepseek" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor por defecto `deepseek` desde `@ai-sdk/deepseek`:

```ts
import { deepseek } from '@ai-sdk/deepseek';
```

Para una configuración personalizada, puedes importar `createDeepSeek` y crear una instancia de proveedor con tus ajustes:

```ts
import { createDeepSeek } from '@ai-sdk/deepseek';

const deepseek = createDeepSeek({
  apiKey: process.env.DEEPSEEK_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor DeepSeek:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para las llamadas a API.
  El prefijo predeterminado es `https://api.deepseek.com/v1`.

- **apiKey** _cadena_

  Llave de API que se envía utilizando el encabezado `Authorization`. Por defecto es la variable de entorno `DEEPSEEK_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modelos de Lenguaje

Puedes crear modelos de lenguaje utilizando una instancia de proveedor:

```ts
import { deepseek } from '@ai-sdk/deepseek';
import { generateText } from 'ai';

const { text } = await generateText({
  model: deepseek('deepseek-chat'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje DeepSeek se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

### Razonamiento

DeepSeek tiene soporte de razonamiento para el modelo `deepseek-reasoner`:

```ts
import { deepseek } from '@ai-sdk/deepseek';
import { generateText } from 'ai';

const { texto, razonamiento } = await generateText({
  modelo: deepseek('deepseek-reasoner'),
  prompt: '¿Cuántas personas vivirán en el mundo en 2040?',
});

console.log(razonamiento);
console.log(texto);
```

Consulte [SDK de IA UI: Chatbot](/docs/ai-sdk-ui/chatbot#razonamiento) para obtener más detalles sobre cómo integrar el razonamiento en tu chatbot.

### Uso de tokens de caché

DeepSeek proporciona tecnología de caché de contexto en disco que puede reducir significativamente los costos de tokens para contenido repetido. Puedes acceder a las métricas de caché hit/miss a través de la propiedad `providerMetadata` en la respuesta:

```ts
import { deepseek } from '@ai-sdk/deepseek';
import { generateText } from 'ai';

const resultado = await generateText({
  modelo: deepseek('deepseek-chat'),
  prompt: 'Tu prompt aquí',
});

console.log(resultado.providerMetadata);
// Salida de ejemplo: { deepseek: { promptCacheHitTokens: 1856, promptCacheMissTokens: 5 } }
```

Las métricas incluyen:

- `promptCacheHitTokens`: Número de tokens de entrada que se almacenaron en caché
- `promptCacheMissTokens`: Número de tokens de entrada que no se almacenaron en caché

<Nota>
  Para obtener más detalles sobre el sistema de caché de DeepSeek, consulte la [documentación de caché de DeepSeek](https://api-docs.deepseek.com/guides/kv_cache#checking-cache-hit-status).
</Nota>

## Capacidad del Modelo

| Modelo               | Generación de Texto     | Generación de Objetos   | Entrada de Imagen         | Uso de Herramienta          | Streaming de Herramienta      |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `deepseek-chat`     | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `deepseek-reasoner` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  Consulte los [documentos de DeepSeek](https://api-docs.deepseek.com) para obtener una lista completa
  de modelos disponibles. También puede pasar cualquier ID de modelo de proveedor disponible como una cadena si es necesario.
</Nota>

---
titulo: Cerebras
descripcion: Aprenda a utilizar los modelos de Cerebras con la SDK de Inteligencia Artificial.
---

# Proveedor de Cerebras

El [proveedor de Cerebras](https://cerebras.ai) ofrece acceso a modelos de lenguaje poderosos a través de la API de Cerebras, incluyendo sus capacidades de inferencia de alta velocidad impulsadas por motores de escala de lámina y sistemas CS-3.

Las claves de API se pueden obtener desde la [Plataforma de Cerebras](https://cloud.cerebras.ai).

## Configuración

El proveedor de Cerebras está disponible a través del módulo `@ai-sdk/cerebras`. Puedes instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/cerebras" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/cerebras" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/cerebras" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor por defecto `cerebras` desde `@ai-sdk/cerebras`:

```ts
import { cerebras } from '@ai-sdk/cerebras';
```

Para configuraciones personalizadas, puedes importar `createCerebras` y crear una instancia de proveedor con tus ajustes:

```ts
import { createCerebras } from '@ai-sdk/cerebras';

const cerebras = createCerebras({
  apiKey: process.env.CEREBRAS_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor de Cerebras:

- **baseURL** _cadena_

  Utiliza una dirección URL diferente para prefixar llamadas a API.
  La dirección URL predeterminada es `https://api.cerebras.ai/v1`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`. Por defecto, es la variable de entorno `CEREBRAS_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modelos de Lenguaje

Puedes crear modelos de lenguaje utilizando una instancia de proveedor:

```ts
import { cerebras } from '@ai-sdk/cerebras';
import { generateText } from 'ai';

const { text } = await generateText({
  model: cerebras('llama3.1-8b'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

Los modelos de lenguaje de Cerebras se pueden utilizar en la función `streamText` (ver [AI SDK Core](/docs/ai-sdk-core)).

## Capabilidades del Modelo

| Modelo          | Entrada de Imagen         | Generación de Objetos   | Uso de Herramientas          | Transmisión de Herramientas      |
| -------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `llama3.1-8b`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama3.1-70b` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama3.3-70b` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Nota>
  Consulte los [docs de Cerebras](https://inference-docs.cerebras.ai/introducción) para obtener más detalles sobre los modelos disponibles. Tenga en cuenta que las ventanas de contexto están limitadas temporalmente a 8192 tokens en la Tarifa Gratuita.
</Nota>

---
titulo: Replicar
descripcion: Aprenda a utilizar modelos de Replicar con el SDK de AI.
---

# Proveedor de Replicar

[Replicar](https://replicate.com/) es una plataforma para ejecutar modelos de AI de código abierto. Es una elección popular para ejecutar modelos de generación de imágenes.

## Configuración

El proveedor de Replicar está disponible a través del módulo `@ai-sdk/replicate`. Puede instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add ai @ai-sdk/replicate" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install ai @ai-sdk/replicate" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add ai @ai-sdk/replicate" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `replicate` desde `@ai-sdk/replicate`:

```ts
import { replicate } from '@ai-sdk/replicate';
```

Si necesitas una configuración personalizada, puedes importar `createReplicate` desde `@ai-sdk/replicate`
y crear una instancia de proveedor con tus ajustes:

```ts
import { createReplicate } from '@ai-sdk/replicate';

const replicate = createReplicate({
  apiToken: process.env.REPLICATE_API_TOKEN ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Replicate:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para llamadas a la API, por ejemplo, para utilizar servidores proxy.
  El prefijo predeterminado es `https://api.replicate.com/v1`.

- **apiToken** _cadena_

  Token de API que se envía utilizando el encabezado `Authorization`. Por defecto, es el valor de la variable de entorno `REPLICATE_API_TOKEN`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modelos de Imágenes

Puedes crear modelos de imágenes de Replicate utilizando el método de fábrica `.image()`.
Para más información sobre la generación de imágenes con el SDK de IA, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

<Nota>
  El soporte de modelos para `size` y otros parámetros varía según el modelo. Consulta la documentación del modelo en [Replicate](https://replicate.com/explore) para obtener opciones admitidas y parámetros adicionales que se pueden pasar mediante `providerOptions.replicate`.
</Nota>

### Modelos de Imágenes Soportados

Los siguientes modelos de imágenes están actualmente soportados por el proveedor Replicate:

- [black-forest-labs/flux-1.1-pro-ultra](https://replicate.com/black-forest-labs/flux-1.1-pro-ultra)
- [black-forest-labs/flux-1.1-pro](https://replicate.com/black-forest-labs/flux-1.1-pro)
- [black-forest-labs/

- [stability-ai

Puedes utilizar también [modelos versionados](https://replicate.com/docs/topics/models/versions).
El id para modelos versionados es el id del modelo de Replicate seguido de un punto y coma y el id de la versión (`$modelId:$versionId`), por ejemplo:
`bytedance/sdxl-lightning-4step:5599ed30703defd

### Uso Básico

```ts
import { replicate } from '@ai-sdk/replicate';
import { experimental_generateImage as generateImage } from 'ai';
import { writeFile } from 'node:fs/promises';

const { image } = await generateImage({
  model: replicate.image('black-forest-labs/flux-schnell'),
  prompt: 'El monstruo del lago Ness haciendo una manicura',
  aspectRatio: '16:9',
});

await writeFile('image.webp', image.uint8Array);

console.log('La imagen se ha guardado como image.webp');
```

### Opciones específicas del modelo

```ts highlight="9-11"
import { replicate } from '@ai-sdk/replicate';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: replicate.image('recraft-ai/recraft-v3'),
  prompt: 'El monstruo del lago Ness haciendo una manicura',
  size: '1365x1024',
  providerOptions: {
    replicate: {
      style: 'imagen realista',
    },
  },
});
```

### Modelos versionados

```ts
import { replicate } from '@ai-sdk/replicate';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: replicate.image(
    'bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637',
  ),
  prompt: 'El monstruo del lago Ness haciendo una manicura',
});
```

Para obtener más detalles, consulte la [página de modelos de Replicate](https://replicate.com/explore).

---
title: Perplexidad
description: Aprende a utilizar la API Sonar de Perplexity con el SDK de AI.
---

# Proveedor de Perplexidad

El [Proveedor de Perplexidad](https://sonar.perplexity.ai) ofrece acceso a la API Sonar - un modelo de lenguaje que combina de manera única la búsqueda en tiempo real en la web con el procesamiento de lenguaje natural. Cada respuesta se basa en datos web actuales y incluye citas detalladas, lo que lo hace ideal para la investigación, la verificación de hechos y la obtención de información actualizada.

Las claves de API se pueden obtener desde la [Plataforma de Perplexidad](https://docs.perplexity.ai).

## Configuración

El proveedor de Perplexidad está disponible a través del módulo `@ai-sdk/perplexity`. Puede instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/perplexity" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/perplexity" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/perplexity" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor predeterminada `perplexity` desde `@ai-sdk/perplexity`:

```ts
import { perplexity } from '@ai-sdk/perplexity';
```

Para una configuración personalizada, puedes importar `createPerplexity` y crear una instancia de proveedor con tus ajustes:

```ts
import { createPerplexity } from '@ai-sdk/perplexity';

const perplexity = createPerplexity({
  apiKey: process.env.PERPLEXITY_API_KEY ?? '',
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Perplexity:

- **baseURL** _cadena_

  Utiliza un prefijo de URL diferente para las llamadas a API.
  El prefijo predeterminado es `https://api.perplexity.ai`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`. Por defecto es
  la variable de entorno `PERPLEXITY_API_KEY`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modelos de Lenguaje

Puedes crear modelos Perplexity utilizando una instancia de proveedor:

```ts
import { perplexity } from '@ai-sdk/perplexity';
import { generateText } from 'ai';

const { text } = await generateText({
  model: perplexity('sonar-pro'),
  prompt: '¿Cuáles son los últimos avances en la computación cuántica?',
});
```

### Fuentes

Los sitios web utilizados para generar la respuesta se incluyen en la propiedad `sources` del resultado:

```ts
import { perplexity } from '@ai-sdk/perplexity';
import { generateText } from 'ai';

const { text, sources } = await generateText({
  model: perplexity('sonar-pro'),
  prompt: '¿Cuáles son los últimos avances en la computación cuántica?',
});

console.log(sources);
```

### Opciones del Proveedor & Metadatos

El proveedor Perplexity incluye metadatos adicionales en la respuesta a través de `providerMetadata`.
Otras opciones de configuración están disponibles a través de `providerOptions`.

```ts
const resultado = await generarTexto({
  modelo: perplexity('sonar-pro'),
  prompt: '¿Cuáles son los últimos avances en la computación cuántica?',
  opcionesDelProveedor: {
    perplexity: {
      return_images: true, // Habilitar respuestas de imágenes (solo usuarios Tier-2 de Perplexity)
    },
  },
});

console.log(resultado.providerMetadata);
// Salida de ejemplo:
// {
//   perplexity: {
//     uso: { citationTokens: 5286, numSearchQueries: 1 },
//     imágenes: [
//       { imageUrl: "https://ejemplo.com/imagen1.jpg", originUrl: "https://otro-lado.com/pagina1", height: 1280, width: 720 },
//       { imageUrl: "https://ejemplo.com/imagen2.jpg", originUrl: "https://otro-lado.com/pagina2", height: 1280, width: 720 }
//     ]
//   },
// }
```

Los metadatos incluyen:

- `uso`: Objeto que contiene las métricas `citationTokens` y `numSearchQueries`
- `imágenes`: Arreglo de URLs de imágenes cuando `return_images` está habilitado (solo usuarios Tier-2 y superiores)

Puede habilitar respuestas de imágenes estableciendo `return_images: true` en las opciones del proveedor. Esta característica solo está disponible para usuarios de Perplexity Tier-2 y superiores.

<Nota>
  Para obtener más detalles sobre las capacidades de Perplexity, consulte la [documentación de completación de chat de Perplexity](https://docs.perplexity.ai/api-reference/chat-completions).
</Nota>

## Capabilidades del Modelo

| Modelo                 | Entrada de Imagen         | Generación de Objetos   | Uso de Herramientas          | Streaming de Herramientas      |
| --------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `sonar-pro`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `sonar`               | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `sonar-deep-research` | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Nota>
  Por favor, consulte la [documentación de Perplexity](https://docs.perplexity.ai) para obtener la documentación de la API detallada y las últimas actualizaciones.
</Nota>

---
titulo: Luma
descripcion: Aprende a utilizar los modelos de Luma AI con el SDK de AI.
---

# Proveedor de Luma

[Luma AI](https://lumalabs.ai/) proporciona modelos de generación de imágenes de alta calidad a través de su plataforma Dream Machine. Sus modelos ofrecen una generación de imágenes ultra alta calidad con una comprensión de promesas superior y capacidades únicas como la consistencia de caracteres y el soporte para referencias de imágenes múltiples.

## Configuración

El proveedor Luma está disponible a través del módulo `@ai-sdk/luma`. Puede instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/luma" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/luma" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/luma" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Puedes importar la instancia de proveedor por defecto `luma` desde `@ai-sdk/luma`:

```ts
import { luma } from '@ai-sdk/luma';
```

Si necesitas una configuración personalizada, puedes importar `createLuma` y crear una instancia de proveedor con tus ajustes:

```ts
import { createLuma } from '@ai-sdk/luma';

const luma = createLuma({
  apiKey: 'tu-api-key', // opcional, por defecto utiliza la variable de entorno LUMA_API_KEY
  baseURL: 'url-customizada', // opcional
  headers: {
    /* encabezados personalizados */
  }, // opcional
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia del proveedor Luma:

- **baseURL** _cadena_

  Utiliza una URL de prefijo diferente para las llamadas a la API, por ejemplo, para utilizar servidores proxy.
  El prefijo predeterminado es `https://api.lumalabs.ai`.

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, utiliza la variable de entorno `LUMA_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Puedes utilizarla como middleware para interceptar solicitudes,
  o proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Imágenes

Puedes crear modelos de imágenes de Luma utilizando el método de fabricación `.image()`.
Para más información sobre la generación de imágenes con el SDK de AI, consulta [generateImage()](/docs/reference/ai-sdk-core/generate-image).

### Uso Básico

```ts
import { luma } from '@ai-sdk/luma';
import { experimental_generateImage as generateImage } from 'ai';
import fs from 'fs';

const { image } = await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Un paisaje montañoso sereno a la puesta del sol',
  aspectRatio: '16:9',
});

const filename = `image-${Date.now()}.png`;
fs.writeFileSync(filename, image.uint8Array);
console.log(`La imagen se ha guardado en ${filename}`);
```

### Configuración de Modelos de Imágenes

Al crear un modelo de imagen, puedes personalizar el comportamiento de generación con ajustes opcionales:

```ts
const model = luma.image('photon-1', {
  maxImagesPerCall: 1, // Número máximo de imágenes generadas por llamada a la API
  pollIntervalMillis: 5000, // Frecuencia con la que se comprueba el estado de las imágenes (en ms)
  maxPollAttempts: 10, // Número máximo de intentos de comprobación antes de timeout
});
```

Dado que Luma procesa imágenes mediante un sistema de cola asincrónica, estos ajustes te permiten configurar el comportamiento de comprobación:

- **maxImagesPerCall** _number_

  Sobreescribe el número máximo de imágenes generadas por llamada a la API. Por defecto es 1.

- **pollIntervalMillis** _number_

  Controla con qué frecuencia se comprueba el estado de las imágenes mientras se están procesando. Por defecto es 500ms.

- **maxPollAttempts** _number_

  Limita el tiempo de espera por resultados antes de timeout, ya que la generación de imágenes se realiza de manera asincrónica. Por defecto es 120 intentos.

### Capabilidades del Modelo

Luma ofrece dos modelos principales:

| Modelo            | Descripción                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `photon-1`       | Generación de imágenes de alta calidad con comprensión superior de la solicitud |
| `photon-flash-1` | Generación más rápida optimizada para velocidad mientras se mantiene la calidad  |

Ambos modelos admiten las siguientes relaciones de aspecto:

- 1:1
- 3:4
- 4:3
- 9:16
- 16:9 (por defecto)
- 9:21
- 21:9

Para obtener más detalles sobre las relaciones de aspecto admitidas, consulte la [documentación de generación de imágenes de Luma](https://docs.lumalabs.ai/docs/image-generation).

Las características clave de los modelos de Luma incluyen:

- Generación de imágenes de alta calidad ultra alta
- Eficiencia de costos 10 veces superior en comparación con modelos similares
- Comprensión y adherencia de la solicitud superior
- Capacidad de consistencia de caracteres única desde imágenes de referencia únicas
- Soporte de múltiples imágenes de referencia para un ajuste de estilo preciso

#### Referencia de Imagen

Utilice hasta 4 imágenes de referencia para guiar su generación. Útil para crear variaciones o visualizar conceptos complejos. Ajuste el `peso` (0-1) para controlar la influencia de las imágenes de referencia.

```ts
// Ejemplo: Generar un salamándeo con referencia
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Un salamándeo a la puesta del sol en un estanque de bosque, en el estilo de ukiyo-e',
  providerOptions: {
    luma: {
      image_ref: [
        {
          url: 'https://example.com/reference.jpg',
          weight: 0.85,
        },
      ],
    },
  },
});
```

#### Referencia de Estilo

Aplicar estilos visuales específicos a sus generaciones utilizando imágenes de referencia. Controlar la influencia del estilo utilizando el parámetro `peso`.

```ts
// Ejemplo: Generar con referencia de estilo
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Un gato persa de pelo azul crema lanzando su sitio web en Vercel',
  providerOptions: {
    luma: {
      style_ref: [
        {
          url: 'https://example.com/style.jpg',
          weight: 0.8,
        },
      ],
    },
  },
});
```

#### Referencia de Caracteres

Crea caracteres consistentes y personalizados utilizando hasta 4 imágenes de referencia de la misma materia. Más imágenes de referencia mejoran la representación del carácter.

```ts
// Ejemplo: Generar imagen basada en el carácter
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Una mujer con un gato montando una escoba en un bosque',
  providerOptions: {
    luma: {
      character_ref: {
        identity0: {
          images: ['https://example.com/character.jpg'],
        },
      },
    },
  },
});
```

#### Modificar Imagen

Transforma imágenes existentes utilizando promesas de texto. Utiliza el parámetro `weight` para controlar hasta qué punto el resultado se ajusta a la imagen de entrada (peso más alto = más cercano a la entrada pero menos creativo).

<Nota>
  Para cambios de color, se recomienda utilizar un valor de peso más bajo (0.0-0.1).
</Nota>

```ts
// Ejemplo: Modificar imagen existente
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'transformar la bicicleta en un barco',
  providerOptions: {
    luma: {
      modify_image_ref: {
        url: 'https://example.com/image.jpg',
        weight: 1.0,
      },
    },
  },
});
```

Para obtener más detalles sobre las capacidades y características de Luma, visita la [documentación de generación de imágenes de Luma](https://docs.lumalabs.ai/docs/image-generation).

---
title: ElevenLabs
description: Aprende a utilizar el proveedor de ElevenLabs para el SDK de IA.
---

# Proveedor de ElevenLabs

El [proveedor de ElevenLabs](https://elevenlabs.io/) contiene soporte para el modelo de lenguaje de la API de transcripción de ElevenLabs.

## Configuración

El proveedor de ElevenLabs está disponible en el módulo `@ai-sdk/elevenlabs`. Puedes instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/elevenlabs" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/elevenlabs" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/elevenlabs" dark />
  </Tab>
</Tabs>

## Instancia de Proveedor

Puedes importar la instancia de proveedor por defecto `elevenlabs` desde `@ai-sdk/elevenlabs`:

```ts
import { elevenlabs } from '@ai-sdk/elevenlabs';
```

Si necesitas una configuración personalizada, puedes importar `createElevenLabs` desde `@ai-sdk/elevenlabs` y crear una instancia de proveedor con tus ajustes:

```ts
import { createElevenLabs } from '@ai-sdk/elevenlabs';

const elevenlabs = createElevenLabs({
  // ajustes personalizados, por ejemplo
  fetch: customFetch,
});
```

Puedes utilizar los siguientes ajustes opcionales para personalizar la instancia de proveedor de ElevenLabs:

- **apiKey** _cadena_

  Clave de API que se envía utilizando el encabezado `Authorization`.
  Por defecto, es la variable de entorno `ELEVENLABS_API_KEY`.

- **headers** _Registro&lt;cadena,cadena&gt;_

  Encabezados personalizados para incluir en las solicitudes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Por defecto, es la función global `fetch`.
  Puedes utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Transcripción

Puedes crear modelos que llamen a la [API de transcripción de ElevenLabs](https://elevenlabs.io/speech-to-text)
utilizando el método de fábrica `.transcription()`.

El primer argumento es el id del modelo, por ejemplo `scribe_v1`.

```ts
const model = elevenlabs.transcription('scribe_v1');
```

También puedes pasar opciones específicas del proveedor utilizando el argumento `providerOptions`. Por ejemplo, proporcionar el código de idioma en formato ISO-639-1 (por ejemplo `en`) puede mejorar el rendimiento de la transcripción si se conoce con anticipación.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { elevenlabs } from '@ai-sdk/elevenlabs';

const result = await transcribe({
  model: elevenlabs.transcription('scribe_v1'),
  audio: new Uint8Array([1, 2, 3, 4]),
  providerOptions: { elevenlabs: { languageCode: 'en' } },
});
```

Las siguientes opciones de proveedor están disponibles:

- **languageCode** _cadena_

  Un código de idioma ISO-639-1 o ISO-639-3 correspondiente al idioma del archivo de audio.
  Puede mejorar el rendimiento de la transcripción si se conoce con anticipación.
  Por defecto es `null`, en cuyo caso el idioma se predice automáticamente.

- **tagAudioEvents** _boolean_

  Si se deben etiquetar eventos de audio como (risas), (pasos), etc. en la transcripción.
  Por defecto es `true`.

- **numSpeakers** _entero_

  La cantidad máxima de personas hablando en el archivo subido.
  Puede ayudar a predecir quién habla cuando.
  La cantidad máxima de personas que se pueden predecir es 32.
  Por defecto es `null`, en cuyo caso la cantidad de personas se establece en el valor máximo que admite el modelo.

- **timestampsGranularity** _enum_

  La granularidad de los tiempos en la transcripción.
  Por defecto es `'word'`.
  Valores permitidos: `'none'`, `'word'`, `'character'`.

- **diarize** _boolean_

**Anotar a quién está hablando en el archivo subido.**
  Por defecto, `true`.

- **fileFormat** _enum_

  El formato del audio de entrada.
  Por defecto, `'other'`.
  Valores permitidos: `'pcm_s16le_16'`, `'other'`.
  Para `'pcm_s16le_16'`, el audio de entrada debe ser PCM de 16 bits a una frecuencia de muestreo de 16 kHz, canal único (mono) y orden de bytes little-endian.
  La latencia será menor que pasando un onda de onda codificada.

### Capabilidades del Modelo

| Modelo                    | Transcripción       | Duración            | Segmentos            | Idioma            |
| ------------------------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `scribe_v1`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `scribe_v1_experimental` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titulo: Estudio de LM
descripcion: Utilice la API compatible con OpenAI del Estudio de LM con la SDK de AI.
---

# Proveedor de Estudio de LM

[Estudio de LM](https://lmstudio.ai/) es una interfaz de usuario para ejecutar modelos locales.

Contiene un servidor de API compatible con OpenAI que puede utilizar con la SDK de AI.
Puede iniciar el servidor local en la pestaña [Servidor local](https://lmstudio.ai/docs/basics/server) del UI de Estudio de LM ("Iniciar servidor" en el botón).

## Configuración

El proveedor de Estudio de LM está disponible a través del módulo `@ai-sdk/openai-compatible` ya que es compatible con la API de OpenAI.
Puede instalarlo con

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/openai-compatible" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/openai-compatible" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/openai-compatible" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Para utilizar LM Studio, puedes crear una instancia de proveedor personalizada con la función `createOpenAICompatible` de `@ai-sdk/openai-compatible`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'http://localhost:1234/v1',
});
```

<Nota>
  LM Studio utiliza el puerto `1234` por defecto, pero puedes cambiarlo en la pestaña [Servidor Local](https://lmstudio.ai/docs/basics/server) de la aplicación.
</Nota>

## Modelos de Lenguaje

Puedes interactuar con LLMs locales en [LM Studio](https://lmstudio.ai/docs/basics/server#endpoints-overview) utilizando una instancia de proveedor.
El primer argumento es el identificador del modelo, por ejemplo `llama-3.2-1b`.

```ts
const model = lmstudio('llama-3.2-1b');
```

###### Para poder utilizar un modelo, debes descargarlo primero [aquí](https://lmstudio.ai/docs/basics/download-model).

### Ejemplo

Puedes utilizar los modelos de lenguaje de LM Studio para generar texto con la función `generateText`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'https://localhost:1234/v1',
});

const { text } = await generateText({
  model: lmstudio('llama-3.2-1b'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
  maxRetries: 1, // falla inmediatamente si el servidor no está funcionando
});
```

Los modelos de lenguaje de LM Studio también se pueden utilizar con `streamText`.

## Integrando Modelos

Puedes crear modelos que utilicen la [API de embeddings de LM Studio](https://lmstudio.ai/docs/basics/server#endpoints-overview)
mediante el método de fabricación `.embedding()`.

```ts
const model = lmstudio.embedding('text-embedding-nomic-embed-text-v1.5');
```

### Ejemplo - Integrar un Valor Único

```tsx
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { embed } from 'ai';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'https://localhost:1234/v1',
});

// 'embedding' es un objeto de integración de embeddings (number[])
const { embedding } = await embed({
  model: lmstudio.textEmbeddingModel('text-embedding-nomic-embed-text-v1.5'),
  value: 'un día soleado en la playa',
});
```

### Ejemplo - Incorporar Muchos Valores

Al cargar datos, por ejemplo, al preparar un almacén de datos para la generación recuperada-aumentada (RAG),
es útil a menudo incorporar muchos valores al mismo tiempo (incorporación en batch).

El SDK de IA proporciona la función [`embedMany`](/docs/reference/ai-sdk-core/embed-many) para este propósito.
De manera similar a `embed`, puedes utilizarla con modelos de incorporación,
por ejemplo `lmstudio.textEmbeddingModel('text-embedding-nomic-embed-text-v1.5')` o `lmstudio.textEmbeddingModel('text-embedding-bge-small-en-v1.5')`.

```tsx
import { createOpenAICompatible } from '@ai-sdk/openai';
import { embedMany } from 'ai';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'https://localhost:1234/v1',
});

// 'embeddings' es un array de objetos de incorporación (number[][]).
// Está ordenado en el mismo orden que los valores de entrada.
const { embeddings } = await embedMany({
  model: lmstudio.textEmbeddingModel('text-embedding-nomic-embed-text-v1.5'),
  values: [
    'día soleado en la playa',
    'tarde lluviosa en la ciudad',
    'noche nevada en las montañas',
  ],
});
```

---
titulo: NVIDIA NIM
descripcion: Utilice la API compatible con OpenAI de NVIDIA NIM con el SDK de IA.
---

# Proveedor NVIDIA NIM

[NVIDIA NIM](https://www.nvidia.com/en-us/ai/) proporciona microservicios de inferencia optimizados para desplegar modelos de base. Ofrece una API compatible con OpenAI que puede utilizar con el SDK de IA.

## Configuración

El proveedor NVIDIA NIM está disponible a través del módulo `@ai-sdk/openai-compatible` ya que es compatible con la API de OpenAI.
Puedes instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/openai-compatible" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/openai-compatible" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/openai-compatible" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Para utilizar NVIDIA NIM, puedes crear una instancia personalizada del proveedor con la función `createOpenAICompatible` de `@ai-sdk/openai-compatible`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const nim = createOpenAICompatible({
  name: 'nim',
  baseURL: 'https://integrate.api.nvidia.com/v1',
  headers: {
    Authorization: `Bearer ${process.env.NIM_API_KEY}`,
  },
});
```

<Nota>
  Puedes obtener una clave de API y créditos gratuitos registrándote en [NVIDIA Build](https://build.nvidia.com/explore/discover). Los nuevos usuarios reciben 1,000 créditos de inferencia para empezar.
</Nota>

## Modelos de Lenguaje

Puedes interactuar con modelos NIM utilizando una instancia del proveedor. Por ejemplo, para utilizar [DeepSeek-R1](https://build.nvidia.com/deepseek-ai/deepseek-r1), un modelo de lenguaje de código abierto poderoso:

```ts
const model = nim.chatModel('deepseek-ai/deepseek-r1');
```

### Ejemplo - Generar texto

Puedes utilizar modelos de lenguaje NIM para generar texto con la función `generateText`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

const nim = createOpenAICompatible({
  name: 'nim',
  baseURL: 'https://integrate.api.nvidia.com/v1',
  headers: {
    Authorization: `Bearer ${process.env.NIM_API_KEY}`,
  },
});

const { texto, uso, razónDeFinalización } = await generateText({
  modelo: nim.chatModel('deepseek-ai/deepseek-r1'),
  prompt: 'Cuentame la historia del burrito estilo Mission de San Francisco.',
});

console.log(texto);
console.log('Uso de tokens:', uso);
console.log('Razón de finalización:', razónDeFinalización);
```

### Ejemplo - Stream Text

Los modelos de lenguaje NIM también pueden generar texto de manera en streaming con la función `streamText`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { streamText } from 'ai';

const nim = createOpenAICompatible({
  name: 'nim',
  baseURL: 'https://integrate.api.nvidia.com/v1',
  headers: {
    Authorization: `Bearer ${process.env.NIM_API_KEY}`,
  },
});

const result = streamText({
  model: nim.chatModel('deepseek-ai/deepseek-r1'),
  prompt: 'Cuéntame la historia del Rinoceronte Blanco del Norte.',
});

for await (const textPart of result.textStream) {
  process.stdout.write(textPart);
}

console.log();
console.log('Uso de tokens:', await result.usage);
console.log('Razón de finalización:', await result.finishReason);
```

Los modelos de lenguaje NIM también se pueden utilizar con otras funciones de SDK de IA como `generateObject` y `streamObject`.

<Nota>
  El soporte de modelos para llamadas a herramientas y generación de objetos estructurados varía. Por ejemplo, el modelo
  [`meta/llama-3.3-70b-instruct`](https://build.nvidia.com/meta/llama-3_3-70b-instruct)
  admite capacidades de generación de objetos. Verifique las características específicas de cada modelo en NVIDIA Build.
</Nota>

---
titulo: Proveedores compatibles con OpenAI
descripcion: Utilice proveedores compatibles con OpenAI con el SDK de IA.
---

# Proveedores Compatible con OpenAI

Puedes utilizar el paquete de [Proveedor Compatible con OpenAI](https://www.npmjs.com/package/@ai-sdk/openai-compatible) para utilizar proveedores de modelos de lenguaje que implementen la API de OpenAI.

A continuación, nos enfocamos en la configuración general y la creación de instancias de proveedores. También puedes [escribir un paquete de proveedor personalizado aprovechando el paquete Compatible con OpenAI](/providers/openai-compatible-providers/custom-providers).

Ofrecemos documentación detallada para los siguientes proveedores compatibles con OpenAI:

- [LM Studio](/providers/openai-compatible-providers/lmstudio)
- [NIM](/providers/openai-compatible-providers/nim)
- [Baseten](/providers/openai-compatible-providers/baseten)

La configuración general y la creación de instancias de proveedores es la misma para todos estos proveedores.

## Configuración

El proveedor Compatible con OpenAI está disponible a través del módulo `@ai-sdk/openai-compatible`. Puedes instalarlo con:

<Tabs items={['pnpm', 'npm', 'yarn']}>
  <Tab>
    <Snippet text="pnpm add @ai-sdk/openai-compatible" dark />
  </Tab>
  <Tab>
    <Snippet text="npm install @ai-sdk/openai-compatible" dark />
  </Tab>
  <Tab>
    <Snippet text="yarn add @ai-sdk/openai-compatible" dark />
  </Tab>
</Tabs>

## Instancia del Proveedor

Para utilizar un proveedor compatible con OpenAI, puede crear una instancia de proveedor personalizada con la función `createOpenAICompatible` de `@ai-sdk/openai-compatible`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const provider = createOpenAICompatible({
  name: 'nombre-del-proveedor',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.proveedor.com/v1',
});
```

Puede utilizar las siguientes configuraciones opcionales para personalizar la instancia del proveedor:

- **baseURL** _cadena_

  Establece la prefija de URL para llamadas a API.

- **apiKey** _cadena_

  Clave de API para autenticar solicitudes. Si se especifica, agrega un encabezado `Authorization`
  a los encabezados de solicitud con el valor `Bearer <apiKey>`. Esto se agregará
  antes de cualquier encabezado potencialmente especificado en la opción `headers`.

- **headers** _Registro&lt;string,string&gt;_

  Encabezados personalizados opcionales para incluir en solicitudes. Estos se agregarán a los encabezados de solicitud
  después de cualquier encabezado potencialmente agregado por el uso de la opción `apiKey`.

- **queryParams** _Registro&lt;string,string&gt;_

  Parámetros de consulta de URL personalizados opcionales para incluir en las URLs de solicitud.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implementación personalizada de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). 
  Por defecto, utiliza la función global `fetch`. 
  Puede utilizarla como middleware para interceptar solicitudes,
  o para proporcionar una implementación de fetch personalizada para e.g. pruebas.

## Modelos de Lenguaje

Puede crear modelos de proveedor utilizando una instancia de proveedor.
El primer argumento es el identificador del modelo, por ejemplo `model-id`.

```ts
const model = provider('model-id');
```

### Ejemplo

Puedes utilizar modelos de proveedor de lenguaje para generar texto con la función `generateText`:

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

const proveedor = createOpenAICompatible({
  nombre: 'nombre-del-proveedor',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.proveedor.com/v1',
});

const { texto } = await generateText({
  modelo: proveedor('modelo-id'),
  prompt: 'Escribe una receta de lasaña vegetariana para 4 personas.',
});
```

### Incluyendo IDs de modelos para completar automáticamente

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

type EjemplosIdsDeModelosDeChat =
  | 'meta-llama/Llama-3-70b-chat-hf'
  | 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
  | (string & {});

type EjemplosIdsDeModelosDeCompleción =
  | 'codellama/CodeLlama-34b-Instruct-hf'
  | 'Qwen/Qwen2.5-Coder-32B-Instruct'
  | (string & {});

type EjemplosIdsDeModelosDeEmbebido =
  | 'BAAI/bge-large-en-v1.5'
  | 'bert-base-uncased'
  | (string & {});

const modelo = createOpenAICompatible<
  EjemplosIdsDeModelosDeChat,
  EjemplosIdsDeModelosDeCompleción,
  EjemplosIdsDeModelosDeEmbebido
>({
  nombre: 'example',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.example.com/v1',
});

// Las llamadas subsiguientes a e.g. `modelo.chatModel` completarán automáticamente el id del modelo
// desde la lista de `EjemplosIdsDeModelosDeChat` mientras aún permite cadenas libres.

const { texto } = await generateText({
  modelo: modelo.chatModel

### Parámetros de consulta personalizados

Algunos proveedores pueden requerir parámetros de consulta personalizados. Un ejemplo es la [API de Inferencia de Modelos de Inteligencia Artificial de Azure](https://learn.microsoft.com/en-us/azure/machine-learning/reference-model-inference-chat-completions?view=azureml-api-2), que requiere un parámetro de consulta `api-version`.

Puedes establecer estos a través de la configuración de proveedor opcional `queryParams`. Estos se agregarán a todas las solicitudes realizadas por el proveedor.

```ts highlight="7-9"
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const provider = createOpenAICompatible({
  name: 'nombre-del-proveedor',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.proveedor.com/v1',
  queryParams: {
    'api-version': '1.0.0',
  },
});
```

Por ejemplo, con la configuración anterior, las solicitudes API incluirían el parámetro de consulta en la URL como:
`https://api.proveedor.com/v1/chat/completions?api-version=1.0.0`.

## Opciones específicas del proveedor

El proveedor compatible con OpenAI admite agregar opciones específicas del proveedor al cuerpo de la solicitud. Estas se especifican con el campo `providerOptions` en el cuerpo de la solicitud.

Por ejemplo, si creas una instancia de proveedor con el nombre `provider-name`, puedes agregar un campo `custom-option` al cuerpo de la solicitud de la siguiente manera:

```ts
const provider = createOpenAICompatible({
  name: 'provider-name',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.provider.com/v1',
});

const { text } = await generateText({
  model: provider('model-id'),
  prompt: 'Hello',
  providerOptions: {
    'provider-name': { customOption: 'magic-value' },
  },
});
```

El cuerpo de la solicitud enviado al proveedor incluirá el campo `customOption` con el valor `magic-value`. Esto te da una forma fácil de agregar opciones específicas del proveedor a las solicitudes sin tener que modificar el código del proveedor o la SDK de IA.

## Extracción de Metadatos Personalizados

El proveedor compatible con OpenAI admite la extracción de metadatos específicos del proveedor desde respuestas de API a través de extractores de metadatos.
Estos extractores te permiten capturar información adicional devuelta por el proveedor más allá del formato de respuesta estándar.

Los extractores de metadatos reciben los datos de respuesta bruta y no procesada del proveedor, lo que te da completa flexibilidad
para extraer cualquier campo personalizado o características experimentales que el proveedor incluya.
Esto es particularmente útil cuando:

- Estás trabajando con proveedores que incluyen campos de respuesta no estándar
- Estás experimentando con características beta o de vista previa
- Estás capturando métricas o información de depuración específicas del proveedor
- Estás apoyando la evolución rápida de la API del proveedor sin cambios en el SDK

Los extractores de metadatos funcionan con tanto completos como streaming completos de chat y consisten en dos componentes principales:

1. Una función para extraer metadatos de respuestas completas
2. Un extractor de transmisión que puede acumular metadatos a lo largo de trozos en una respuesta de transmisión

Aquí hay un ejemplo de extractor de metadatos que captura tanto datos estándar como personalizados del proveedor:

```typescript
const myMetadataExtractor: MetadataExtractor = {
  // Procesar respuestas completas, no de transmisión
  extractMetadata: ({ parsedBody }) => {
    // Tienes acceso a la respuesta bruta completa
    // Extraer cualquier campo que el proveedor incluya
    return {
      miProveedor: {
        usoEstandar: parsedBody.usage,
        característicasExperimentales: parsedBody.beta_features,
        métricasPersonalizadas: {
          tiempoDeProcesamiento: parsedBody.server_timing?.total_ms,
          versiónDelModelo: parsedBody.model_version,
          // ... cualquier otro dato específico del proveedor
        },
      },
    };
  },

  // Procesar respuestas de transmisión
  createStreamExtractor: () => {
    let accumulatedData = {
      timing: [],
      camposPersonalizados: {},
    };
```

Nota: He mantenido el código en inglés como se solicitó en el enunciado del problema.

```markdown
return {
  // Procesar cada trozo de datos bruto
  processChunk: parsedChunk => {
    if (parsedChunk.server_timing) {
      accumulatedData.timing.push(parsedChunk.server_timing);
    }
    if (parsedChunk.custom_data) {
      Object.assign(accumulatedData.customFields, parsedChunk.custom_data);
    }
  },
  // Construir metadatos finales a partir de los datos acumulados
  buildMetadata: () => ({
    miProveedor: {
      tiempoDeTransmisión: accumulatedData.timing,
      datosPersonalizados: accumulatedData.customFields,
    },
  }),
};
},
```

Puedes proporcionar un extractor de metadatos cuando se crea una instancia de tu proveedor:

```typescript
const proveedor = createOpenAICompatible({
  nombre: 'mi-proveedor',
  apiKey: process.env.PROVEEDOR_API_KEY,
  baseURL: 'https://api.proveedor.com/v1',
  metadataExtractor: miMetadataExtractor,
});
```

Los metadatos extraídos se incluirán en la respuesta bajo el campo `providerMetadata`:

```typescript
const { texto, providerMetadata } = await generarTexto({
  modelo: proveedor('modelo-id'),
  prompt: 'Hola',
});

console.log(providerMetadata.miProveedor.datosPersonalizados);
```

Esto te permite acceder a información específica del proveedor mientras se mantiene una interfaz consistente a lo largo de diferentes proveedores.