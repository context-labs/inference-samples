---
titre : Serveur HTTP Node.js
description : Apprenez à utiliser le SDK AI dans un serveur HTTP Node.js
tags : ['serveurs API', 'streaming']
---

# Serveur HTTP Node.js

Vous pouvez utiliser le SDK AI dans un serveur HTTP Node.js pour générer du texte et le transmettre au client.

## Exemples

Les exemples démarreront un serveur HTTP simple qui écoute sur le port 8080. Vous pouvez par exemple le tester en utilisant `curl` :

```bash
curl -X POST http://localhost:8080
```

<Note>
  Les exemples utilisent le modèle OpenAI `gpt-4o`. Assurez-vous que la clé API OpenAI est
  définie dans l'environnement de variable `OPENAI_API_KEY`.
</Note>

**Exemple complet** : [github.com/vercel/ai/examples/node-http-server](https://github.com/vercel/ai/tree/main/examples/node-http-server)

### Flux de données

Vous pouvez utiliser la méthode `pipeDataStreamToResponse` pour faire passer les données du flux au réponse du serveur.

```typescript filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { createServer } from 'http';

createServer(async (req, res) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  });

  result.pipeDataStreamToResponse(res);
}).listen(8080);
```

### Envoi de Données Custom

`pipeDataStreamToResponse` peut être utilisé pour envoyer des données personnalisées au client.

```ts filename='index.ts' highlight="6-9,16"
import { openai } from '@ai-sdk/openai';
import { pipeDataStreamToResponse, streamText } from 'ai';
import { createServer } from 'http';

createServer(async (req, res) => {
  // commencez immédiatement à diffuser la réponse
  pipeDataStreamToResponse(res, {
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('appel initialisé');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: error => {
      // Les messages d'erreur sont masqués par défaut pour des raisons de sécurité.
      // Si vous souhaitez exposer le message d'erreur au client, vous pouvez le faire ici :
      return error instanceof Error ? error.message : String(error);
    },
  });
}).listen(8080);
```

### Flux de Texte

Vous pouvez envoyer un flux de texte au client à l'aide de `pipeTextStreamToResponse`.

```ts filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { createServer } from 'http';

createServer(async (req, res) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  });

  result.pipeTextStreamToResponse(res);
}).listen(8080);
```

## Dépannage

- Streaming non fonctionnel lorsqu'il est [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
titre : Express
description : Apprenez à utiliser le SDK AI dans un serveur Express
tags : ['serveurs API', 'streaming']
---

# Express

Vous pouvez utiliser le SDK AI dans un [Express](https://expressjs.com/) serveur pour générer et diffuser du texte et des objets vers le client.

## Exemples

Les exemples démarrent un serveur HTTP simple qui écoute sur le port 8080. Vous pouvez par exemple le tester en utilisant `curl` :

```bash
curl -X POST http://localhost:8080
```

<Note>
  Les exemples utilisent le modèle OpenAI `gpt-4o`. Assurez-vous que la clé API OpenAI est
  définie dans la variable d'environnement `OPENAI_API_KEY`.
</Note>

**Exemple complet** : [github.com/vercel/ai/examples/express](https://github.com/vercel/ai/tree/main/examples/express)

### Flux de données

Vous pouvez utiliser la méthode `pipeDataStreamToResponse` pour diffuser les données de flux vers la réponse du serveur.

```ts filename='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import express, { Request, Response } from 'express';

const app = express();

app.post('/', async (req: Request, res: Response) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  });

  result.pipeDataStreamToResponse(res);
});

app.listen(8080, () => {
  console.log(`Exemple d'application qui écoute sur le port ${8080}`);
});
```

### Envoyer des Données Custom

`pipeDataStreamToResponse` peut être utilisé pour envoyer des données custom au client.

```ts filename='index.ts' highlight="8-11,18"
import { openai } from '@ai-sdk/openai';
import { pipeDataStreamToResponse, streamText } from 'ai';
import express, { Request, Response } from 'express';

const app = express();

app.post('/stream-data', async (req: Request, res: Response) => {
  // démarrer immédiatement la diffusion de la réponse
  pipeDataStreamToResponse(res, {
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('appel initialisé');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventez un nouveau jour férié et décrit ses traditions.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: error => {
      // Les messages d'erreur sont masqués par défaut pour des raisons de sécurité.
      // Si vous souhaitez exposer le message d'erreur au client, vous pouvez le faire ici :
      return error instanceof Error ? error.message : String(error);
    },
  });
});

app.listen(8080, () => {
  console.log(`L'application d'exemple écoute sur le port ${8080}`);
});
```

### Flux de texte

Vous pouvez envoyer un flux de texte au client à l'aide de `pipeTextStreamToResponse`.

```ts fichier='index.ts' miseEnSurbrillance="13"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import express, { Request, Response } from 'express';

const app = express();

app.post('/', async (req: Request, res: Response) => {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  });

  result.pipeTextStreamToResponse(res);
});

app.listen(8080, () => {
  console.log(`L'exemple d'application écoute sur le port ${8080}`);
});
```

## Dépannage

- Le streaming ne fonctionne pas lorsque vous êtes [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
titre: Hono
description: Exemple d'utilisation de la bibliothèque AI dans un serveur Hono.
tags: ['serveurs API', 'streaming']
---

# Hono

Vous pouvez utiliser la bibliothèque AI dans un [Hono](https://hono.dev/) pour générer et diffuser du texte et des objets au client.

## Exemples

Les exemples lancent un serveur HTTP simple qui écoute sur le port 8080. Vous pouvez tester cela en utilisant `curl` :

```bash
curl -X POST http://localhost:8080
```

<Note>
  Les exemples utilisent le modèle OpenAI `gpt-4o`. Assurez-vous que la clé API OpenAI est définie dans la variable d'environnement `OPENAI_API_KEY`.
</Note>

**Exemple complet** : [github.com/vercel/ai/examples/hono](https://github.com/vercel/ai/tree/main/examples/hono)

### Flux de Données

Vous pouvez utiliser la méthode `toDataStream` pour obtenir un flux de données à partir du résultat et puis le rediriger vers la réponse.

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
    prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  });

  // Marquez la réponse comme un flux de données v1 :
  c.header('X-Vercel-AI-Data-Stream', 'v1');
  c.header('Content-Type', 'text/plain; charset=utf-8');

  return stream(c, stream => stream.pipe(result.toDataStream()));
});

serve({ fetch: app.fetch, port: 8080 });
```

### Envoi de Données Custom

`createDataStream` peut être utilisé pour envoyer des données custom au client.

```ts filename='index.ts' highlight="10-13,20"
import { openai } from '@ai-sdk/openai';
import { serve } from '@hono/node-server';
import { createDataStream, streamText } from 'ai';
import { Hono } from 'hono';
import { stream } from 'hono/streaming';

const app = new Hono();

app.post('/stream-data', async c => {
  // commencez immédiatement à fluxer la réponse
  const dataStream = createDataStream({
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('appel initialisé');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: erreur => {
      // Les messages d'erreur sont masqués par défaut pour des raisons de sécurité.
      // Si vous souhaitez exposer le message d'erreur au client, vous pouvez le faire ici :
      return erreur instanceof Error ? erreur.message : String(erreur);
    },
  });

  // Marquez la réponse comme un flux de données v1 :
  c.header('X-Vercel-AI-Data-Stream', 'v1');
  c.header('Content-Type', 'text/plain; charset=utf-8');

  return stream(c, stream =>
    stream.pipe(dataStream.pipeThrough(new TextEncoderStream())),
  );
});

serve({ fetch: app.fetch, port: 8080 });
```

### Flux de texte

Vous pouvez utiliser la propriété `textStream` pour obtenir un flux de texte à partir du résultat et le rediriger vers la réponse.

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
    prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  });

  c.header('Content-Type', 'text/plain; charset=utf-8');

  return stream(c, stream => stream.pipe(result.textStream));
});

serve({ fetch: app.fetch, port: 8080 });
```

## Dépannage

- Le streaming ne fonctionne pas lorsque vous utilisez [la mise en cache](/docs/troubleshooting/streaming-not-working-when-proxied)

---
title: Fastify
description: Apprenez à utiliser le SDK AI dans un serveur Fastify
tags: ['serveurs API', 'streaming']
---

# Fastify

Vous pouvez utiliser le SDK AI dans un [serveur Fastify](https://fastify.dev/) pour générer et diffuser du texte et des objets vers le client.

## Exemples

Les exemples lancent un serveur HTTP simple qui écoute sur le port 8080. Vous pouvez par exemple le tester à l'aide de `curl` :

```bash
curl -X POST http://localhost:8080
```

<Note>
  Les exemples utilisent le modèle OpenAI `gpt-4o`. Assurez-vous que la clé API OpenAI est
  définie dans la variable d'environnement `OPENAI_API_KEY`.
</Note>

**Exemple complet** : [github.com/vercel/ai/examples/fastify](https://github.com/vercel/ai/tree/main/examples/fastify)

### Flux de Données

Vous pouvez utiliser la méthode `toDataStream` pour obtenir un flux de données à partir du résultat et puis le faire passer à la réponse.

```ts fichier='index.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.post('/', async function (request, reply) {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  });

  // Marquez la réponse comme un flux de données v1 :
  reply.header('X-Vercel-AI-Data-Stream', 'v1');
  reply.header('Content-Type', 'text/plain; charset=utf-8');

  return reply.send(result.toDataStream({ data }));
});

fastify.listen({ port: 8080 });
```

### Envoyer des Données Custom

`createDataStream` peut être utilisé pour envoyer des données custom au client.

```ts filename='index.ts' highlight="8-11,18"
import { openai } from '@ai-sdk/openai';
import { createDataStream, streamText } from 'ai';
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.post('/stream-data', async function (request, reply) {
  // commencez immédiatement à diffuser la réponse
  const dataStream = createDataStream({
    execute: async dataStreamWriter => {
      dataStreamWriter.writeData('appel initialisé');

      const result = streamText({
        model: openai('gpt-4o'),
        prompt: 'Inventez un nouveau jour férié et décrit ses traditions.',
      });

      result.mergeIntoDataStream(dataStreamWriter);
    },
    onError: erreur => {
      // Les messages d'erreur sont masqués par défaut pour des raisons de sécurité.
      // Si vous souhaitez exposer le message d'erreur au client, vous pouvez le faire ici :
      return erreur instanceof Error ? erreur.message : String(erreur);
    },
  });

  // Marquez la réponse comme un flux de données v1 :
  reply.header('X-Vercel-AI-Data-Stream', 'v1');
  reply.header('Content-Type', 'text/plain; charset=utf-8');

  return reply.send(dataStream);
});

fastify.listen({ port: 8080 });
```

### Flux de Texte

Vous pouvez utiliser la propriété `textStream` pour obtenir un flux de texte à partir du résultat et puis le rediriger vers la réponse.

```ts filename='index.ts' highlight="15"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.post('/', async function (request, reply) {
  const result = streamText({
    model: openai('gpt-4o'),
    prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  });

  reply.header('Content-Type', 'text/plain; charset=utf-8');

  return reply.send(result.textStream);
});

fastify.listen({ port: 8080 });
```

## Dépannage

- Le flux ne fonctionne pas lorsque vous utilisez un [proxy](/docs/troubleshooting/streaming-not-working-when-proxied)

---
title: Nest.js
description: Apprenez à utiliser le SDK AI dans un serveur Nest.js
tags: ['serveurs API', 'flux']
---

# Nest.js

Vous pouvez utiliser le SDK AI dans un [serveur Nest.js](https://nestjs.com/) pour générer et envoyer en flux de texte et d'objets au client.

## Exemples

Les exemples montrent comment implémenter un contrôleur Nest.js qui utilise le SDK AI pour envoyer en flux de texte et d'objets au client.

**Exemple complet** : [github.com/vercel/ai/examples/nest](https://github.com/vercel/ai/tree/main/examples/nest)

### Flux de Données

Vous pouvez utiliser la méthode `pipeDataStreamToResponse` pour obtenir un flux de données à partir du résultat et puis le faire passer à la réponse.

```ts nom_fichier='app.controller.ts'
import { Controller, Post, Res } from '@nestjs/common';
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { Response } from 'express';

@Controller()
export class AppController {
  @Post()
  async exemple(@Res() res: Response) {
    const result = streamText({
      model: openai('gpt-4o'),
      prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
    });

    result.pipeDataStreamToResponse(res);
  }
}
```

### Envoi de Données Custom

`pipeDataStreamToResponse` peut être utilisé pour envoyer des données personnalisées au client.

```ts fichier='app.controller.ts' miseEnSurbrillance="10-12,19"
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
        dataStreamWriter.writeData('appel initialisé');

        const result = streamText({
          model: openai('gpt-4o'),
          prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
        });

        result.mergeIntoDataStream(dataStreamWriter);
      },
      onError: erreur => {
        // Les messages d'erreur sont masqués par défaut pour des raisons de sécurité.
        // Si vous souhaitez exposer le message d'erreur au client, vous pouvez le faire ici :
        return erreur instanceof Error ? erreur.message : String(erreur);
      },
    });
  }
}
```

### Flux de Texte

Vous pouvez utiliser la méthode `pipeTextStreamToResponse` pour obtenir un flux de texte à partir du résultat et puis le faire passer à la réponse.

```ts filename='app.controller.ts' highlight="15"
import { Controller, Post, Res } from '@nestjs/common';
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { Response } from 'express';

@Controller()
export class AppController {
  @Post()
  async example(@Res() res: Response) {
    const result = streamText({
      model: openai('gpt-4o'),
      prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
    });

    result.pipeTextStreamToResponse(res);
  }
}
```

## Dépannage

- La mise en flux ne fonctionne pas lorsque [proxifié](/docs/troubleshooting/streaming-not-working-when-proxied)

---
title: SDK AI par Vercel
description: Le SDK AI est l'outil TypeScript pour la construction d'applications et d'agents AI avec React, Next.js, Vue, Svelte, Node.js, et plus encore.
---

# SDK AI

Le SDK AI est l'outil TypeScript conçu pour aider les développeurs à construire des applications et des agents AI avec React, Next.js, Vue, Svelte, Node.js, et plus encore.

## Pourquoi utiliser le SDK AI ?

L'intégration de grands modèles de langage (LLM) dans les applications est compliquée et dépend fortement du fournisseur de modèle spécifique que vous utilisez.

Le SDK AI normalise l'intégration des modèles d'intelligence artificielle (IA) à travers [les fournisseurs pris en charge](/docs/foundations/providers-and-models). Cela permet aux développeurs de se concentrer sur la création d'applications AI de haute qualité, sans gaspiller leur temps sur les détails techniques.

Par exemple, voici comment vous pouvez générer du texte avec différents modèles en utilisant le SDK AI :

<PreviewSwitchProviders />

Le SDK AI dispose de deux bibliothèques principales :

- **[SDK AI Core](/docs/ai-sdk-core) :** Une API unifiée pour générer du texte, des objets structurés, des appels de fonction et construire des agents avec les LLM.
- **[SDK AI UI](/docs/ai-sdk-ui) :** Un ensemble de hooks sans framework pour construire rapidement des interfaces utilisateur de chat et génératives.

## Fournisseurs de Modèles

Le SDK AI prend en charge [plusieurs fournisseurs de modèles](/providers).

<OfficialModelCards />

## Modèles

Nous avons construit certains [modèles](https://vercel.com/templates?type=ai) qui incluent des intégrations SDK AI pour différents cas d'utilisation, fournisseurs et frameworks. Vous pouvez utiliser ces modèles pour démarrer votre application AI.

### Kits de démarrage

<Templates type="starter-kits" />

### Exploration de fonctionnalités

<Templates type="feature-exploration" />

### Frameworks

<Templates type="frameworks" />

### UI Générative

<Templates type="generative-ui" />

### Sécurité

<Templates type="security" />

## Rejoignez notre Communauté

Si vous avez des questions sur tout ce qui concerne le SDK AI, vous êtes toujours les bienvenus pour poser vos questions dans notre communauté sur [GitHub Discussions](https://github.com/vercel/ai/discussions).

## `llms.txt` (pour Cursor, Windsurf, Copilot, Claude, etc.)

Vous pouvez accéder à la documentation complète du SDK AI en format Markdown à [ai-sdk.dev/llms.txt](/llms.txt). Cela peut être utilisé pour poser des questions à tout LLM (en supposant qu'il dispose d'une fenêtre de contexte suffisamment large) sur le SDK AI sur la documentation la plus à jour.

### Exemple d'utilisation

Par exemple, pour solliciter un LLM sur les questions concernant le SDK AI :

1. Copiez le contenu de la documentation à partir de [ai-sdk.dev/llms.txt](/llms.txt)
2. Utilisez le format de sollicitation suivant :

```prompt
Documentation :
{coller la documentation ici}
---
Sur la base de la documentation ci-dessus, réponds à la question suivante :
{votre question}
```

---
titre : AI SDK 5 Alpha
description : Démarrage avec la version Alpha de AI SDK 5.
---

# Lancement de AI SDK 5 Alpha

<Note type="warning">
  C'est une prévisualisation précoce — AI SDK 5 est en développement actif. Les APIs peuvent changer sans avertissement. Fixez-vous sur des versions spécifiques car les changements de version peuvent se produire même dans les patchs. Pour en savoir plus, consultez les [docs v5](https://v5.ai-sdk.dev)
</Note>

## Conseils pour la version Alpha

Le SDK AI 5 Alpha est destiné à :

- L'exploration et les prototypes précoces
- Les projets de terrain vierge où vous pouvez expérimenter librement
- Les environnements de développement où vous pouvez tolérer les changements de version

Cette version Alpha n'est **pas recommandée** pour :

- Les applications de production
- Les projets qui nécessitent des APIs stables
- Les applications existantes qui nécessiteraient des chemins de migration

Pendant cette phase Alpha, nous nous attendons à apporter des changements significatifs, potentiellement brisants à la surface de l'API. Nous partageons tôt pour recueillir des commentaires et améliorer le SDK avant la stabilisation. Votre input est précieux — partagez vos expériences à travers les problèmes GitHub ou les discussions pour aider à façonner la version finale.

<Note type="warning">
  Nous nous attendons à des bugs dans cette version Alpha. Pour nous aider à améliorer le SDK, veuillez [soumettre des rapports de bug sur GitHub](https://github.com/vercel/ai/issues/new/choose). Vos rapports contribuent directement à rendre la version finale plus stable et fiable.
</Note>

Pour en savoir plus, consultez les [docs v5](https://v5.ai-sdk.dev).

## Installation

Pour installer le SDK AI 5 - Alpha, exécutez la commande suivante :

```bash
npm install @vercel/ai@alpha
```

# remplacez par votre fournisseur et votre framework
npm install ai@alpha @ai-sdk/[votre-fournisseur]@alpha @ai-sdk/[votre-framework]@alpha
```

<Note type="avertissement">
  Les APIs peuvent changer sans préavis. Fixez-vous sur des versions spécifiques car des changements de rupture
  peuvent se produire même dans les mises à jour de patch.
</Note>

## Qu'est-ce de nouveau dans l'API SDK 5 ?

L'API SDK 5 est une refonte complète du protocole et de l'architecture de l'API SDK basée sur tout ce que nous avons appris au cours des deux dernières années d'utilisation dans le monde réel. Nous avons également modernisé l'interface utilisateur et les protocoles qui ont resté largement inchangés depuis l'API SDK v2/3, créant une solide base pour l'avenir.

### Pourquoi l'API SDK 5 ?

Lorsque nous avons conçu le protocole v1 il y a plus d'un an, le modèle d'interaction standard avec les modèles de langage était simple : texte entré, appel de texte ou d'outil sortant. Mais les LLMs d'aujourd'hui vont bien au-delà du texte et des appels d'outil, générant des raisonnements, des sources, des images et plus encore. De plus, de nouveaux cas d'utilisation comme les agents utilisant des ordinateurs introduisent une approche fondamentalement nouvelle pour interagir avec les modèles de langage qui a rendu impossible de les supporter dans une approche unifiée avec notre architecture originale.

Nous avions besoin d'un protocole conçu pour cette nouvelle réalité. Même si cela constitue une rupture de changement que nous n'abordons pas légèrement, cela nous a donné l'occasion de reconstruire la base et d'ajouter de puissants nouveaux fonctionnalités.

Même si nous avons conçu l'API SDK 5 pour être une amélioration substantielle par rapport aux versions précédentes, nous sommes toujours en développement actif. Vous pourriez rencontrer des bogues ou un comportement inattendu. Nous apprécierions grandement vos retours d'expérience et vos rapports de bogues — ils sont essentiels pour rendre cette version meilleure. Partagez vos expériences et vos suggestions avec nous à travers les [issues GitHub](https://github.com/vercel/ai/issues/new/choose) ou les [discussions GitHub](https://github.com/vercel/ai/discussions).

## Nouvelles fonctionnalités

- [**LanguageModelV2**](#languagemodelv2) - nouvelle architecture redessinée
- [**Message Overhaul**](#message-overhaul) - nouveaux types `UIMessage` et `ModelMessage`
- [**ChatStore**](#chatstore) - nouvelle architecture `useChat`
- [**Server-Sent Events (SSE)**](

# Serveurs Envois d'Événements (SSE) - nouveau protocole standardisé pour envoyer des messages de l'interface utilisateur au client
- [**Contrôle Agent**](#contrôle-agent) - nouvelles primitives pour construire des systèmes agents

## LanguageModelV2

LanguageModelV2 représente une refonte complète de la façon dont le SDK IA communique avec les modèles de langage, adaptée aux sorties complexes croissantes des systèmes AI modernes. Le nouveau LanguageModelV2 traite toutes les sorties LLM comme des parties de contenu, permettant un traitement plus cohérent du texte, des images, de la raison, des sources et d'autres types de réponse. Il dispose maintenant :

- **Conception de Contenu Prioritaire** - Au lieu de séparer le texte, la raison et les appels de l'outil, tout est maintenant représenté comme des parties de contenu ordonnées dans un tableau unifié
- **Sécurité de Type Améliorée** - Le nouveau LanguageModelV2 fournit des garanties de type TypeScript plus sûres, facilitant ainsi le travail avec différents types de contenu
- **Extensibilité Simplifiée** - L'ajout de support pour de nouvelles capacités de modèle ne nécessite plus de changements à la structure de base

## Réaménagement des Messages

La SDK AI 5 présente un système de messages entièrement réaménagé avec deux types de messages qui répondent aux besoins duals de ce que vous affichez dans votre interface et de ce que vous envoyez au modèle. Le contexte est crucial pour des générations efficaces de modèles de langage, et ces deux types de messages servent des buts distincts :

- **MessageUIMessage** représente l'histoire complète de conversation pour votre interface, conservant tous les parties de message (texte, images, données), les métadonnées (horaires de création, horaires de génération), et l'état de l'interface—quel que soit sa longueur.

- **ModelMessage** est optimisé pour l'envoi vers les modèles de langage, en considérant les contraintes d'entrée de jetons. Il supprime les métadonnées spécifiques à l'interface et les contenus irrelevants.

Avec cette modification, vous devrez explicitement convertir vos `MessageUIMessage`s en `ModelMessage`s avant de les envoyer au modèle.

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

<Note>
  Cette séparation est essentielle car vous ne pouvez pas utiliser un seul format de message pour les deux buts. L'état que vous sauvegardez devrait toujours être le format de `MessageUIMessage` pour éviter la perte d'informations, avec une conversion explicite en `ModelMessage` lors de la communication avec les modèles de langage.
</Note>

Le nouveau système de messages a rendu possible plusieurs fonctionnalités fortement demandées :

- **Métadonnées de Message de Type Sécurisé** - ajoutez des informations structurées par message
- **Nouveau Écrivain de Flux** - fluxez tout type de partie (raisonnement, sources, etc.) en conservant l'ordre approprié
- **Parties de Données** - fluxez des parties de données de type sécurisé pour les composants UI dynamiques

### Métadonnées du message

Les métadonnées permettent de joindre des informations structurées à des messages individuels, ce qui facilite la gestion de détails importants comme le temps de réponse, l'utilisation de jetons ou les spécifications du modèle. Ces informations peuvent améliorer votre interface utilisateur avec des données contextuelles sans les intégrer dans le contenu du message lui-même.

Pour ajouter des métadonnées à un message, définissez d'abord le schéma de métadonnées :

```ts filename="app/api/chat/example-metadata-schema.ts"
export const exampleMetadataSchema = z.object({
  durée: z.number().optional(),
  modèle: z.string().optional(),
  jetonsTotal: z.number().optional(),
});

export type ExampleMetadata = z.infer<typeof exampleMetadataSchema>;
```

Ensuite, ajoutez les métadonnées en utilisant la propriété `message.metadata` de la fonction `toUIMessageStreamResponse()` :

```ts filename="app/api/chat/route.ts"
import { openai } from '@ai-sdk/openai';
import { convertToModelMessages, streamText, UIMessage } from 'ai';
import { ExampleMetadata } from './example-metadata-schema';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const startTime = Date.now();
  const result = streamText({
    modèle: openai('gpt-4o'),
    prompt: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse({
    messageMetadata: ({ part }): ExampleMetadata | undefined => {
      // envoie des informations personnalisées au client au démarrage :
      if (part.type === 'start') {
        return {
          modèle: 'gpt-4o', // identifiant initial du modèle
        };
      }
```

// envoie des informations supplémentaires sur le modèle à la fin de l'étape de finition :
      if (part.type === 'finish-step') {
        return {
          model: part.response.modelId, // met à jour avec l'ID du modèle réel
          duration: Date.now() - startTime,
        };
      }

      // lorsqu'un message est terminé, envoie des informations supplémentaires :
      if (part.type === 'finish') {
        return {
          totalTokens: part.totalUsage.totalTokens,
        };
      }
    },
  });
}
```

Enfin, spécifiez le schéma de métadonnées du message sur le client et puis affichez (dans un cadre sécurisé) les métadonnées dans votre interface utilisateur :

```tsx fichier="app/page.tsx"
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

```jsx
return (
  <div>
    {messages.map(message => {
      const { metadata } = message;
      return (
        <div key={message.id} className="whitespace-pre-wrap">
          {metadata?.duration && <div>Durée : {metadata.duration}ms</div>}
          {metadata?.model && <div>Modèle : {metadata.model}</div>}
          {metadata?.totalTokens && (
            <div>Jetons totaux : {metadata.totalTokens}</div>
          )}
        </div>
      );
    })}
  </div

### Flux de Messages de l'Interface Utilisateur

Le flux de messages de l'interface utilisateur permet de diffuser tout type de contenu provenant du serveur vers le client. Avec ce flux, vous pouvez envoyer des données structurées comme des sources personnalisées de votre pipeline RAG directement vers votre interface utilisateur. L'écrivain de flux est simplement une utilité qui facilite l'écriture dans ce flux de messages.

```ts
const stream = createUIMessageStream({
  execute: writer => {
    // diffusez des sources personnalisées
    writer.write({
      type: 'source',
      value: {
        type: 'source',
        sourceType: 'url',
        id: 'source-1',
        url: 'https://example.com',
        title: 'Exemple de Source',
      },
    });
  },
});
```

Sur le client, ceux-ci seront ajoutés à l'array `message.parts` ordonnée.

### Parties de données

Le nouveau flux de sortie permet également une façon sécurisée par type de fluxer des données arbitraires du serveur vers le client et de les afficher dans votre interface utilisateur.

Vous pouvez créer et fluxer des parties de données personnalisées sur le serveur :

```tsx
// Sur le serveur
const flux = createUIMessageStream({
  execute: writer => {
    // Mise à jour initiale
    writer.write({
      type: 'données-météo', // Type personnalisé
      id: toolCallId, // ID pour les mises à jour
      données: { ville, status: 'chargement' }, // Vos données
    });

    // Plus tard, mettez à jour la même partie
    writer.write({
      type: 'données-météo',
      id: toolCallId,
      données: { ville, météo, status: 'succès' },
    });
  },
});
```

Sur le client, vous pouvez afficher ces parties avec une sécurité par type :

```tsx
{
  message.parts
    .filter(part => part.type === 'données-météo') // sécurisé par type
    .map((part, index) => (
      <Météo
        key={index}
        ville={part.données.ville} // sécurisé par type
        météo={part.données.météo} // sécurisé par type
        status={part.données.status} // sécurisé par type
      />
    ));
}
```

Les parties de données apparaissent dans le tableau `message.parts` en compagnie d'autres contenus, en maintenant l'ordre correct de la conversation. Vous pouvez mettre à jour des parties en référençant le même ID, permettant des expériences dynamiques comme des artefacts collaboratifs.

## ChatStore

AI SDK 5 introduit une nouvelle architecture `useChat` avec les composants ChatStore et ChatTransport. Ces deux blocs de construction fondamentaux rendent la gestion d'état et l'intégration de l'API plus flexibles, vous permettant de composer des liaisons de l'interface utilisateur réactive, de partager l'état de la conversation entre plusieurs instances et de remplacer votre protocole de serveur sans reécrire la logique d'application.

Le `ChatStore` est responsable de :

- **Gestion de plusieurs conversations** – accéder et passer entre les conversations de manière fluide.
- **Traitement des flux de réponse** – gérer les flux provenant du serveur et synchroniser l'état (par exemple, lorsque des résultats de l'outil côté client sont synchronisés).
- **Caching et synchronisation** – partager l'état (messages, statut, erreurs) entre les appels `useChat`.

Vous pouvez créer un ChatStore de base avec la fonction d'aide :

```ts
import { defaultChatStore } from 'ai';

const chatStore = defaultChatStore({
  api: '/api/chat', // votre point de terminaison de chat
  maxSteps: 5, // optionnel : limiter les appels LLM dans les chaînes d'outils
  chats: {}, // optionnel : charger les sessions de conversation précédentes
});

import { useChat } from '@ai-sdk/react';
const { messages, input, handleSubmit } = useChat({ chatStore });
```

## Événements envoyés par le serveur (SSE)

AI SDK 5 utilise désormais les événements envoyés par le serveur (SSE) au lieu d'un protocole de streaming personnalisé. SSE est un standard web courant pour envoyer des données des serveurs vers les navigateurs. Cette mise à jour présente plusieurs avantages :

- **Fonctionne partout** - Utilise une technologie qui fonctionne dans tous les navigateurs majeurs et plateformes
- **Facile à déboguer** - Vous pouvez voir le flux de données dans les outils de développement de navigateur
- **Simple à élargir** - Ajouter de nouvelles fonctionnalités est plus direct
- **Plus stable** - Construit sur une technologie éprouvée que de nombreux développeurs utilisent déjà

## Contrôle agent

AI SDK 5 introduit de nouvelles fonctionnalités pour créer des agents qui vous aident à contrôler le comportement du modèle de manière plus précise.

### prepareStep

La fonction `prepareStep` vous donne un contrôle détaillé sur chaque étape dans un agent à plusieurs étapes. Elle est appelée avant que l'étape ne commence et vous permet :

- De changer dynamiquement le modèle utilisé pour des étapes spécifiques
- De forcer des sélections d'outil pour des étapes particulières
- De limiter les outils disponibles pendant des étapes spécifiques
- D'examiner le contexte des étapes précédentes avant de poursuivre

```ts
const result = await generateText({
  // ...
  experimental_prepareStep: async ({ model, stepNumber, maxSteps, steps }) => {
    if (stepNumber === 0) {
      return {
        // utilisez un modèle différent pour cette étape :
        model: modelForThisParticularStep,
        // forcez une sélection d'outil pour cette étape :
        toolChoice: { type: 'tool', toolName: 'tool1' },
        // limitez les outils disponibles pour cette étape :
        experimental_activeTools: ['tool1'],
      };
    }
    // lorsque rien n'est retourné, les paramètres par défaut sont utilisés
  },
});
```

Cela facilite la construction de systèmes d'intelligence artificielle qui s'adaptent à leurs capacités en fonction du contexte actuel et des exigences de la tâche.

### `stopWhen`

Le paramètre `stopWhen` vous permet de définir des conditions d'arrêt pour votre agent. Au lieu de se lancer à l'infini, vous pouvez spécifier exactement quand l'agent devrait s'arrêter en fonction de diverses conditions :

- Lorsque le nombre maximum de pas est atteint
- Lorsqu'une outil spécifique est appelé
- Lorsque toute condition personnalisée que vous définissez est satisfaite

```ts
const result = generateText({
  // ...
  // arrêter le boucle à 5 pas
  stopWhen: stepCountIs(5),
});

const result = generateText({
  // ...
  // arrêter le boucle lorsque l'outil météo est appelé
  stopWhen: hasToolCall('weather'),
});

const result = generateText({
  // ...
  // arrêter le boucle à votre propre condition personnalisée
  stopWhen: maxTotalTokens(20000),
});
```

Ces contrôles agenciers forment la base pour construire des systèmes d'intelligence artificielle plus fiables, contrôlables et capables de résoudre des problèmes complexes tout en restant dans des contraintes bien définies.

---
titre : Vue d'ensemble
description : Vue d'ensemble de l'API SDK Core.
---

# API SDK Core

Les grands modèles de langage (LLM) sont des programmes avancés qui peuvent comprendre, créer et interagir avec le langage humain sur une grande échelle.
Ils sont entraînés sur des quantités vastes de matériel écrit pour reconnaître les modèles du langage et prédire ce qui pourrait venir ensuite dans un morceau de texte donné.

L'API SDK Core **simplifie le travail avec les LLM en offrant une façon standardisée d'intégrer les LLM dans votre application** - afin que vous puissiez vous concentrer sur la construction d'applications AI de qualité pour vos utilisateurs, et non gaspiller votre temps sur les détails techniques.

Par exemple, voici comment vous pouvez générer du texte avec divers modèles en utilisant l'API SDK :

<PreviewSwitchProviders />

## Fonctions de base de l'API AI

L'API AI Core comporte diverses fonctions conçues pour la [génération de texte](./generating-text), la [génération de données structurées](./generating-structured-data) et l'[utilisation de outils](./tools-and-tool-calling).
Ces fonctions adoptent une approche standardisée pour la configuration des [prompts](./prompts) et des [paramètres](./settings), ce qui facilite la collaboration avec différents modèles.

- [`generateText`](/docs/ai-sdk-core/generating-text) : Génère du texte et des appels d'outils.
  Cette fonction est idéale pour les cas d'utilisation non interactifs tels que les tâches d'automatisation où vous avez besoin d'écrire du texte (par exemple, rédiger un e-mail ou résumer des pages web) et pour les agents qui utilisent des outils.
- [`streamText`](/docs/ai-sdk-core/generating-text) : Flux de texte et d'appels d'outils.
  Vous pouvez utiliser la fonction `streamText` pour les cas d'utilisation interactifs tels que les [bots de chat](/docs/ai-sdk-ui/chatbot) et la [diffusion de contenu](/docs/ai-sdk-ui/completion).
- [`generateObject`](/docs/ai-sdk-core/generating-structured-data) : Génère un objet structuré typé qui correspond à un schéma [Zod](https://zod.dev/).
  Vous pouvez utiliser cette fonction pour forcer le modèle de langage à retourner des données structurées, par exemple pour l'extraction d'informations, la génération de données synthétiques ou les tâches de classification.
- [`streamObject`](/docs/ai-sdk-core/generating-structured-data) : Flux d'un objet structuré qui correspond à un schéma Zod.
  Vous pouvez utiliser cette fonction pour [diffuser des UI générés](/docs/ai-sdk-ui/object-generation).

## Référence de l'API

Veuillez consulter la [Référence de l'API Core AI](/docs/reference/ai-sdk-core) pour plus de détails sur chaque fonction.

---
Titre : Génération de texte
Description : Apprenez à générer du texte avec l'API AI.
---

# Génération et Streaming de Texte

Les grands modèles de langage (GML) peuvent générer du texte en réponse à un prompt, qui peut contenir des instructions et des informations à traiter.
Par exemple, vous pouvez demander à un modèle de concocter une recette, rédiger un courrier électronique ou résumer un document.

La bibliothèque SDK Core fournit deux fonctions pour générer du texte et le streamer à partir des GML :

- [`generateText`](#generatetext) : Génère du texte pour un prompt donné et un modèle.
- [`streamText`](#streamtext) : Streame du texte à partir d'un prompt donné et d'un modèle.

Les fonctionnalités avancées des GML, telles que [l'appel de outils](./outils-et-appel-de-fonction) et [la génération de données structurées](./génération-de-données-structurées), sont construites à partir de la génération de texte.

## `generateText`

Vous pouvez générer du texte à l'aide de la fonction [`generateText`](/docs/reference/ai-sdk-core/generate-text). Cette fonction est idéale pour les cas d'utilisation non interactifs où vous avez besoin d'écrire du texte (par exemple, rédiger un e-mail ou résumer des pages web) et pour les agents qui utilisent des outils.

```tsx
import { generateText } from 'ai';

const { text } = await generateText({
  model: votreModel,
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Vous pouvez utiliser des [prompts avancés](./prompts) pour générer du texte avec des instructions et du contenu plus complexes :

```tsx
import { generateText } from 'ai';

const { text } = await generateText({
  model: votreModel,
  system:
    'Vous êtes un écrivain professionnel. ' +
    'Vous écrivez du contenu simple, clair et concis.',
  prompt: `Résumez l'article suivant en 3-5 phrases : ${article}`,
});
```

L'objet résultat de `generateText` contient plusieurs promesses qui se résolvent lorsque tous les données requis sont disponibles :

- `result.text`: Le texte généré.
- `result.reasoning`: Le texte de raisonnement du modèle (disponible uniquement pour certains modèles).
- `result.sources`: Les sources qui ont été utilisées comme entrée pour générer la réponse (disponible uniquement pour certains modèles).
- `result.finishReason`: La raison pour laquelle le modèle a terminé de générer du texte.
- `result.usage`: L'utilisation du modèle pendant la génération de texte.

### Accéder aux en-têtes & au corps de la réponse

Parfois, vous avez besoin d'accéder au corps complet de la réponse du fournisseur de modèle,
par exemple pour accéder à certains en-têtes ou au contenu du corps spécifiques du fournisseur.

Vous pouvez accéder aux en-têtes et au corps de la réponse bruts à l'aide de la propriété `response` :

```ts
import { generateText } from 'ai';

const result = await generateText({
  // ...
});

console.log(JSON.stringify(result.response.headers, null, 2));
console.log(JSON.stringify(result.response.body, null, 2));
```

## `streamText`

Selon votre modèle et votre requête, il peut prendre jusqu'à une minute à un grand modèle de langage (LLM) pour terminer la génération de sa réponse. Cette attente peut être inacceptable pour les cas d'utilisation interactifs comme les chatbots ou les applications en temps réel, où les utilisateurs attendent des réponses immédiates.

Le SDK AI Core fournit la fonction [`streamText`](/docs/reference/ai-sdk-core/stream-text) qui simplifie l'afflux de texte à partir des LLMs :

```ts
import { streamText } from 'ai';

const result = streamText({
  model: votreModèle,
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
});

// exemple : utilisez textStream comme un itérateur asynchrone
for await (const textPart of result.textStream) {
  console.log(textPart);
}
```

<Note>
  `result.textStream` est à la fois un `ReadableStream` et un `AsyncIterable`.
</Note>

<Note type="warning">
  `streamText` commence immédiatement à affluer et supprime les erreurs pour prévenir les plantages du serveur. Utilisez la fonction de rappel `onError` pour logger les erreurs.
</Note>

Vous pouvez utiliser `streamText` seul ou en combinaison avec [AI SDK UI](/examples/next-pages/basics/streaming-text-generation) et [AI SDK RSC](/examples/next-app/basics/streaming-text-generation).

L'objet de résultat contient plusieurs fonctions d'aide pour faciliter l'intégration dans [AI SDK UI](/docs/ai-sdk-ui) :

- `result.toDataStreamResponse()`: Crée une réponse HTTP de flux de données (avec appels d'outil, etc.) qui peut être utilisée dans une route API d'application Next.js Router.
- `result.pipeDataStreamToResponse()`: Écrit le delta de sortie de flux de données dans un objet de réponse Node.js.
- `result.toTextStreamResponse()`: Crée une réponse HTTP de flux de texte simple.
- `result.pipeTextStreamToResponse()`: Écrit le delta de sortie de texte dans un objet de réponse Node.js.

<Note>
  `streamText` utilise la technique de la pression arrière et ne génère des jetons que lorsqu'ils sont demandés. Vous devez consommer le flux pour qu'il se termine.
</Note>

Il fournit également plusieurs promesses qui se résolvent lorsque le flux est terminé :

- `result.text`: Le texte généré.
- `result.reasoning`: Le texte de raisonnement du modèle (disponible uniquement pour certains modèles).
- `result.sources`: Les sources qui ont été utilisées comme entrée pour générer la réponse (disponible uniquement pour certains modèles).
- `result.finishReason`: La raison pour laquelle le modèle a terminé la génération de texte.
- `result.usage`: L'utilisation du modèle pendant la génération de texte.

### `onError` callback

`streamText` commence immédiatement à diffuser pour permettre l'envoi de données sans attendre le modèle.
Les erreurs deviennent partie du flux et ne sont pas lancées pour éviter par exemple que les serveurs ne s'arrêtent.

Pour logger les erreurs, vous pouvez fournir un callback `onError` qui est déclenché lorsqu'une erreur se produit.

```tsx highlight="6-8"
import { streamText } from 'ai';

const result = streamText({
  model: votreModel,
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  onError({ erreur }) {
    console.error(erreur); // votre logique de gestion d'erreur ici
  },
});
```

### `onChunk` callback

Lorsque vous utilisez `streamText`, vous pouvez fournir un callback `onChunk` qui est déclenché pour chaque morceau du flux.

Il reçoit les types de morceau suivants :

- `text-delta`
- `reasoning`
- `source`
- `tool-call`
- `tool-result`
- `tool-call-streaming-start` (lorsque `toolCallStreaming` est activé)
- `tool-call-delta` (lorsque `toolCallStreaming` est activé)

```tsx highlight="6-11"
import { streamText } from 'ai';

const result = streamText({
  model: votreModel,
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  onChunk({ morceau }) {
    // implémentez votre propre logique ici, par exemple :
    if (morceau.type === 'text-delta') {
      console.log(morceau.text);
    }
  },
});
```

### `onFinish` callback

Lorsque vous utilisez `streamText`, vous pouvez fournir un callback `onFinish` qui est déclenché lorsque le flux est terminé (
[Référence de l'API](/docs/reference/ai-sdk-core/stream-text)

# Lorsque la conversation est terminée)
).
Il contient le texte, les informations d'utilisation, la raison de fin, les messages, et plus encore :

```tsx highlight="6-8"
import { streamText } from 'ai';

const result = streamText({
  model: votreModèle,
  prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  onFinish({ text, finishReason, usage, response }) {
    // votre propre logique, par exemple pour sauvegarder l'historique de la conversation ou enregistrer les données d'utilisation

    const messages = response.messages; // messages générés
  },
});
```

### Propriété `fullStream`

Vous pouvez lire un flux avec tous les événements en utilisant la propriété `fullStream`.
Cela peut être utile si vous souhaitez mettre en œuvre votre propre interface utilisateur ou traiter le flux de manière différente.
Voici un exemple de comment utiliser la propriété `fullStream` :

```tsx
import { streamText } from 'ai';
import { z } from 'zod';

const result = streamText({
  model: votreModel,
  outils : {
    cityAttractions : {
      paramètres : z.object({ ville : z.string() }),
      exécuter : async ({ ville }) => ({
        attractions : ['attraction1', 'attraction2', 'attraction3'],
      }),
    },
  },
  invitation : 'Quels sont les principaux lieux touristiques de San Francisco ?',
});
```

```javascript
async function traiterPartie(result) {
  for await (const part of result.fullStream) {
    switch (part.type) {
      case 'text-delta' : {
        // gérer le delta de texte ici
        break;
      }
      case 'raisonnement' : {
        // gérer le raisonnement ici
        break;
      }
      case 'source' : {
        // gérer la source ici
        break;
      }
      case 'appel-outil' : {
        switch (part.toolName) {
          case 'cityAttractions' : {
            // gérer l'appel d'outil ici
            break;
          }
        }
        break;
      }
      case 'résultat-outil' : {
        switch (part.toolName) {
          case 'cityAttractions' : {
            // gérer le résultat d'outil ici
            break;
          }
        }
        break;
      }
      case 'fin' : {
        // gérer la fin ici
        break;
      }
      case 'erreur' : {
        // gérer l'erreur ici
        break;
      }
    }
  }
}
```

### Transformation de flux

Vous pouvez utiliser l'option `experimental_transform` pour transformer le flux.
Cela est utile pour par exemple filtrer, modifier ou lisser le flux de texte.

Les transformations sont appliquées avant que les appels de rappel ne soient invoqués et les promesses ne soient résolues.
Si par exemple vous avez une transformation qui change tout le texte en majuscules, le callback `onFinish` recevra le texte transformé.

#### Lissage des flux

La bibliothèque AI SDK Core fournit une fonction [`smoothStream`](/docs/reference/ai-sdk-core/smooth-stream) qui peut être utilisée pour lisser les flux de texte.

```tsx highlight="6"
import { smoothStream, streamText } from 'ai';

const result = streamText({
  model,
  prompt,
  experimental_transform: smoothStream(),
});
```

#### Transformations personnalisées

Vous pouvez également implémenter vos propres transformations personnalisées.
La fonction de transformation reçoit les outils disponibles pour le modèle,
et retourne une fonction utilisée pour transformer le flux.
Les outils peuvent être soit génériques, soit limités aux outils que vous utilisez.

Voici un exemple d'implémentation d'une transformation personnalisée qui convertit
toutes les chaînes de caractères en majuscules :

```ts
const upperCaseTransform =
  <TOOLS extends ToolSet>() =>
  (options: { tools: TOOLS; stopStream: () => void }) =>
    new TransformStream<TextStreamPart<TOOLS>, TextStreamPart<TOOLS>>({
      transform(chunk, controller) {
        controller.enqueue(
          // pour les tronçons de texte-delta, convertissez la chaîne de caractères en majuscules :
          chunk.type === 'text-delta'
            ? { ...chunk, textDelta: chunk.textDelta.toUpperCase() }
            : chunk,
        );
      },
    });
```

Vous pouvez également arrêter le flux en utilisant la fonction `stopStream`.
Cela est par exemple utile si vous voulez arrêter le flux lorsque les garde-fous du modèle sont violés, par exemple en générant un contenu inapproprié.

Lorsque vous invoquez `stopStream`, il est important de simuler les événements `step-finish` et `finish` pour garantir que le flux bien formé est retourné
et que toutes les callbacks sont invoquées.

```ts
const transformationDeMotCesse =
  <ENSEMBLEDETOOL extends EnsemblierDeTool>() =>
  ({ arrêtDeLaFenêtre }: { arrêtDeLaFenêtre: () => void }) =>
    new TransformStream<PartieDeFluxDeTexte<ENSEMBLEDETOOL>, PartieDeFluxDeTexte<ENSEMBLEDETOOL>>({
      // note : cette transformation simplifiée est destinée à des tests;
      // dans une version réelle, il faudrait plus de tamponnage de flux et de balayage pour émettre correctement le texte antérieur
      // et détecter toutes les occurrences de MOT_CESSE.
      transform(partieDuFlux, contrôleur) {
        if (partieDuFlux.type !== 'delta-de-texte') {
          contrôleur.enqueue(partieDuFlux);
          return;
        }

        if (partieDuFlux.deltaDeTexte.includes('MOT_CESSE')) {
          // arrêter le flux
          arr

// simuler l'événement step-finish
          controller.enqueue({
            type: 'step-finish',
            finishReason: 'stop',
            logprobs: undefined,
            usage: {
              completionTokens: NaN,
              promptTokens: NaN,
              totalTokens: NaN,
            },
            request: {},
            response: {
              id: 'response-id',
              modelId: 'mock-model-id',
              timestamp: new Date(0),
            },
            warnings: [],
            isContinued: false,
          });

// simulez l'événement de fin
          controller.enqueue({
            type: 'finish',
            finishReason: 'stop',
            logprobs: undefined,
            usage: {
              completionTokens: NaN,
              promptTokens: NaN,
              totalTokens: NaN,
            },
            response: {
              id: 'response-id',
              modelId: 'mock-model-id',
              timestamp: new Date(0),
            },
          });

          return;
        }

        controller.enqueue(chunk);
      },
    });

#### Multiples transformations

Vous pouvez également fournir plusieurs transformations. Elles sont appliquées dans l'ordre dans lequel elles sont fournies.

```tsx highlight="4"
const result = streamText({
  model,
  prompt,
  experimental_transform: [firstTransform, secondTransform],
});
```

## Sources

Certains fournisseurs tels que [Perplexity](/providers/ai-sdk-providers/perplexity#sources) et
[Google Generative AI](/providers/ai-sdk-providers/google-generative-ai

# Sources
Les sources sont incluses dans la réponse.

Actuellement, les sources sont limitées aux pages web qui fondent la réponse.
Vous pouvez y accéder à l'aide de la propriété `sources` du résultat.

Chaque source `url` contient les propriétés suivantes :

- `id`: L'ID de la source.
- `url`: L'URL de la source.
- `title`: Le titre optionnel de la source.
- `providerMetadata`: Les métadonnées du fournisseur de la source.

Lorsque vous utilisez `generateText`, vous pouvez accéder aux sources à l'aide de la propriété `sources` :

```ts
const result = await generateText({
  model: google('gemini-2.0-flash-exp', { useSearchGrounding: true }),
  prompt: 'Listez les 5 premières nouvelles de San Francisco de la semaine passée.',
});

for (const source of result.sources) {
  if (source.sourceType === 'url') {
    console.log('ID:', source.id);
    console.log('Titre:', source.title);
    console.log('URL:', source.url);
    console.log('Métadonnées du fournisseur:', source.providerMetadata);
    console.log();
  }
}
```

Lorsque vous utilisez `streamText`, vous pouvez accéder aux sources à l'aide de la propriété `fullStream` :

```tsx
const result = streamText({
  model: google('gemini-2.0-flash-exp', { useSearchGrounding: true }),
  prompt: 'Listez les 5 premières nouvelles de San Francisco de la semaine passée.',
});

for await (const part of result.fullStream) {
  if (part.type === 'source' && part.source.sourceType === 'url') {
    console.log('ID:', part.source.id);
    console.log('Titre:', part.source.title);
    console.log('URL:', part.source.url);
    console.log('Métadonnées du fournisseur:', part.source.providerMetadata);
    console.log();
  }
}
```

Les sources sont également disponibles dans la promesse `result.sources`.

## Génération de texte long

La plupart des modèles de langage ont une limite de sortie beaucoup plus courte que leur fenêtre de contexte.
Cela signifie que vous ne pouvez pas générer de texte long en une seule fois,
mais il est possible d'ajouter des réponses au texte d'entrée et de continuer à générer
pour créer du texte plus long.

`generateText` et `streamText` supportent de telles continuités pour la génération de texte long en utilisant la configuration expérimentale `continueSteps` :

```tsx highlight="5-6,9-10"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const {
  text, // texte combiné
  usage, // utilisation combinée de toutes les étapes
} = await generateText({
  model: openai('gpt-4o'), // 4096 tokens de sortie
  maxSteps: 5, // activer les appels multi-étapes
  experimental_continueSteps: true,
  prompt:
    'Écrivez un livre sur l'histoire romaine, ' +
    'de la fondation de la ville de Rome ' +
    'à la chute de l'Empire romain d'Occident. ' +
    'Chaque chapitre DOIT avoir au moins 1000 mots.',
});
```

<Note>
  Lorsque `experimental_continueSteps` est activé, seuls les mots complets sont transmis dans
  `streamText`, et les deux `generateText` et `streamText` peuvent supprimer les derniers tokens
  de certaines appels pour prévenir les problèmes de blanc.
</Note>

<Note type="warning">
  Certains modèles ne s'arrêtent pas toujours correctement d'eux-mêmes et continuent à générer
  jusqu'à ce que `maxSteps` soit atteint. Vous pouvez donner un indice au modèle pour s'arrêter en utilisant
  par exemple un message système tel que "Arrêtez-vous lorsque suffisamment d'informations ont été fournies."
</Note>

## Exemples

Vous pouvez voir `generateText` et `streamText` en action en utilisant divers frameworks dans les exemples suivants :

### `generateText`

<ExampleLinks
  examples={[
    {
      title: 'Apprenez à générer du texte en Node.js',
      link: '/examples/node/generating-text/generate-text',
    },
    {
      title:
        'Apprenez à générer du texte en Next.js avec les Gestionnaires de Route (AI SDK UI)',
      link: '/examples/next-pages/basics/generating-text',
    },
    {
      title:
        'Apprenez à générer du texte en Next.js avec les Actions de Serveur (AI SDK RSC)',
      link: '/examples/next-app/basics/generating-text',
    },
  ]}
/>

### `streamText`

<ExampleLinks
  examples={[
    {
      title: 'Apprenez à générer du texte en flux en Node.js',
      link: '/examples/node/generating-text/stream-text',
    },
    {
      title: 'Apprenez à générer du texte en flux en Next.js avec les Gestionnaires de Route (AI SDK UI)',
      link: '/examples/next-pages/basics/streaming-text-generation',
    },
    {
      title: 'Apprenez à générer du texte en flux en Next.js avec les Actions de Serveur (AI SDK RSC)',
      link: '/examples/next-app/basics/streaming-text-generation',
    },
  ]}
/>

---
titre : Génération de données structurées
description : Apprenez à générer des données structurées avec l'AI SDK.
---

# Génération de Données Structurées

Bien que la génération de texte puisse être utile, votre cas d'utilisation nécessitera probablement la génération de données structurées.
Par exemple, vous pourriez vouloir extraire des informations à partir de texte, classer des données ou générer des données synthétiques.

De nombreux modèles de langage sont capables de générer des données structurées, souvent définies en utilisant des "modes JSON" ou des "outils".
Cependant, vous devez fournir manuellement des schémas et valider ensuite les données générées, car les LLM peuvent produire des données structurées incorrectes ou incomplètes.

Le SDK AI standardise la génération d'objets structurés à travers les fournisseurs de modèles avec les fonctions `generateObject` et `streamObject` (`/docs/reference/ai-sdk-core/generate-object` et `/docs/reference/ai-sdk-core/stream-object`).
Vous pouvez utiliser les deux fonctions avec différentes stratégies de sortie, par exemple `array`, `object` ou `no-schema`, et avec différents modes de génération, par exemple `auto`, `tool` ou `json`.
Vous pouvez utiliser des schémas [Zod](/docs/reference/ai-sdk-core/zod-schema), [Valibot](/docs/reference/ai-sdk-core/valibot-schema) ou [JSON](/docs/reference/ai-sdk-core/json-schema) pour spécifier la forme des données que vous souhaitez,
et le modèle AI générera des données qui correspondent à cette structure.

<Note>
  Vous pouvez passer directement des objets Zod aux fonctions du SDK AI ou utiliser la fonction `zodSchema`.
</Note>

## Générer un Objet

La fonction `generateObject` génère des données structurées à partir d'une prompt.
Le schéma est également utilisé pour valider les données générées, garantissant la sécurité de type et la correction.

```ts
import { generateObject } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: votreModel,
  schema: z.object({
    recette: z.object({
      nom: z.string(),
      ingrédients: z.array(z.object({ nom: z.string(), quantité: z.string() })),
      étapes: z.array(z.string()),
    }),
  }),
  prompt: 'Générer une recette de lasagna.',
});
```

<Note>
  Voir `generateObject` en action avec [ces exemples](#more-examples)
</Note>

### Accéder aux en-têtes et au corps de la réponse

Parfois, vous avez besoin d'accéder à la réponse complète du fournisseur de modèle,
par exemple pour accéder à certains en-têtes ou au contenu du corps spécifiques au fournisseur.

Vous pouvez accéder aux en-têtes et au corps de la réponse bruts en utilisant la propriété `response` :

```ts
import { generateText } from 'ai';

const result = await generateText({
  // ...
});

console.log(JSON.stringify(result.response.headers, null, 2));
console.log(JSON.stringify(result.response.body, null, 2));
```

## Objet de Flux

Étant donné la complexité ajoutée de la restitution de données structurées, le temps de réponse du modèle peut être inacceptable pour votre cas d'utilisation interactif.
Avec la fonction [`streamObject`](/docs/reference/ai-sdk-core/stream-object), vous pouvez diffuser la réponse du modèle au fur et à mesure qu'elle est générée.

```ts
import { streamObject } from 'ai';

const { partialObjectStream } = streamObject({
  // ...
});

// utilisez partialObjectStream comme un itérateur asynchrone
for await (const partialObject of partialObjectStream) {
  console.log(partialObject);
}
```

Vous pouvez utiliser `streamObject` pour diffuser les UI générés en combinaison avec les composants de serveur React (voir [UI Génératif](../ai-sdk-rsc)) ou le hook [`useObject`](/docs/reference/ai-sdk-ui/use-object).

<Note>Consultez `streamObject` en action avec [ces exemples](#more-examples)</Note>

### Callback `onError`

`streamObject` démarre immédiatement la diffusion.
Les erreurs deviennent partie du flux et ne sont pas lancées pour éviter par exemple que les serveurs ne s'arrêtent.

Pour logger les erreurs, vous pouvez fournir un callback `onError` qui est déclenché lorsqu'une erreur se produit.

```tsx highlight="5-7"
import { streamObject } from 'ai';

const result = streamObject({
  // ...
  onError({ error }) {
    console.error(error); // votre logique de journalisation d'erreur ici
  },
});
```

## Stratégie d'Output

Vous pouvez utiliser les deux fonctions avec différentes stratégies d'output, par exemple `array`, `object` ou `no-schema`.

### Objet

La stratégie d'output par défaut est `object`, qui retourne les données générées sous forme d'objet.
Vous n'avez pas besoin de spécifier la stratégie d'output si vous souhaitez utiliser la valeur par défaut.

### Tableau

Si vous souhaitez générer un tableau d'objets, vous pouvez définir la stratégie de sortie sur `array`.
Lorsque vous utilisez la stratégie de sortie `array`, le schéma spécifie la forme d'un élément du tableau.
Avec `streamObject`, vous pouvez également diffuser les éléments du tableau générés à l'aide de `elementStream`.

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
      .describe('Classe de personnage, par exemple guerrier, mage ou voleur.'),
    description: z.string(),
  }),
  prompt: 'Générez 3 descriptions de héros pour un jeu de rôle de fantasy.',
});

for await (const hero of elementStream) {
  console.log(hero);
}
```

### Enumération

Si vous souhaitez générer une valeur d'enum spécifique, par exemple pour les tâches de classification,
vous pouvez définir la stratégie de sortie sur `enum`
et fournir une liste de valeurs possibles dans le paramètre `enum`.

<Note>La sortie Enum n'est disponible qu'avec `generateObject`.</Note>

```ts highlight="5-6"
import { generateObject } from 'ai';

const { object } = await generateObject({
  model: votreModel,
  output: 'enum',
  enum: ['action', 'comédie', 'drame', 'horreur', 'science-fiction'],
  prompt:
    'Classifiez le genre de ce résumé de film : ' +
    '"Un groupe d'astronautes voyage à travers un trou de ver pour rechercher un ' +
    'nouveau planète habitable pour l'humanité."',
});
```

### Pas de schéma

Dans certains cas, vous pouvez ne pas vouloir utiliser un schéma,
par exemple lorsque les données sont une requête utilisateur dynamique.
Vous pouvez utiliser la configuration `output` pour définir le format de sortie sur `no-schema` dans ces cas
et omettre le paramètre schéma.

```ts highlight="6"
import { openai } from '@ai-sdk/openai';
import { generateObject } from 'ai';

const { object } = await generateObject({
  model: openai('gpt-4-turbo'),
  output: 'no-schema',
  prompt: 'Générez une recette de lasagne.',
});
```

## Mode de génération

Bien que certains modèles (comme OpenAI) supportent nativement la génération d'objets, d'autres nécessitent des méthodes alternatives, comme l'appel de l'outil modifié ([appel d'outil](/docs/ai-sdk-core/tools-and-tool-calling)). La fonction `generateObject` vous permet de spécifier la méthode qu'elle utilisera pour retourner des données structurées.

- `auto` : Le fournisseur choisira le meilleur mode pour le modèle. Ce mode recommandé est utilisé par défaut.
- `tool` : Un outil avec le schéma JSON en tant que paramètres est fourni et le fournisseur est instruit de l'utiliser.
- `json` : Le format de réponse est défini sur JSON lorsqu'il est pris en charge par le fournisseur, par exemple via les modes JSON ou la génération guidée par la grammaire. Si la génération guidée par la grammaire n'est pas prise en charge, le schéma JSON et les instructions pour générer un JSON conforme au schéma sont injectés dans le système de prompt.

<Note>
  Veuillez noter que pas tous les fournisseurs supportent tous les modes de génération. Certains
  fournisseurs ne supportent pas la génération d'objets du tout.
</Note>

## Nom du schéma et description

Vous pouvez optionnellement spécifier un nom et une description pour le schéma. Ces informations sont utilisées par certains fournisseurs pour une orientation supplémentaire des LLM, par exemple via le nom du outil ou du schéma.

```ts highlight="6-7"
import { generateObject } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: votreModel,
  schemaName: 'Recette',
  schemaDescription: 'Une recette pour un plat.',
  schema: z.object({
    name: z.string(),
    ingredients: z.array(z.object({ name: z.string(), amount: z.string() })),
    steps: z.array(z.string()),
  }),
  prompt: 'Générez une recette de lasagna.',
});
```

## Gestion des Erreurs

Lorsque `generateObject` ne parvient pas à générer un objet valide, elle lance une exception de type [`AI_NoObjectGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-object-generated-error).

Cette erreur se produit lorsque le fournisseur de l'IA échoue à générer un objet pouvant être analysé qui correspond au schéma.
Elle peut survenir en raison des raisons suivantes :

- Le modèle a échoué à générer une réponse.
- Le modèle a généré une réponse qui ne pouvait pas être analysée.
- Le modèle a généré une réponse qui ne pouvait pas être validée par rapport au schéma.

L'erreur conserve les informations suivantes pour vous aider à enregistrer l'erreur :

- `text`: Le texte généré par le modèle. Il peut s'agir du texte brut ou du texte de l'appel de l'outil, en fonction du mode de génération d'objet.
- `response`: Informations sur la réponse du modèle de langage, y compris l'identifiant de réponse, la date et l'heure, et le modèle.
- `usage`: Utilisation du jeton de requête.
- `cause`: La cause de l'erreur (par exemple, une erreur de parsing JSON). Vous pouvez utiliser cela pour une gestion d'erreur plus détaillée.

```ts
import { generateObject, NoObjectGeneratedError } from 'ai';

try {
  await generateObject({ model, schema, prompt });
} catch (error) {
  if (NoObjectGeneratedError.isInstance(error)) {
    console.log('NoObjectGeneratedError');
    console.log('Cause:', error.cause);
    console.log('Text:', error.text);
    console.log('Response:', error.response);
    console.log('Usage:', error.usage);
  }
}
```

## Réparation de JSON invalides ou mal formés

<Note type="avertissement">
  La fonction `repairText` est expérimentale et peut changer à l'avenir.
</Note>

Parfois, le modèle générera un JSON invalide ou mal formé.
Vous pouvez utiliser la fonction `repairText` pour essayer de réparer le JSON.

Elle reçoit l'erreur, soit un `JSONParseError` ou un `TypeValidationError`,
et le texte qui a été généré par le modèle.
Vous pouvez alors essayer de réparer le texte et retourner le texte réparé.

```ts highlight="7-10"
import { generateObject } from 'ai';

const { object } = await generateObject({
  model,
  schema,
  prompt,
  experimental_repairText: async ({ text, error }) => {
    // exemple : ajouter une accolade fermante au texte
    return text + '}';
  },
});
```

## Sorties structurées avec `generateText` et `streamText`

Vous pouvez générer des données structurées avec `generateText` et `streamText` en utilisant la mise en œuvre `experimental_output`.

<Note>
  Certains modèles, par exemple ceux fournis par OpenAI, supportent les sorties structurées et l'appel à des outils
  en même temps. Cela n'est possible que avec `generateText` et `streamText`.
</Note>

<Note type="avertissement">
  La génération de sorties structurées avec `generateText` et `streamText` est
  expérimentale et peut changer à l'avenir.
</Note>

### `generateText`

```ts highlight="2,4-18"
// experimental_output est un objet structuré qui correspond au schéma :
const { experimental_output } = await generateText({
  // ...
  experimental_output: Output.object({
    schema: z.object({
      nom : z.string(),
      age : z.number().nullable().describe('Âge de la personne.'),
      contact : z.object({
        type : z.literal('email'),
        valeur : z.string(),
      }),
      occupation : z.object({
        type : z.literal('employé'),
        entreprise : z.string(),
        poste : z.string(),
      }),
    }),
  }),
  prompt : 'Générer un exemple de personne pour les tests.',
});
```

### `streamText`

```ts highlight="2,4-18"
// experimental_partialOutputStream contient des objets générés partiels :
const { experimental_partialOutputStream } = await streamText({
  // ...
  experimental_output: Output.object({
    schema: z.object({
      nom : z.string(),
      age : z.number().nullable().describe('Âge de la personne.'),
      contact : z.object({
        type : z.literal('email'),
        valeur : z.string(),
      }),
      occupation : z.object({
        type : z.literal('employé'),
        entreprise : z.string(),
        poste : z.string(),
      }),
    }),
  }),
  prompt : 'Générer un exemple de personne pour les tests.',
});
```

## Exemples supplémentaires

Vous pouvez voir `generateObject` et `streamObject` en action à l'aide de divers frameworks dans les exemples suivants :

### `generateObject`

<ExampleLinks
  examples={[
    {
      titre : 'Apprenez à générer des objets en Node.js',
      lien : '/examples/node/generating-structured-data/generate-object',
    },
    {
      titre :
        'Apprenez à générer des objets en Next.js avec les gestionnaires de route (AI SDK UI)',
      lien : '/examples/next-pages/basics/generating-object',
    },
    {
      titre :
        'Apprenez à générer des objets en Next.js avec les actions de serveur (AI SDK RSC)',
      lien : '/examples/next-app/basics/generating-object',
    },
  ]}
/>

### `streamObject`

<ExampleLinks
  examples={[
    {
      titre : 'Apprenez à streamer des objets en Node.js',
      lien : '/examples/node/streaming-structured-data/stream-object',
    },
    {
      titre :
        'Apprenez à streamer des objets en Next.js avec les gestionnaires de route (AI SDK UI)',
      lien : '/examples/next-pages/basics/streaming-object-generation',
    },
    {
      titre :
        'Apprenez à streamer des objets en Next.js avec les actions de serveur (AI SDK RSC)',
      lien : '/examples/next-app/basics/streaming-object-generation',
    },
  ]}
/>

---
titre : Appel de l'outil
description : Apprenez à utiliser l'appel d'outil et les appels multi-étapes (en utilisant maxSteps) avec AI SDK Core.
---

# Appel de l'outil

Comme abordé dans les Fondements, [les outils](/docs/fondements/outils) sont des objets qui peuvent être appelés par le modèle pour effectuer une tâche spécifique.
Les outils de la couche de noyau SDK AI contiennent trois éléments :

- **`description`** : Une description facultative de l'outil qui peut influencer lorsqu'il est sélectionné.
- **`parameters`** : Un [schéma Zod](/docs/fondements/outils)

# Schemas) ou un [schéma JSON](/docs/reference/ai-sdk-core/json-schema) qui définit les paramètres. Le schéma est consommé par le LLM, et utilisé également pour valider les appels des outils LLM.
- **`execute`** : Une fonction asynchrone facultative qui est appelée avec les arguments provenant de l'appel de l'outil. Elle produit une valeur de type `RESULT` (type générique). Elle est facultative car vous pourriez vouloir faire passer les appels d'outil au client ou à une file d'attente au lieu de les exécuter dans le même processus.

<Note className="mb-2">
  Vous pouvez utiliser la fonction d'aide [`tool`](/docs/reference/ai-sdk-core/tool) pour
  inférer les types des paramètres de l'`execute`.
</Note>

Le paramètre `tools` de `generateText` et `streamText` est un objet qui a les noms d'outils comme clés et les outils comme valeurs :

```ts highlight="6-17"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const result = await generateText({
  model: votreModel,
  tools: {
    weather: tool({
      description: 'Obtenir le temps dans une localité',
      parameters: z.object({
        location: z.string().describe('La localité pour obtenir le temps'),
      }),
      execute: async ({ location }) => ({
        location,
        temperature: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  prompt: 'Quel est le temps à San Francisco ?',
});
```

<Note>
  Lorsqu'un modèle utilise un outil, il s'agit d'un "appel d'outil" et la sortie de l'outil est appelée "résultat d'outil".
</Note>

L'appel d'outil n'est pas limité à la génération de texte.
Vous pouvez également l'utiliser pour rendre des interfaces utilisateur (UI générative).

## Appels Multi-Étapes (en utilisant maxSteps)

Avec la configuration `maxSteps`, vous pouvez activer les appels multi-étapes dans `generateText` et `streamText`. Lorsque `maxSteps` est défini sur un nombre supérieur à 1 et que le modèle génère un appel de tool, l'API SDK déclenchera une nouvelle génération en passant en argument le résultat de l'appel de tool jusqu'à ce qu'il n'y ait plus d'appels de tool ou que le nombre maximum d'étapes de tool soit atteint.

<Note>
  Pour décider de la valeur à attribuer à `maxSteps`, considérez la tâche la plus complexe que l'appel pourrait gérer et le nombre d'étapes séquentielles requises pour sa réalisation, plutôt que le nombre de tools disponibles.
</Note>

Par défaut, lorsque vous utilisez `generateText` ou `streamText`, cela déclenche une génération unique (`maxSteps: 1`). Cela fonctionne bien pour de nombreux cas d'utilisation où vous pouvez vous fier aux données d'apprentissage du modèle pour générer une réponse. Cependant, lorsque vous fournissez des tools, le modèle a maintenant le choix de générer une réponse de texte normale ou d'appeler un tool. Si le modèle génère un appel de tool, sa génération est terminée et cette étape est terminée.

Vous pouvez vouloir que le modèle génère du texte après l'exécution du tool, soit pour résumer les résultats du tool dans le contexte de la question de l'utilisateur. Dans de nombreux cas, vous pouvez également vouloir que le modèle utilise plusieurs tools dans une seule réponse. C'est là que les appels multi-étapes entrent en jeu.

Vous pouvez penser aux appels multi-étapes d'une manière similaire à une conversation avec une personne. Lorsque vous posez une question, si la personne ne dispose pas de la connaissance requise dans sa connaissance commune (données d'apprentissage du modèle), la personne peut avoir besoin de rechercher des informations (utiliser un tool) avant de pouvoir vous fournir une réponse. De la même manière, le modèle peut avoir besoin d'appeler un tool pour obtenir les informations dont il a besoin pour répondre à votre question, chaque génération (appel de tool ou génération de texte) étant une étape.

### Exemple

Dans l'exemple suivant, il y a deux étapes :

1. **Étape 1**
   1. La prompt `'Quel est le temps à San Francisco?'` est envoyée au modèle.
   1. Le modèle génère une appelle d'outil.
   1. L'appel d'outil est exécuté.
1. **Étape 2**
   1. Le résultat de l'outil est envoyé au modèle.
   1. Le modèle génère une réponse en considérant le résultat de l'outil.

```ts highlight="18"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const { text, steps } = await generateText({
  model: votreModel,
  tools: {
    weather: tool({
      description: 'Obtenir le temps dans une localité',
      parameters: z.object({
        location: z.string().describe('La localité pour obtenir le temps'),
      }),
      execute: async ({ location }) => ({
        location,
        temperature: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  maxSteps: 5, // autoriser jusqu'à 5 étapes
  prompt: 'Quel est le temps à San Francisco?',
});
```

<Note>Vous pouvez utiliser `streamText` de manière similaire.</Note>

### Étapes

Pour accéder aux appels d'outils intermédiaires et résultats, vous pouvez utiliser la propriété `steps` de l'objet résultat
ou le callback `onFinish` de `streamText`.
Il contient tous les textes, appels d'outils, résultats d'outils, etc. de chaque étape.

#### Exemple : Extraire les résultats des outils de toutes les étapes

```ts highlight="3,9-10"
import { generateText } from 'ai';

const { steps } = await generateText({
  model: openai('gpt-4-turbo'),
  maxSteps: 10,
  // ...
});

// extraire toutes les appels d'outils des étapes :
const tousLesAppelsDoutils = steps.flatMap(step => step.toolCalls);
```

### `onStepFinish` callback

Lorsque vous utilisez `generateText` ou `streamText`, vous pouvez fournir un callback `onStepFinish` qui
est déclenché lorsque une étape est terminée,
c'est-à-dire que tous les deltas de texte, les appels d'outils et les résultats des outils pour l'étape sont disponibles.
Lorsque vous avez plusieurs étapes, le callback est déclenché pour chaque étape.

```tsx highlight="5-7"
import { generateText } from 'ai';

const result = await generateText({
  // ...
  onStepFinish({ text, toolCalls, toolResults, finishReason, usage }) {
    // votre propre logique, par exemple pour sauvegarder l'historique de conversation ou enregistrer l'utilisation
  },
});
```

### `experimental_prepareStep` callback

<Note type="warning">
  Le callback `experimental_prepareStep` est expérimental et peut changer à l'avenir. Il n'est disponible que dans la fonction `generateText`.
</Note>

Le callback `experimental_prepareStep` est appelé avant l'exécution d'une étape.

Il est appelé avec les paramètres suivants :

- `model`: Le modèle qui a été passé dans `generateText`.
- `maxSteps`: Le nombre maximum d'étapes qui a été passé dans `generateText`.
- `stepNumber`: Le numéro de l'étape qui est en cours d'exécution.
- `steps`: Les étapes qui ont été exécutées jusqu'à présent.

Vous pouvez l'utiliser pour fournir des paramètres différents pour une étape.

```tsx highlight="5-7"
import { generateText } from 'ai';

const result = await generateText({
  // ...
  experimental_prepareStep: async ({ model, stepNumber, maxSteps, steps }) => {
    if (stepNumber === 0) {
      return {
        // utilisez un modèle différent pour cette étape :
        model: modelForThisParticularStep,
        // imposez un choix d'outil pour cette étape :
        toolChoice: { type: 'outil', toolName: 'tool1' },
        // limitez les outils disponibles pour cette étape :
        experimental_activeTools: ['tool1'],
      };
    }

    // lorsqu'il n'y a rien de renvoyé, les paramètres par défaut sont utilisés
  },
});
```

## Messages de Réponse

L'ajout des messages générés par l'assistant et les outils à votre historique de conversation est une tâche courante,
surtout si vous utilisez des appels d'outils multi-étapes.

Les méthodes `generateText` et `streamText` disposent d'une propriété `response.messages` que vous pouvez utiliser pour
ajouter les messages de l'assistant et des outils à votre historique de conversation.
Cette propriété est également disponible dans le callback `onFinish` de `streamText`.

La propriété `response.messages` contient un tableau d'objets `CoreMessage` que vous pouvez ajouter à votre historique de conversation :

```ts
import { generateText } from 'ai';

const messages: CoreMessage[] = [
  // ...
];

const { response } = await generateText({
  // ...
  messages,
});

// ajoutez les messages de réponse à votre historique de conversation :
messages.push(...response.messages); // streamText : ...((await response).messages)
```

## Choix de l'Outil

Vous pouvez utiliser la mise en page `toolChoice` pour influencer quand un outil est sélectionné.
Il prend en charge les paramètres suivants :

- `auto` (par défaut) : le modèle peut choisir de faire appel à un outil et lequel appeler.
- `required`: le modèle doit faire appel à un outil. Il peut choisir lequel appeler.
- `none`: le modèle ne doit pas faire appel à d'outils
- `{ type: 'tool', toolName: string (typed) }`: le modèle doit faire appel à l'outil spécifié

```ts highlight="18"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const result = await generateText({
  model: votreModèle,
  tools: {
    météo: tool({
      description: 'Obtenir le temps dans une localité',
      parameters: z.object({
        location: z.string().describe('La localité pour laquelle obtenir le temps'),
      }),
      execute: async ({ location }) => ({
        location,
        temperature: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  toolChoice: 'required', // force le modèle à appeler un outil
  prompt: 'Quel est le temps à San Francisco ?',
});
```

## Options d'Exécution des Outils

Lorsque les outils sont appelés, ils reçoivent des options supplémentaires en tant que deuxième paramètre.

### ID de l'appel de l'outil

L'ID de l'appel de l'outil est transmis à l'exécution de l'outil.
Vous pouvez l'utiliser par exemple lorsque vous envoyez des informations liées à l'appel de l'outil avec les données de flux.

```ts highlight="14-20"
import { StreamData, streamText, tool } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const data = new StreamData();

  const result = streamText({
    // ...
    messages,
    tools: {
      monOutil: tool({
        // ...
        execute: async (args, { toolCallId }) => {
          // retourner par exemple un statut personnalisé pour l'appel de l'outil
          data.appendMessageAnnotation({
            type: 'statut-outil',
            toolCallId,
            status: 'en-cours',
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

### Messages

Les messages qui ont été envoyés au modèle de langage pour lancer la réponse contenant l'appel de la fonctionnalité sont transmis à l'exécution de la fonctionnalité.
Vous pouvez y accéder dans le deuxième paramètre de la fonction `execute`.
Dans les appels multi-étapes, les messages contiennent le texte, les appels de fonctionnalité et les résultats de fonctionnalité de toutes les étapes précédentes.

```ts highlight="8-9"
import { generateText, tool } from 'ai';

const result = await generateText({
  // ...
  tools: {
    myTool: tool({
      // ...
      execute: async (args, { messages }) => {
        // utiliser l'historique des messages dans des appels à d'autres modèles de langage
        return something;
      },
    }),
  },
});
```

### Signaux d'abord

Les signaux d'abord provenant de `generateText` et `streamText` sont transmis à l'exécution de l'outil.
Vous pouvez y accéder dans le deuxième paramètre de la fonction `execute` et par exemple, annuler les calculs longs en cours ou les transmettre aux appels de récupération à l'intérieur des outils.

```ts highlight="6,11,14"
import { z } from 'zod';
import { generateText, tool } from 'ai';

const result = await generateText({
  model: votreModel,
  abortSignal: monAbortSignal, // signal qui sera transmis aux outils
  tools: {
    weather: tool({
      description: 'Obtenir le temps dans une localité',
      parameters: z.object({ location: z.string() }),
      execute: async ({ location }, { abortSignal }) => {
        return fetch(
          `https://api.weatherapi.com/v1/current.json?q=${location}`,
          { signal: abortSignal }, // transmettre le signal d'abord à fetch
        );
      },
    }),
  },
  prompt: 'Quel est le temps à San Francisco?',
});
```

## Types

La modularisation de votre code nécessite souvent la définition de types pour garantir la sécurité des types et la réutilisabilité.
Pour permettre cela, le SDK AI fournit plusieurs types de helper pour les outils, les appels d'outils et les résultats d'outils.

Vous pouvez les utiliser pour forcer le typage de vos variables, des paramètres de fonctions et des types de retour
dans les parties du code qui ne sont pas directement liées à `streamText` ou `generateText`.

Chaque appel d'outil est typé avec `ToolCall<NAME extends string, ARGS>`, en fonction
de l'outil qui a été invoqué.
De même, les résultats d'outils sont typés avec `ToolResult<NAME extends string, ARGS, RESULT>`.

Les outils dans `streamText` et `generateText` sont définis comme un `ToolSet`.
Les helpers de typage d'inference `ToolCallUnion<TOOLS extends ToolSet>`
et `ToolResultUnion<TOOLS extends ToolSet>` peuvent être utilisés pour
extraire les types d'appel d'outil et de résultat d'outil des outils.

```ts highlight="18-19,23-24"
import { openai } from '@ai-sdk/openai';
import { ToolCallUnion, ToolResultUnion, generateText, tool } from 'ai';
import { z } from 'zod';

const monEnsembleDoutils = {
  premiereOutil: tool({
    description: 'Salut le utilisateur',
    parameters: z.object({ nom: z.string() }),
    execute: async ({ nom }) => `Bonjour, ${nom} !`,
  }),
  deuxiemeOutil: tool({
    description: 'Dit à l utilisateur leur age',
    parameters: z.object({ age: z.number() }),
    execute: async ({ age }) => `Vous avez ${age} ans !`,
  }),
};

type MonAppelDoutil = ToolCallUnion<typeof monEnsembleDoutils>;
type MonResultatDoutil = ToolResultUnion<typeof monEnsembleDoutils>;
```

```javascript
async function générerQuelqueChose(prompt: string): Promise<{
  texte: string;
  appelsDeOutil: Array<MyToolCall>; // appels d'outil typés
  résultatsDeOutil: Array<MyToolResult>; // résultats d'outil typés
}> {
  return générerTexte({
    modèle: openai('gpt-4o'),
    outils: monOutilSet,


## Gestion des Erreurs

L'API SDK dispose de trois erreurs liées aux appels de fonctions :

- [`NoSuchToolError`](/docs/reference/ai-sdk-errors/ai-no-such-tool-error) : le modèle tente d'appeler une fonction qui n'est pas définie dans l'objet de fonctions
- [`InvalidToolArgumentsError`](/docs/reference/ai-sdk-errors/ai-invalid-tool-arguments-error) : le modèle appelle une fonction avec des arguments qui ne correspondent pas aux paramètres de la fonction
- [`ToolExecutionError`](/docs/reference/ai-sdk-errors/ai-tool-execution-error) : une erreur qui est survenue pendant l'exécution de la fonction
- [`ToolCallRepairError`](/docs/reference/ai-sdk-errors/ai-tool-call-repair-error) : une erreur qui est survenue pendant la réparation d'un appel de fonction

### `generateText`

`generateText` lance des erreurs et peut être gérées à l'aide d'un bloc `try`/`catch` :

```ts
essai {
  const result = attendre generateText({
    //...
  });
} catch (erreur) {
  si (NoSuchToolError.isInstance(erreur)) {
    // gérer l'erreur de fonction non trouvée
  } else if (InvalidToolArgumentsError.isInstance(erreur)) {
    // gérer l'erreur d'arguments de fonction invalides
  } else if (ToolExecutionError.isInstance(erreur)) {
    // gérer l'erreur d'exécution de fonction
  } else {
    // gérer les autres erreurs
  }
}
```

### `streamText`

`streamText` envoie les erreurs comme partie intégrante de la flux complet. Les parties d'erreur contiennent l'objet d'erreur.

Lorsque vous utilisez `toDataStreamResponse`, vous pouvez passer une fonction `getErrorMessage` pour extraire le message d'erreur de la partie d'erreur et la transmettre comme partie intégrante de la réponse de flux de données :

```ts
const result = streamText({
  // ...
});

return result.toDataStreamResponse({
  getErrorMessage: error => {
    if (NoSuchToolError.isInstance(error)) {
      return 'Le modèle a essayé d\'appeler un outil inconnu.';
    } else if (InvalidToolArgumentsError.isInstance(error)) {
      return 'Le modèle a appelé un outil avec des arguments invalides.';
    } else if (ToolExecutionError.isInstance(error)) {
      return 'Une erreur est survenue lors de l\'exécution de l\'outil.';
    } else {
      return 'Une erreur inconnue est survenue.';
    }
  },
});
```

## Réparation d'appel d'outil

<Note type="warning">
  La fonction de réparation d'appel d'outil est expérimentale et peut changer à l'avenir.
</Note>

Les modèles de langage échouent parfois à générer des appels d'outil valides,
surtout lorsque les paramètres sont complexes ou que le modèle est plus petit.

Vous pouvez utiliser la fonction `experimental_repairToolCall` pour essayer de réparer l'appel d'outil
avec une fonction personnalisée.

Vous pouvez utiliser différentes stratégies pour réparer l'appel d'outil :

- Utilisez un modèle avec des sorties structurées pour générer les arguments.
- Envoyez les messages, la prompt système et le schéma de l'outil à un modèle plus fort pour générer les arguments.
- Fournissez des instructions de réparation plus spécifiques en fonction de l'outil appelé.

### Exemple : Utiliser un modèle avec des sorties structurées pour la réparation

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
      return null; // ne pas tenter de corriger les noms de outil non valides
    }

    const outil = tools[toolCall.toolName as keyof typeof tools];

    const { objet: argumentsReparés } = await generateObject({
      model: openai('gpt-4o', { sortiesStructurées: true }),
      schema: outil.parameters,
      prompt: [
        `Le modèle a tenté d'appeler l'outil "${toolCall.toolName}"` +
          ` avec les arguments suivants :`,
        JSON.stringify(toolCall.args),
        `L'outil accepte le schéma suivant :`,
        JSON.stringify(parameterSchema(toolCall)),
        'Veuillez corriger les arguments.',
      ].join('\n'),
    });

    return { ...toolCall, args: JSON.stringify(argumentsReparés) };
  },
});
```

### Exemple : Utiliser la stratégie de re-ask pour le réparateur

```ts
import { openai } from '@ai-sdk/openai';
import { generateObject, generateText, NoSuchToolError, tool } from 'ai';

const result = await generateText({
  model,
  tools,
  prompt,
  strategy: 're-ask', // Stratégie de re-ask pour le réparateur
});
```

### Util

`experimental_repairToolCall`: async ({
  toolCall,
  outils,
  erreur,
  messages,
  système,
}) => {
  const résultat = await generateText({
    modèle,
    système,
    messages: [
      ...messages,
      {
        rôle: 'assistant',
        contenu: [
          {
            type: 'appel-outil',
            toolCallId: toolCall.toolCallId,
            nomOutil: toolCall.toolName,
            args: toolCall.args,
          },
        ],
      },
      {
        rôle: 'outil' as const,
        contenu: [
          {
            type: 'résultat-outil',
            toolCallId: toolCall.toolCallId,
            nomOutil: toolCall.toolName,
            résultat: erreur.message,
          },
        ],
      },
    ],
    outils,
  });

  const nouvelAppelOutil = résultat.appelsOutils.find(
    nouvelAppelOutil => nouvelAppelOutil.nom

retourne newToolCall != null
      ? {
          typeDeLancementDeLoutil : 'function' as const,
          idDeLancementDeLoutil : toolCall.toolCallId,
          nomDeLoutil : toolCall.toolName,
          args : JSON.stringify(newToolCall.args),


## Outils Actifs

<Note type="warning">
  La propriété `activeTools` est expérimentale et peut changer à l'avenir.
</Note>

Les modèles de langage ne peuvent gérer qu'un nombre limité d'outils en même temps, en fonction du modèle.
Pour permettre la typage statique en utilisant un grand nombre d'outils et en limitant les outils disponibles au modèle en même temps,
le SDK AI fournit la propriété `experimental_activeTools`.

Il s'agit d'un tableau de noms d'outils qui sont actuellement actifs.
Par défaut, la valeur est `undefined` et tous les outils sont actifs.

```ts highlight="7"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: openai('gpt-4o'),
  tools: monEnsembleDoutils,
  experimental_activeTools: ['premierOutil'],
});
```

## Résultats de l'outil multi-modal

<Note type="warning">
  Les résultats des outils multi-modal sont expérimentaux et ne sont pris en charge que par Anthropic.
</Note>

Pour envoyer les résultats des outils multi-modal, par exemple des captures d'écran, de retour au modèle, ils doivent être convertis dans un format spécifique.

Les outils Core SDK d'IA ont une fonction facultative `experimental_toToolResultContent` qui convertit le résultat de l'outil en une partie de contenu.

Voici un exemple de conversion d'une capture d'écran en partie de contenu :

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

// carte pour le contenu de résultat de l'outil pour la consommation LLM :
      experimental_toToolResultContent(result) {
        return typeof result === 'string'
          ? [{ type: 'text', text: result }]
          : [{ type: 'image', data: result.data, mimeType: 'image/png' }];
      },
    }),
  },
  // ...
});

## Extraction des Outils

Une fois que vous avez de nombreux outils, vous pourriez vouloir les extraire dans des fichiers séparés.
La fonction d'aide `tool` est cruciale pour cela, car elle garantit une inférence de type correcte.

Voici un exemple d'outil extrait :

```ts filename="outils/outil-météo.ts" highlight="1,4-5"
import { tool } from 'ai';
import { z } from 'zod';

// la fonction d'aide `tool` garantit une inférence de type correcte :
export const outilMétéo = tool({
  description: 'Obtenir le temps dans une localité',
  parameters: z.object({
    location: z.string().describe('La localité pour obtenir le temps'),
  }),
  execute: async ({ location }) => ({
    location,
    temperature: 72 + Math.floor(Math.random() * 21) - 10,
  }),
});
```

## Outils MCP

<Note type="warning">
  Les outils MCP sont expérimentaux et peuvent changer à l'avenir.
</Note>

La bibliothèque SDK AI prend en charge la connexion à des serveurs [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) pour accéder à leurs outils.
Cela permet à vos applications AI de découvrir et d'utiliser des outils à travers divers services via une interface standardisée.

### Initialisation d'un Client MCP

Créez un client MCP en utilisant :

- `SSE` (Server-Sent Events) : Utilise la communication en temps réel basée sur HTTP, plus adaptée pour les serveurs distants qui doivent envoyer des données sur le réseau
- `stdio` : Utilise les flux de sortie standard pour la communication, idéal pour les serveurs d'outils locaux exécutés sur la même machine (comme les outils CLI ou les services locaux)
- Transport personnalisé : Apportez votre propre transport en mettant en œuvre l'interface `MCPTransport`, idéal lorsque vous implémentez des transports à partir de la bibliothèque officielle Typescript de MCP (par exemple `StreamableHTTPClientTransport`)

#### Transport SSE

Le transport SSE peut être configuré à l'aide d'un objet simple avec les propriétés `type` et `url` :

```typescript
import { experimental_createMCPClient as createMCPClient } from 'ai';

const mcpClient = await createMCPClient({
  transport: {
    type: 'sse',
    url: 'https://mon-serviteur.com/sse',

    // optionnel : configurez les en-têtes HTTP, par exemple pour l'authentification
    headers: {
      Authorization: 'Bearer mon-api-clé',
    },
  },
});
```

#### Transport Stdio

Le transport Stdio nécessite l'importation de la classe `StdioMCPTransport` du package `ai/mcp-stdio` :

```typescript
import { experimental_createMCPClient as createMCPClient } from 'ai';
import { Experimental_StdioMCPTransport as StdioMCPTransport } from 'ai/mcp-stdio';

const mcpClient = await createMCPClient({
  transport: new StdioMCPTransport({
    commande: 'node',
    arguments: ['src/stdio/dist/server.js'],
  }),
});
```

#### Transport personnalisé

Vous pouvez également apporter votre propre transport, à condition qu'il implémente l'interface `MCPTransport`. Voici un exemple d'utilisation du nouveau `StreamableHTTPClientTransport` de la bibliothèque officielle Typescript de MCP :

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

<Note>
  Le client retourné par la fonction `experimental_createMCPClient` est un client
  léger destiné à l'utilisation dans la conversion d'outil. Il ne prend actuellement
  pas en charge toutes les fonctionnalités du client MCP complet, telles que : 
  l'authentification, la gestion de session, les flux résumables, et la réception de notifications.
</Note>

#### Fermer le Client MCP

Après l'initialisation, vous devriez fermer le client MCP en fonction de votre modèle d'utilisation :

- Pour les utilisations de courte durée (par exemple, des requêtes uniques), fermez le client lorsque la réponse est terminée
- Pour les clients longs (par exemple, des applications de ligne de commande), gardez le client ouvert mais assurez-vous qu'il soit fermé lorsque l'application se termine

Lors de la streaming de réponses, vous pouvez fermer le client lorsque la réponse LLM est terminée. Par exemple, lors de l'utilisation de `streamText`, vous devriez utiliser le callback `onFinish` :

```typescript
const mcpClient = await experimental_createMCPClient({
  // ...
});

const tools = await mcpClient.tools();

const result = await streamText({
  model: openai('gpt-4o'),
  tools,
  prompt: 'Quel est le temps à Brooklyn, New York?',
  onFinish: async () => {
    await mcpClient.close();
  },
});
```

Lors de la génération de réponses sans streaming, vous pouvez utiliser try/finally ou des fonctions de nettoyage dans votre framework :

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

### Utilisation des Outils MCP

La méthode `tools` du client agit comme un adaptateur entre les outils MCP et les outils SDK IA. Elle prend en charge deux approches pour travailler avec les schémas d'outil :

#### Découverte de Schemas

L'approche la plus simple où tous les outils proposés par le serveur sont listés, et les types de paramètres d'entrée sont inférés sur la base des schémas fournis par le serveur :

```typescript
const tools = await mcpClient.tools();
```

**Avantages :**

- Plus simple à mettre en œuvre
- Reste automatiquement à jour avec les changements du serveur

**Inconvénients :**

- Pas de sécurité de type TypeScript pendant le développement
- Pas d'autocomplétion IDE pour les paramètres d'outil
- Les erreurs ne se manifestent qu'en temps de exécution
- Charge tous les outils du serveur

#### Définition du Schéma

Vous pouvez également définir explicitement les outils et leurs schémas d'entrée dans votre code client :

```typescript
import { z } from 'zod';

const outils = await mcpClient.outils({
  schemas: {
    'get-data': {
      paramètres: z.object({
        query: z.string().describe('La requête de données'),
        format: z.enum(['json', 'text']).facultatif(),
      }),
    },
    // Pour les outils sans argument, vous devez utiliser un objet vide :
    'outil-avec-aucun-argument' : {
      paramètres: z.object({}),
    },
  },
});
```

**Avantages:**

- Contrôle sur les outils chargés
- Sécurité de type complète avec TypeScript
- Meilleure prise en charge de l'IDE avec l'autocomplétion
- Capturer les incohérences de paramètres pendant le développement

**Inconvénients:**

- Besoin de maintenir manuellement les schémas en accord avec le serveur
- Plus de code à maintenir

Lorsque vous définissez `schemas`, le client ne chargera que les outils explicitement définis, même si le serveur propose des outils supplémentaires. Cela peut être bénéfique pour :

- Garder votre application centrée sur les outils dont elle a besoin
- Réduire les chargements d'outils inutiles
- Faire les dépendances des outils explicites

## Exemples

Vous pouvez voir les outils en action à l'aide de divers frameworks dans les exemples suivants :

<ExampleLinks
  examples={[
    {
      title: 'Apprendre à utiliser les outils dans Node.js',
      link: '/cookbook/node/call-tools',
    },
    {
      title: 'Apprendre à utiliser les outils dans Next.js avec les gestionnaires de route',
      link: '/cookbook/next/call-tools',
    },
    {
      title: 'Apprendre à utiliser les outils MCP dans Node.js',
      link: '/cookbook/node/mcp-tools',
    },
  ]}
/>

---
titre : Ingénierie de requêtes
description : Apprenez à développer des requêtes avec le SDK Core AI.
---

# Ingénierie de requêtes

## Conseils

### Prompts pour les Outils

Lorsque vous créez des prompts qui incluent des outils, obtenir de bons résultats peut être difficile à mesure que le nombre et la complexité de vos outils augmentent.

Voici quelques conseils pour vous aider à obtenir les meilleurs résultats :

1. Utilisez un modèle qui est fort en matière d'appel d'outils, tel que `gpt-4` ou `gpt-4-turbo`. Les modèles moins puissants auront souvent du mal à appeler les outils de manière efficace et sans erreur.
1. Gardez le nombre d'outils bas, par exemple à 5 ou moins.
1. Gardez la complexité des paramètres des outils basse. Les schémas Zod complexes avec de nombreux éléments imbriqués et optionnels, des unions, etc. peuvent être difficiles à travailler pour le modèle.
1. Utilisez des noms significatifs sémantiquement pour vos outils, vos paramètres, les propriétés des paramètres, etc. Plus d'informations que vous passez au modèle, mieux il peut comprendre ce que vous voulez.
1. Ajoutez `.describe("...")` à vos propriétés de schéma Zod pour donner au modèle des indices sur ce que sert une propriété particulière.
1. Lorsque l'output d'un outil peut être incertain pour le modèle et qu'il existe des dépendances entre outils, utilisez le champ `description` d'un outil pour fournir des informations sur l'output de l'exécution de l'outil.
1. Vous pouvez inclure des exemples d'entrées/sorties de l'appel d'outils dans votre prompt pour aider le modèle à comprendre comment utiliser les outils. Gardez à l'esprit que les outils travaillent avec des objets JSON, donc les exemples doivent utiliser JSON.

En général, l'objectif devrait être de donner au modèle toutes les informations dont il a besoin de manière claire.

### Outils & Schémas de Données Structurés

La correspondance entre les schémas Zod et les entrées des LLM (généralement schéma JSON) n'est pas toujours directe, puisque la correspondance n'est pas un à un.

#### Dates de Zod

Zod attend des objets Date JavaScript, mais les modèles retournent des dates sous forme de chaînes.
Vous pouvez spécifier et valider la forme de date en utilisant `z.string().datetime()` ou `z.string().date()`,
et puis utiliser une transformateur Zod pour convertir la chaîne en objet Date.

```ts highlight="7-10"
const result = await generateObject({
  model: openai('gpt-4-turbo'),
  schema: z.object({
    events: z.array(
      z.object({
        event: z.string(),
        date: z
          .string()
          .date()
          .transform(value => new Date(value)),
      }),
    ),
  }),
  prompt: 'Liste 5 événements importants de l\'année 2000.',
});
```

## Débogage

### Inspection des Avertissements

Tous les fournisseurs ne supportent pas toutes les fonctionnalités de l'API SDK.
Les fournisseurs lancent soit des exceptions, soit des avertissements lorsqu'ils ne supportent pas une fonctionnalité.
Pour vérifier si votre prompt, vos outils et vos paramètres sont traités correctement par le fournisseur, vous pouvez inspecter les avertissements :

```ts
const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Bonjour, monde !',
});

console.log(result.warnings);
```

### Corps de requête HTTP

Vous pouvez inspecter les corps de requête HTTP bruts pour les modèles qui les exposent, par exemple [OpenAI](/providers/ai-sdk-providers/openai).
Cela vous permet d'inspecter le payload exact qui est envoyé au fournisseur de modèle de manière spécifique au fournisseur.

Les corps de requête sont disponibles via la propriété `request.body` de la réponse :

```ts highlight="6"
const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Hello, world!',
});

console.log(result.request.body);
```

---
titre : Paramètres
description : Apprenez à configurer le SDK AI.
---

# Paramètres

Les grands modèles de langage (GML) fournissent généralement des paramètres pour augmenter leur sortie.

Toutes les fonctions du SDK AI supportent les paramètres de configuration suivants en plus du modèle, de la [suggestion](./prompts) et des paramètres spécifiques au fournisseur :

```ts highlight="3-5"
const result = await generateText({
  model: votreModel,
  maxTokens: 512,
  temperature: 0,3,
  maxRetries: 5,
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
});
```

<Note>
  Certains fournisseurs ne supportent pas tous les paramètres de configuration communs. Si vous utilisez un paramètre avec un fournisseur qui ne le supporte pas, un avertissement sera généré. Vous pouvez vérifier la propriété `warnings` de l'objet de résultat pour voir si des avertissements ont été générés.
</Note>

### `maxTokens`

Nombre maximum de jetons à générer.

### `temperature`

Réglage de la température.

La valeur est transmise au fournisseur. La plage dépend du fournisseur et du modèle.
Pour la plupart des fournisseurs, `0` signifie des résultats presque déterministes, et des valeurs plus élevées signifient plus d'aléatoire.

Il est recommandé de définir soit `temperature`, soit `topP`, mais pas les deux.

### `topP`

Échantillonnage de Nucleus.

La valeur est transmise au fournisseur. La plage dépend du fournisseur et du modèle.
Pour la plupart des fournisseurs, l'échantillonnage de Nucleus est un nombre compris entre 0 et 1.
Par exemple, 0,1 signifie que seuls les tokens avec les 10% de probabilité la plus élevée sont considérés.

Il est recommandé de définir soit `temperature` soit `topP`, mais pas les deux.

### `topK`

N'échantillonner que les options les plus élevées K pour chaque token suivant.

Utilisé pour supprimer les "longues queues" de réponses de faible probabilité.
Recommandé pour les cas d'utilisation avancés uniquement. Vous n'avez généralement besoin de utiliser que `temperature`.

### `presencePenalty`

La pénalité de présence affecte la probabilité du modèle à répéter des informations qui sont déjà dans le prompt.

La valeur est transmise au fournisseur. La plage dépend du fournisseur et du modèle.
Pour la plupart des fournisseurs, `0` signifie pas de pénalité.

### `frequencyPenalty`

La pénalité de fréquence affecte la probabilité du modèle à répéter les mêmes mots ou phrases.

La valeur est transmise au fournisseur. La plage dépend du fournisseur et du modèle.
Pour la plupart des fournisseurs, `0` signifie pas de pénalité.

### `stopSequences`

Les séquences d'arrêt à utiliser pour arrêter la génération de texte.

Si défini, le modèle arrêtera la génération de texte lorsqu'une des séquences d'arrêt est générée.
Les fournisseurs peuvent avoir des limites sur le nombre de séquences d'arrêt.

### `seed`

Il s'agit de la graine (entier) à utiliser pour l'échantillonnage aléatoire.
Si défini et pris en charge par le modèle, les appels généreront des résultats déterministes.

### `maxRetries`

Nombre maximum de tentatives. Définir sur 0 pour désactiver les tentatives. Défaut : `2`.

### `abortSignal`

Un signal d'arrêt optionnel qui peut être utilisé pour annuler l'appel.

Le signal d'arrêt peut par exemple être transmis depuis une interface utilisateur pour annuler l'appel,
ou pour définir un temps d'attente.

#### Exemple : Temps d'attente

```ts
const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  abortSignal: AbortSignal.timeout(5000), // 5 secondes
});
```

### En-têtes

En-têtes HTTP supplémentaires à envoyer avec la requête. Seulement applicable pour les fournisseurs basés sur HTTP.

Vous pouvez utiliser les en-têtes de requête pour fournir des informations supplémentaires au fournisseur,
selon ce que le fournisseur supporte. Par exemple, certains fournisseurs de visibilité supportent
des en-têtes comme `Prompt-Id`.

```ts
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Invente un nouveau jour férié et décrit ses traditions.',
  headers: {
    'Prompt-Id': 'mon-id-de-prompt',
  },
});
```

<Remarque>
  La configuration `headers` est pour les en-têtes spécifiques à la requête. Vous pouvez également définir
  `headers` dans la configuration du fournisseur. Ces en-têtes seront envoyés avec chaque requête effectuée par le fournisseur.
</Remarque>

---
titre : Embeddings
description : Apprenez comment intégrer des valeurs avec le SDK AI.
---

# Embeddings

Les embeddings sont une façon de représenter des mots, des phrases ou des images sous forme de vecteurs dans un espace à haute dimensionnalité.
Dans cet espace, les mots similaires sont proches les uns des autres, et la distance entre les mots peut être utilisée pour mesurer leur similarité.

## Intégration d'une valeur unique

Le SDK AI fournit la fonction `embed` pour intégrer des valeurs uniques, qui est utile pour les tâches telles que la recherche de mots ou de phrases similaires ou la mise en cluster du texte.
Vous pouvez l'utiliser avec des modèles d'embeddings, par exemple `openai.embedding('text-embedding-3-large')` ou `mistral.embedding('mistral-embed')`.

```tsx
import { embed } from 'ai';
import { openai } from '@ai-sdk/openai';

// 'embedding' est un objet d'embeddings unique (tableau de nombres)
const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'jour ensoleillé à la plage',
});
```

## Embedding de Plusieurs Valeurs

Lors de la charge de données, par exemple lors de la préparation d'un magasin de données pour la génération renforcée par la recherche (RAG),
il est souvent utile d'embed de nombreuses valeurs à la fois (embeddage en batch).

Le SDK AI fournit la fonction [`embedMany`](/docs/reference/ai-sdk-core/embed-many) à cette fin.
De manière similaire à `embed`, vous pouvez l'utiliser avec des modèles d'embeddage,
par exemple `openai.embedding('text-embedding-3-large')` ou `mistral.embedding('mistral-embed')`.

```tsx
import { openai } from '@ai-sdk/openai';
import { embedMany } from 'ai';

// 'embeddings' est un tableau d'objets d'embeddage (number[][]).
// Il est classé dans le même ordre que les valeurs d'entrée.
const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: [
    'jour ensoleillé à la plage',
    'après-midi pluvieux dans la ville',
    'nuit enneigée dans les montagnes',
  ],
});
```

## Similarité de l'Embeddage

Après avoir embeddé des valeurs, vous pouvez calculer la similarité entre elles à l'aide de la fonction [`cosineSimilarity`](/docs/reference/ai-sdk-core/cosine-similarity).
Cela est utile pour trouver des mots ou des phrases similaires dans un jeu de données.
Vous pouvez également classer et filtrer des éléments liés en fonction de leur similarité.

```ts highlight={"2,10"}
import { openai } from '@ai-sdk/openai';
import { cosineSimilarity, embedMany } from 'ai';

const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['jour ensoleillé à la plage', 'après-midi pluvieux dans la ville'],
});

console.log(
  `similarité cosinus : ${cosineSimilarity(embeddings[0], embeddings[1])}`,
);
```

## Utilisation des jetons

Beaucoup de fournisseurs facturent en fonction du nombre de jetons utilisés pour générer des embeddings.
Les deux `embed` et `embedMany` fournissent des informations sur l'utilisation des jetons dans la propriété `usage` de l'objet de résultat :

```ts highlight={"4,9"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding, usage } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'jour ensoleillé à la plage',
});

console.log(usage); // { tokens: 10 }
```

## Paramètres

### Redemandes

Les deux `embed` et `embedMany` acceptent un paramètre optionnel `maxRetries` de type `number`
que vous pouvez utiliser pour définir le nombre maximum de redemandes pour le processus d'embedding.
Il est défini par défaut sur `2` redemandes (3 tentatives au total). Vous pouvez le définir sur `0` pour désactiver les redemandes.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'jour ensoleillé à la plage',
  maxRetries: 0, // Désactiver les redemandes
});
```

### Signaux d'annulation et temps d'attente

Les deux `embed` et `embedMany` acceptent un paramètre optionnel `abortSignal` de
type [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
que vous pouvez utiliser pour annuler le processus d'embedding ou définir un temps d'attente.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'jour ensoleillé à la plage',
  abortSignal: AbortSignal.timeout(1000), // Annuler après 1 seconde
});
```

### En-têtes personnalisés

Les deux `embed` et `embedMany` acceptent un paramètre `headers` optionnel de type `Record<string, string>`
que vous pouvez utiliser pour ajouter des en-têtes personnalisés à la demande d'embedage.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { embed } from 'ai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'jour ensoleillé à la plage',
  headers: { 'X-Custom-Header': 'custom-value' },
});
```

## Fournisseurs & Modèles d'Embedding

Plusieurs fournisseurs proposent des modèles d'embedding :

| Fournisseur                                                                                   | Modèle                           | Dimensions d'embedding |
| ------------------------------------------------------------------------------------------ | ------------------------------- | -------------------- |
| [OpenAI](/providers/ai-sdk-providers/openai#modèles-d-embedding)                              | `text-embedding-3-large`        | 3072                 |
| [OpenAI](/providers/ai-sdk-providers/openai#modèles-d-embedding)                              | `text-embedding-3-small`        | 1536                 |
| [OpenAI](/providers/ai-sdk-providers/openai#modèles-d-embedding)

# Modèles d'embedding
| | `text-embedding-ada-002`        | 1536                 |
| [Google Generative AI](/providers/ai-sdk-providers/google-generative-ai#modèles-d'embedding) | `text-embedding-004`            | 768                  |
| [Mistral](/providers/ai-sdk-providers/mistral#modèles-d'embedding)                           | `mistral-embed`                 | 1024                 |
| [Cohere](/providers/ai-sdk

# Modèles d'embeddings
| [Cohere](/providers/ai-sdk-providers/cohere#modèles-d'embeddings)                             | `embed-anglais-light-v3.0`      | 384                  |
| [Cohere](/providers/ai-sdk-providers/cohere#modèles-d'embeddings)                             | `embed-multilingue-light-v3.0` | 384                  |
| [Cohere](/providers/ai-sdk-providers/cohere#modèles-d'

# Modèles d'embeddings)             | `amazon.titan-embed-text-v1`    | 1024                 |
| [Amazon Bedrock](/providers/ai-sdk-providers/amazon-bedrock#modèles-d'embeddings)             | `amazon.titan-embed-text-v2:0`  | 1024                 |

---
Titre : Génération d'images
Description : Apprenez à générer des images avec l'API SDK.
---

# Génération d'images

<Note type="warning">La génération d'images est une fonctionnalité expérimentale.</Note>

L'API SDK fournit la fonction `generateImage` pour générer des images en fonction d'un prompt donné à l'aide d'un modèle d'image.

```tsx
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduisant un Cadillac',
});
```

Vous pouvez accéder aux données d'image à l'aide des propriétés `base64` ou `uint8Array` :

```tsx
const base64 = image.base64; // données d'image au format base64
const uint8Array = image.uint8Array; // Uint8Array données d'image
```

## Paramètres

### Taille et Rapport d'Aspect

En fonction du modèle, vous pouvez soit spécifier la taille, soit le rapport d'aspect.

##### Taille

La taille est spécifiée sous la forme d'une chaîne dans le format `{largeur}x{hauteur}`.
Les modèles ne supportent qu'une poignée de tailles, et les tailles supportées diffèrent pour chaque modèle et fournisseur.

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Le Père Noël conduisant un Cadillac',
  size: '1024x1024',
});
```

##### Rapport d'aspect

Le rapport d'aspect est spécifié sous la forme d'une chaîne dans le format `{largeur}:{hauteur}`.
Les modèles ne supportent qu'une poignée de rapports d'aspect, et les rapports d'aspect supportés diffèrent pour chaque modèle et fournisseur.

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { vertex } from '@ai-sdk/google-vertex';

const { image } = await generateImage({
  model: vertex.image('imagen-3.0-generate-002'),
  prompt: 'Le Père Noël conduisant un Cadillac',
  aspectRatio: '16:9',
});

### Génération de plusieurs images

`generateImage` prend également en charge la génération de plusieurs images à la fois :

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { images } = await generateImage({
  model: openai.image('dall-e-2'),
  prompt: 'Santa Claus conduisant une Cadillac',
  n: 4, // Nombre d'images à générer
});
```

<Note>
  `generateImage` appelle automatiquement le modèle autant de fois que nécessaire (en parallèle) pour générer le nombre de images demandé.
</Note>

Chaque modèle d'image a une limite interne sur le nombre d'images qu'il peut générer dans une seule appel API. Le SDK AI gère cela automatiquement en regroupant les requêtes en fonction du paramètre `n` lors de la génération de plusieurs images. Par défaut, le SDK utilise les limites documentées par les fournisseurs (par exemple, DALL-E 3 ne peut générer qu'une image par appel, tandis que DALL-E 2 supporte jusqu'à 10).

Si nécessaire, vous pouvez contourner ce comportement en utilisant la configuration `maxImagesPerCall` lors de la configuration de votre modèle. Cela est particulièrement utile lors du travail avec de nouveaux ou de modèles personnalisés où la taille de la batch par défaut pourrait ne pas être optimale :

```tsx
const model = openai.image('dall-e-2', {
  maxImagesPerCall: 5, // Surpasser la taille de batch par défaut
});

const { images } = await generateImage({
  model,
  prompt: 'Santa Claus conduisant une Cadillac',
  n: 10, // Fera 2 appels de 5 images chacun
});
```

### Fournir un Seed

Vous pouvez fournir un seed à la fonction `generateImage` pour contrôler la sortie du processus de génération d'image.
Si le modèle le supporte, le même seed produira toujours la même image.

```tsx highlight={"7"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduisant une Cadillac',
  seed: 1234567890,
});
```

### Paramètres spécifiques au fournisseur

Les modèles d'image ont souvent des paramètres spécifiques au fournisseur ou même au modèle.
Vous pouvez passer de tels paramètres à la fonction `generateImage` 
en utilisant le paramètre `providerOptions`. Les options du fournisseur 
(`openai` dans l'exemple ci-dessous) deviennent des propriétés du corps de la requête.

```tsx highlight={"9"}
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduisant une Cadillac',
  size: '1024x1024',
  providerOptions: {
    openai: { style: 'vivid', quality: 'hd' },
  },
});
```

### Signaux d'abandon et les temps limites

`generateImage` accepte un paramètre facultatif `abortSignal` de type
[`AbortSignal`](https://developer.mozilla.org/fr/docs/Web/API/AbortSignal)
que vous pouvez utiliser pour abandonner le processus de génération d'image ou définir un temps limite.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduisant une Cadillac',
  abortSignal: AbortSignal.timeout(1000), // Abandonner après 1 seconde
});
```

### En-têtes personnalisés

`generateImage` accepte un paramètre facultatif `headers` de type `Record<string, string>`
que vous pouvez utiliser pour ajouter des en-têtes personnalisés à la requête de génération d'image.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  value: 'jour ensoleillé à la plage',
  headers: { 'X-En-tête-personnalisée': 'valeur-personnalisée' },
});
```

### Avertissements

Si le modèle retourne des avertissements, par exemple pour des paramètres non supportés, ils seront disponibles dans la propriété `warnings` de la réponse.

```tsx
const { image, warnings } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus conduisant une Cadillac',
});
```

### Gestion des Erreurs

Lorsque `generateImage` ne parvient pas à générer une image valide, elle lance une exception [`AI_NoImageGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-image-generated-error).

Cette erreur se produit lorsque le fournisseur d'IA échoue à générer une image. Elle peut survenir en raison des raisons suivantes :

- Le modèle a échoué à générer une réponse
- Le modèle a généré une réponse qui ne pouvait pas être analysée

L'erreur conserve les informations suivantes pour vous aider à logger l'erreur :

- `responses`: Métadonnées sur les réponses du modèle d'image, y compris la date, le modèle et les en-têtes.
- `cause`: La cause de l'erreur. Vous pouvez utiliser cela pour une gestion d'erreur plus détaillée

```ts
import { generateImage, NoImageGeneratedError } from 'ai';

try {
  await generateImage({ model, prompt });
} catch (error) {
  if (NoImageGeneratedError.isInstance(error)) {
    console.log('NoImageGeneratedError');
    console.log('Cause:', error.cause);
    console.log('Responses:', error.responses);
  }
}
```

## Génération d'Images avec les Modèles de Langage

Certains modèles de langage, comme Google `gemini-2.0-flash-exp`, supportent des sorties multi-modales, y compris les images.
Avec de tels modèles, vous pouvez accéder aux images générées à l'aide de la propriété `files` de la réponse.

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const result = await generateText({
  model: google('gemini-2.0-flash-exp'),
  providerOptions: {
    google: { responseModalities: ['TEXT', 'IMAGE'] },
  },
  prompt: 'Générez une image d\'un chat comique',
});

for (const file of result.files) {
  if (file.mimeType.startsWith('image/')) {
    // L'objet de fichier fournit plusieurs formats de données :
    // Accédez aux images sous forme de chaîne de base64, de données binaires Uint8Array ou vérifiez le type
    // - file.base64: chaîne (format de données URL)
    // - file.uint8Array: Uint8Array (données binaires)
    // - file.mimeType: chaîne (par exemple "image/png")
  }
}
```

## Modèles d'Images

| Fournisseur                                                                 | Modèle                                                        | Support des tailles (`largeur x hauteur`) ou ratios d'aspect (`largeur : hauteur`)                                                                                       |
| ------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [xAI Grok](/providers/ai-sdk-providers/xai-grok)                        | -                                                            | -                                                                                                                                                    |
| [Deepgram](/providers/ai-sdk

#modèles d'image)                  | `grok-2-image`                                               | 1024x768 (par défaut)                                                                                                                                                  |
| [OpenAI](/fournisseurs/sdk-ai-providers/openai#modèles d'image)                

# Modèles d'image)                 | `dall-e-3`                                                   | 1024x1024, 1792x1024, 1024x1792                                                                                                                                        |
| [OpenAI](/providers/ai-sdk-providers/openai#modèles-d-image)

# image-models) | `amazon.nova-canvas-v1:0`                                    | 320-4096 (multiples de 16), 1:4 à 4:1, max 4,2M de pixels                                                                                                             |
| [Fal](/providers/ai-sdk-providers/fal#image-models)                       | `fal-ai/flux/dev`                                            | 1:1, 3:

# Modèles d'image)                       | `fal-ai/flux-lora`                                           | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Fal](/providers/ai-sdk-providers/fal#modèles-d-image)                       | `fal-ai

# image-models)                       | `fal-ai/flux-pro/v1.1-ultra`                                 | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Fal](/providers/ai-sdk-providers/fal#image-models)                       | `

# Modèles d'image)                       | `fal-ai/recraft-v3`                                          | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Fal](/providers/ai-sdk-providers/fal#modèles-d'image)                       | `fal-ai

# Modèles d'image
                       | `fal-ai/hyper-sdxl`                                          | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [DeepInfra](/providers/ai-sdk-providers/deepinfra#modèles-d'image)           | `stabilityai/sd

#modèles d'image)           | `black-forest-labs/FLUX-1.1-pro`                             | 256-1440 (multiples de 32)                                                                                                                                          |
| [DeepInfra](/providers/ai-sdk-providers/deepinfra#modèles d'image)          

# Modèles d'image
           | `black-forest-labs/FLUX-1-dev`                               | 256-1440 (multiples de 32)                                                                                                                                          |
| [DeepInfra](/providers/ai-sdk-providers/deepinfra#modèles-d-image)           | `

# image-models)           | `stabilityai/sd3.5-medium`                                   | 1:1, 16:9, 1:9, 3:2, 2:3, 4:

# Modèles d'image)           | `stabilityai/sdxl-turbo`                                     | 1:1, 16:9, 1:9, 3:2, 2:3, 4:5, 5:4, 9:16, 9:21                                                                                                                      |
| [Répliquer](/fournisseurs/sdk-ai/replicate)                       

| [Replicate](/providers/ai-sdk-providers/replicate)                        | `recraft-ai/recraft-v3`                                      | 1024x1024, 1365x1024, 1024x1365, 1536x1024, 1024x1536, 1820x1024,

# Modèles d'image
| `imagen-3.0-generate-002`                                    | 1:1, 3:4, 4:3, 9:16, 16:9                                                                                                                                           |
| [Google Vertex](/providers/ai-sdk-providers/google-vertex#modèles-d-image)   | `imagen

# Modèles d'image
| [Feux d'artifice](/providers/ai-sdk-providers/fireworks#modèles-d'image)           | `accounts/fireworks/models/flux-1-dev-fp8`                   | 1:1, 2:3, 3:2, 4:5, 5:4, 16:9, 9:16, 9:21, 21:9                                                                

# Modèles d'image
| [Feux d'artifice](/providers/ai-sdk-providers/fireworks#modèles-d'image)           | `accounts/fireworks/models/playground-v2-5-1024px-aesthetic` | 640x1536, 768x1344, 832x1216, 896x1152, 1024x1024, 1152x896, 1216x832

# image-models
| [Feux d'artifice](/providers/ai-sdk-providers/feux-d-artifice#image-models)           | `accounts/feux-d-artifice/models/playground-v2-1024px-aesthetic`   | 640x1536, 768x1344, 832x1216, 896x1152, 1024x1024, 1152x896,

# Modèles d'image
| Nom du modèle | URI | Tailles prises en charge |
| --- | --- | --- |
| Stable Diffusion XL 1024 v1.0 | `accounts/fireworks/models/stable-diffusion-xl-1024-v1-0` | 640x1536, 768x1344, 832x1216, 896x1152, 1024

# modèles d'image)                     | `photon-flash-1`                                             | 1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9                                                                                                                               |
| [Together.ai](/providers/ai-sdk-providers/togetherai

# Modèles d'image
        | `black-forest-labs/FLUX.1-dev`                               | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/togetherai

# Modèles d'image)
        | `black-forest-labs/FLUX.1-schnell`                           | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/to

# Modèles d'images)
        | `black-forest-labs/FLUX.1-depth`                             | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/together

# Modèles d'image
| `black-forest-labs/FLUX.1.1-pro`                             | 512x512, 768x768, 1024x1024                                                                                                                                         |
| [Together.ai](/providers/ai-sdk-providers/together

# image-models)
        | `black-forest-labs/FLUX.1-schnell-Free`                      | 512x512, 768x768, 1024x1024                                                                                                                                         |

Voici un petit sous-ensemble des modèles d'image pris en charge par les fournisseurs de la SDK AI. Pour plus d'informations, consultez la documentation respective des fournisseurs.

---
title: Transcription
description: Apprenez à transcrire des enregistrements audio avec la SDK AI.
---

# Transcription

<Note type="warning">La transcription est une fonctionnalité expérimentale.</Note>

La bibliothèque SDK fournit la fonction [`transcribe`](/docs/reference/ai-sdk-core/transcribe)
pour transcrire des enregistrements audio à l'aide d'un modèle de transcription.

```ts
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
});
```

La propriété `audio` peut être un `Uint8Array`, `ArrayBuffer`, `Buffer`, `string` (données audio encodées en base64) ou une `URL`.

Pour accéder au transcript généré :

```ts
const texte = transcript.text; // texte du transcript e.g. "Bonjour, monde !"
const segments = transcript.segments; // tableau de segments avec les heures de début et de fin, si disponible
const langue = transcript.language; // langue du transcript e.g. "fr", si disponible
const duréeEnSecondes = transcript.durationInSeconds; // durée du transcript en secondes, si disponible
```

## Paramètres

### Paramètres spécifiques au fournisseur

Les modèles de transcription ont souvent des paramètres spécifiques au fournisseur ou au modèle que vous pouvez définir en utilisant le paramètre `providerOptions`.

```ts highlight="8-12"
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
  providerOptions: {
    openai: {
      timestampGranularités: ['mot'],
    },
  },
});
```

### Signaux d'abord et les temps limite

`transcribe` accepte un paramètre facultatif `abortSignal` de type
[`AbortSignal`](https://developer.mozilla.org/fr/docs/Web/API/AbortSignal)
que vous pouvez utiliser pour interrompre le processus de transcription ou définir un temps limite.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_transcribe as transcribe } from 'ai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
  abortSignal: AbortSignal.timeout(1000), // Interrompre après 1 seconde
});
```

### En-têtes personnalisés

`transcribe` accepte un paramètre facultatif `headers` de type `Record<string, string>`
que vous pouvez utiliser pour ajouter des en-têtes personnalisés à la demande de transcription.

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

### Avertissements

Les avertissements (par exemple, les paramètres non pris en charge) sont disponibles sur la propriété `warnings`.

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

### Gestion des Erreurs

Lorsque `transcribe` ne peut pas générer un transcript valide, elle lance une exception [`AI_NoTranscriptGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-transcript-generated-error).

Cette erreur peut survenir pour l'une des raisons suivantes :

- Le modèle n'a pas pu générer une réponse
- Le modèle a généré une réponse qui ne pouvait pas être analysée

L'erreur conserve les informations suivantes pour vous aider à logger l'erreur :

- `responses`: Métadonnées sur les réponses du modèle de transcription, y compris le timestamp, le modèle et les en-têtes.
- `cause`: La cause de l'erreur. Vous pouvez utiliser cela pour une gestion d'erreur plus détaillée.

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
    console.log('Cause:', error.cause);
    console.log('Responses:', error.responses);
  }
}
```

## Modèles de Transcription

| Fournisseur                                                                | Modèle                        |
| ------------------------------------------------------------------------- | ---------------------------- |
| [OpenAI](/providers/ai-sdk-providers/openai)

# Modèles de transcription
| [OpenAI](/fournisseurs/sdk-ai-providers/openai#modèles-de-transcription)         | `gpt-4o-transcribe`          |
| [OpenAI](/fournisseurs/sdk-ai-providers/openai#modèles-de-transcription)         | `gpt-4o-mini-transcribe`     |
| [ElevenLabs](/fournisseurs/sdk-ai-providers/elevenlabs#modèles-de-transcription) | `scribe_v1`                  |
| [ElevenLabs](/fournisseurs/sdk-ai-providers/elevenlabs#modèles-de-transcription

# Modèles de transcription
| `gpt-4o-transcribe`          | [Azure OpenAI](/fournisseurs/sdk-ai-providers/azure#modèles-de-transcription)    |
| `gpt-4o-mini-transcribe`     | [Rev.ai](/fournisseurs/sdk-ai-providers/revai#modèles-de-transcription)          |
| `machine`                    | [Rev.ai](/fournisseurs/sdk-ai-providers/revai#modèles-de-transcription)          |
| `low_cost`                   | [Rev.ai](/fournisseurs/sdk-ai-providers/revai#modèles-de-transcription)          |
| `fusion`                     | [Rev.ai](/fournisseurs/sdk-

# (modèles-de-transcription)
| `nova-3` (+ variantes)        |
| [Gladia](/fournisseurs/sdk-ia-providers/gladia#modèles-de-transcription)         | `par-défaut`                    |
| [AssemblyAI](/fournisseurs/sdk-ia-providers/assemblyai#modèles-de-transcription) | `meilleur`                       |
| [AssemblyAI](/fournisseurs/sdk-ia-providers/assemblyai#modèles-de-transcription) | `nano`                       |
| [Fal](/fournisseurs/sdk-ia-providers/fal#modèles-de-transcription)               | `whisper`                    |
| [Fal](/fournisseurs/sdk-ia-providers/fal#modèles-de-transcription)               | `wizper`                     |

Les modèles de transcription ci-dessus sont une petite sous-ensemble des modèles de transcription pris en charge par les

# Parole

<Note type="warning">La parole est une fonction expérimentale.</Note>

Le SDK AI fournit la fonction [`generateSpeech`](/docs/reference/ai-sdk-core/generate-speech)
pour générer des paroles à partir de texte à l'aide d'un modèle de parole.

```ts
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Bonjour, monde!',
  voice: 'alloy',
});
```

Pour accéder aux données audio générées :

```ts
const audio = audio.audioData; // données audio par exemple Uint8Array
```

## Paramètres

### Paramètres spécifiques au fournisseur

Vous pouvez définir des paramètres spécifiques au modèle avec le paramètre `providerOptions`.

```ts highlight="8-12"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Bonjour, monde!',
  providerOptions: {
    openai: {
      // ...
    },
  },
});
```

### Signaux d'abandon et les temps limités

`generateSpeech` accepte un paramètre facultatif `abortSignal` de type [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
que vous pouvez utiliser pour annuler le processus de génération de parole ou définir un temps limite.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Bonjour, monde!',
  abortSignal: AbortSignal.timeout(1000), // Annuler après 1 seconde
});
```

### En-têtes personnalisés

`generateSpeech` accepte un paramètre facultatif `headers` de type `Record<string, string>`
que vous pouvez utiliser pour ajouter des en-têtes personnalisés à la demande de génération de parole.

```ts highlight="8"
import { openai } from '@ai-sdk/openai';
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Bonjour, monde!',
  headers: { 'X-Custom-Header': 'custom-value' },
});
```

### Avertissements

Les avertissements (par exemple, des paramètres non pris en charge) sont disponibles sur la propriété `warnings`.

```ts
import { openai } from '@ai-sdk/openai';
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { readFile } from 'fs/promises';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Bonjour, monde!',
});

const warnings = audio.warnings;
```

### Gestion des Erreurs

Lorsque `generateSpeech` ne parvient pas à générer un audio valide, elle lance une exception de type [`AI_NoAudioGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-audio-generated-error).

Cette erreur peut survenir pour l'une des raisons suivantes :

- Le modèle a échoué à générer une réponse
- Le modèle a généré une réponse qui ne pouvait pas être prise en charge

L'erreur conserve les informations suivantes pour vous aider à logger l'erreur :

- `responses`: Métadonnées sur les réponses du modèle de parole, y compris le timestamp, le modèle et les en-têtes.
- `cause`: La cause de l'erreur. Vous pouvez utiliser cela pour une gestion d'erreur plus détaillée.

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
    text: 'Bonjour, monde!',
  });
} catch (error) {
  if (AI_NoAudioGeneratedError.isInstance(error)) {
    console.log('AI_NoAudioGeneratedError');
    console.log('Cause:', error.cause);
    console.log('Réponses:', error.responses);
  }
}
```

## Modèles de Parole

| Fournisseur                                                  | Modèle             |
| ------------------------------------------------------------- | ----------------- |
| [OpenAI](/providers/ai-sdk-providers/openai#modèles-de-parole) | `tts-1`           |
| [OpenAI](/providers/ai-sdk-providers/openai

# Modèles de parole) | `tts-1-hd`        |
| [OpenAI](/providers/ai-sdk-providers/openai#modèles-de-parole) | `gpt-4o-mini-tts` |
| [LMNT](/providers/ai-sdk-providers/lmnt#modèles-de-parole)     | `aurora`          |
| [LMNT](/providers/ai-sdk-providers/lmnt#modèles-de-parole)     | `blizzard`        |
| [Hume](/providers/ai-sdk-providers/hume#modèles-de-parole)     | `default`         |

Les modèles de parole ci-dessus sont un petit sous-ensemble des modèles de parole pris en charge par les fournisseurs de SDK AI. Pour plus d'informations, voir la documentation respective.

---
titre : Middleware de modèle de langage
description : Apprenez à utiliser les middleware pour améliorer le comportement des modèles de langage
---

# Middleware de modèle de langage

Le middleware de modèle de langage est un moyen d'améliorer le comportement des modèles de langage
en interceptant et en modifiant les appels aux modèles de langage.

Il peut être utilisé pour ajouter des fonctionnalités comme des garde-fous, RAG, cache et journalisation
d'une manière indépendante des modèles de langage. De tels middleware peuvent être développés et
distribués indépendamment des modèles de langage auxquels ils sont appliqués.

## Utilisation du middleware de modèle de langage

Vous pouvez utiliser le middleware de modèle de langage avec la fonction `wrapLanguageModel`. 
Elle prend un modèle de langage et un middleware de modèle de langage et retourne un nouveau
modèle de langage qui incorpore le middleware.

```ts
import { wrapLanguageModel } from 'ai';

const wrappedLanguageModel = wrapLanguageModel({
  model: votreModel,
  middleware: votreMiddlewareDeModelDeLangage,
});
```

Le modèle de langage enveloppé peut être utilisé comme n'importe quel autre modèle de langage, par exemple dans `streamText`:

```ts highlight="2"
const result = streamText({
  model: wrappedLanguageModel,
  prompt: 'Quels sont les villes aux États-Unis ?',
});
```

## Multiple middlewares

Vous pouvez fournir plusieurs middlewares à la fonction `wrapLanguageModel`.
Les middlewares seront appliqués dans l'ordre dans lequel ils sont fournis.

```ts
const wrappedLanguageModel = wrapLanguageModel({
  model: votreModel,
  middleware: [premierMiddleware, deuxièmeMiddleware],
});

// appliqué comme : premierMiddleware(deuxièmeMiddleware(votreModel))
```

## Middleware intégré

La bibliothèque AI SDK comporte plusieurs middlewares intégrés que vous pouvez utiliser pour configurer les modèles de langage :

- `extractReasoningMiddleware`: Extraie les informations de raisonnement du texte généré et les expose comme une propriété `reasoning` sur le résultat.
- `simulateStreamingMiddleware`: Simule le comportement de flux avec des réponses provenant de modèles de langage non en flux.
- `defaultSettingsMiddleware`: Applique les paramètres par défaut à un modèle de langage.

### Extraction de raisonnement

Certains fournisseurs et modèles exposent les informations de raisonnement dans le texte généré à l'aide de balises spéciales,
par exemple &lt;think&gt; et &lt;/think&gt;.

La fonction `extractReasoningMiddleware` peut être utilisée pour extraire ces informations de raisonnement et les exposer comme une propriété `reasoning` sur le résultat.

```ts
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: votreModel,
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Vous pouvez ensuite utiliser ce modèle amélioré dans des fonctions comme `generateText` et `streamText`.

La fonction `extractReasoningMiddleware` inclut également une option `startWithReasoning`.
Lorsqu'elle est définie sur `true`, la balise de raisonnement sera ajoutée au début du texte généré.
Cela est utile pour les modèles qui ne comprennent pas la balise de raisonnement au début de la réponse.
Pour plus de détails, voir la [guide DeepSeek R1](/docs/guides/r1#deepseek-r1-middleware).

### Simuler un Flux

La fonction `simulateStreamingMiddleware` peut être utilisée pour simuler le comportement de flux avec des réponses provenant de modèles de langage non en flux.
Cela est utile lorsque vous souhaitez maintenir une interface de flux cohérente même lorsque vous utilisez des modèles qui ne fournissent que des réponses complètes.

```ts
import { wrapLanguageModel, simulateStreamingMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: votreModel,
  middleware: simulateStreamingMiddleware(),
});
```

### Paramètres par Défaut

La fonction `defaultSettingsMiddleware` peut être utilisée pour appliquer des paramètres par défaut à un modèle de langage.

```ts
import { wrapLanguageModel, defaultSettingsMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: votreModel,
  middleware: defaultSettingsMiddleware({
    settings: {
      temperature: 0,5,
      maxTokens: 800,
      // note : utilisez providerMetadata au lieu de providerOptions ici :
      providerMetadata: { openai: { store: false } },
    },
  }),
});

## Implémentant le middleware de modèle de langue

<Note>
  L'implémentation du middleware de modèle de langue est une fonctionnalité avancée qui nécessite
  une bonne compréhension de la [spécification du modèle de langue](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
</Note>

Vous pouvez implémenter l'une des trois fonctions suivantes pour modifier le comportement du modèle de langue :

1. `transformParams`: Transforme les paramètres avant qu'ils ne soient passés au modèle de langue, pour les deux `doGenerate` et `doStream`.
2. `wrapGenerate`: Enveloppe la méthode `doGenerate` du [modèle de langue](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
   Vous pouvez modifier les paramètres, appeler le modèle de langue et modifier le résultat.
3. `wrapStream`: Enveloppe la méthode `doStream` du [modèle de langue](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
   Vous pouvez modifier les paramètres, appeler le modèle de langue et modifier le résultat.

Voici quelques exemples d'implémentation de middleware de modèle de langue :

## Exemples

<Note>
  Ces exemples ne sont pas destinés à être utilisés en production. Ils sont juste pour montrer
  comment vous pouvez utiliser le middleware pour améliorer le comportement des modèles de langue.
</Note>

### Logging

Cet exemple montre comment logger les paramètres et le texte généré d'une appelle à un modèle de langage.

```ts
import type { LanguageModelV1Middleware, LanguageModelV1StreamPart } from 'ai';

export const votreMiddlewareDeLog : LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    console.log('doGenerate appelé');
    console.log(`params : ${JSON.stringify(params, null, 2)}`);

    const result = await doGenerate();

    console.log('doGenerate terminé');
    console.log(`texte généré : ${result.text}`);

    return result;
  },

  wrapStream: async ({ doStream, params }) => {
    console.log('doStream appelé');
    console.log(`params : ${JSON.stringify(params, null, 2)}`);

    const { stream, ...rest } = await doStream();

    let texteGénéré = '';

    const transformStream = new TransformStream<
      LanguageModelV1StreamPart,
      LanguageModelV1StreamPart
    >({
      transform(chunk, controller) {
        if (chunk.type === 'text-delta') {
          texteGénéré += chunk.textDelta;
        }

        controller.enqueue(chunk);
      },

      flush() {
        console.log('doStream terminé');
        console.log(`texte généré : ${texteGénéré}`);
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

Cet exemple montre comment construire un cache simple pour le texte généré d'une appel à un modèle de langage.

```ts
import type { LanguageModelV1Middleware } from 'ai';

const cache = new Map<string, any>();

export const votreMiddlewareDeCache: LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    const cacheKey = JSON.stringify(params);

    if (cache.has(cacheKey)) {
      return cache.get(cacheKey);
    }

    const result = await doGenerate();

    cache.set(cacheKey, result);

    return result;
  },

  // ici vous implémenteriez la logique de caching pour le streaming
};
```

### Génération Augmentée par la Recherche (RAG)

Cet exemple montre comment utiliser RAG en tant que middleware.

<Note>
  Les fonctions d'aide comme `getLastUserMessageText` et `findSources` ne font pas partie de la bibliothèque AI. Ils sont juste utilisés dans cet exemple pour illustrer le concept de RAG.
</Note>

```ts
import type { LanguageModelV1Middleware } from 'ai';

export const votreMiddlewareDeRag: LanguageModelV1Middleware = {
  transformParams: async ({ params }) => {
    const dernierTexteDeMessageUtilisateur = getLastUserMessageText({
      prompt: params.prompt,
    });

    if (dernierTexteDeMessageUtilisateur == null) {
      return params; // ne pas utiliser RAG (envoyer les paramètres non modifiés)
    }

    const instruction =
      'Utilisez les informations suivantes pour répondre à la question :\n' +
      findSources({ text: dernierTexteDeMessageUtilisateur })
        .map(chunk => JSON.stringify(chunk))
        .join('\n');

    return addToLastUserMessage({ params, text: instruction });
  },
};
```

### Barrières de sécurité

Les barrières de sécurité sont un moyen d'assurer que le texte généré d'une appel à un modèle de langage est sûr et approprié.  Cet exemple montre comment utiliser les barrières de sécurité en tant que middleware.

```ts
import type { LanguageModelV1Middleware } from 'ai';

export const votreMiddlewareDeBarriereDeSécurité: LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate }) => {
    const { text, ...rest } = await doGenerate();

    // approche de filtration, par exemple pour les informations personnelles sensibles ou autres :
    const texteNettoyé = text?.replace(/motmauvais/g, '<REDACTÉ>');

    return { text: texteNettoyé, ...rest };
  },

  // ici vous implémenteriez la logique de la barrière de sécurité pour les flux
  // Note : les barrières de sécurité pour les flux sont difficiles à mettre en œuvre, car
  // vous ne connaissez pas le contenu complet du flux jusqu'à ce qu'il soit terminé.
};
```

## Configuration des métadonnées personnalisées par requête

Pour envoyer et accéder à des métadonnées personnalisées dans le Middleware, vous pouvez utiliser `providerOptions`. Cela est utile lors de la construction de middleware de logging où vous souhaitez passer des contextes supplémentaires comme les ID d'utilisateurs, les horodatages ou d'autres données contextuelles qui peuvent aider à la traçabilité et à la débogage.

```ts
import { openai } from '@ai-sdk/openai';
import { generateText, wrapLanguageModel, LanguageModelV1Middleware } from 'ai';

export const votreMiddlewareDeLog : LanguageModelV1Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    console.log('MÉTADONNÉES', params?.providerMetadata?.votreMiddlewareDeLog);
    const result = await doGenerate();
    return result;
  },
};

const { text } = await generateText({
  model: wrapLanguageModel({
    model: openai('gpt-4o'),
    middleware: votreMiddlewareDeLog,
  }),
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  providerOptions: {
    votreMiddlewareDeLog: {
      hello: 'monde',
    },
  },
});

console.log(text);
```

---
titre : Gestion du fournisseur et du modèle
description : Apprenez à travailler avec plusieurs fournisseurs et modèles
---

# Gestion des fournisseurs et des modèles

Lorsque vous travaillez avec plusieurs fournisseurs et modèles, il est souvent souhaitable de les gérer dans un endroit central et d'accéder aux modèles à l'aide d'identifiants de chaîne simples.

Le SDK AI propose [des fournisseurs personnalisés](/docs/reference/ai-sdk-core/fournisseur-personnalise) et un [registre de fournisseurs](/docs/reference/ai-sdk-core/registre-de-fournisseurs) à cette fin :

- Avec **les fournisseurs personnalisés**, vous pouvez pré-configurer les paramètres des modèles, fournir des alias de nom de modèle et limiter les modèles disponibles.
- Le **registre de fournisseurs** vous permet de mélanger plusieurs fournisseurs et d'y accéder à l'aide d'identifiants de chaîne simples.

Vous pouvez mélanger et combiner les fournisseurs personnalisés, le registre de fournisseurs et [le middleware](/docs/ai-sdk-core/middleware) dans votre application.

## Fournisseurs personnalisés

Vous pouvez créer un [fournisseur personnalisé](/docs/reference/ai-sdk-core/fournisseur-personnalise) à l'aide de `customProvider`.

### Exemple : paramètres de modèle personnalisés

Vous pourriez vouloir remplacer les paramètres de modèle par défaut d'un fournisseur ou fournir des alias de modèle avec des paramètres pré-configurés.

```ts
import { openai as originalOpenAI } from '@ai-sdk/openai';
import { customProvider } from 'ai';

// fournisseur personnalisé avec des paramètres de modèle différents :
export const openai = customProvider({
  languageModels: {
    // modèle de remplacement avec des paramètres personnalisés :
    'gpt-4o': originalOpenAI('gpt-4o', { outputsStructurés : true }),
    // alias de modèle avec des paramètres personnalisés :
    'gpt-4o-mini-structurés' : originalOpenAI('gpt-4o-mini', {
      outputsStructurés : true,
    }),
  },
  fallbackProvider: originalOpenAI,
});
```

### Exemple : nom d'alias du modèle

Vous pouvez également fournir des alias de noms de modèle, afin de pouvoir mettre à jour la version du modèle dans un seul endroit à l'avenir :

```ts
import { anthropic as originalAnthropic } from '@ai-sdk/anthropic';
import { customProvider } from 'ai';

// fournisseur personnalisé avec des noms d'alias :
export const anthropic = customProvider({
  languageModels: {
    opus: originalAnthropic('claude-3-opus-20240229'),
    sonnet: originalAnthropic('claude-3-5-sonnet-20240620'),
    haiku: originalAnthropic('claude-3-haiku-20240307'),
  },
  fallbackProvider: originalAnthropic,
});
```

### Exemple : limitation des modèles disponibles

Vous pouvez limiter les modèles disponibles dans le système, même si vous avez plusieurs fournisseurs.

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
  // pas de fournisseur par défaut
});
```

## Registre de fournisseurs

Vous pouvez créer un [registre de fournisseurs](/docs/reference/ai-sdk-core/provider-registry) avec plusieurs fournisseurs et modèles en utilisant `createProviderRegistry`.

### Configuration

```ts filename={"registry.ts"}
import { anthropic } from '@ai-sdk/anthropic';
import { createOpenAI } from '@ai-sdk/openai';
import { createProviderRegistry } from 'ai';

export const registry = createProviderRegistry({
  // enregistrer le fournisseur avec le préfixe et la configuration par défaut :
  anthropic,

  // enregistrer le fournisseur avec le préfixe et la configuration personnalisée :
  openai: createOpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  }),
});
```

### Configuration avec Séparateur personnalisé

Par défaut, la registre utilise `:` comme séparateur entre les identifiants de fournisseur et de modèle. Vous pouvez personnaliser ce séparateur :

```ts filename={"registry.ts"}
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';

export const customSeparatorRegistry = createProviderRegistry(
  {
    anthropic,
    openai,
  },
  { separator: ' > ' },
);
```

### Exemple : Utiliser les modèles de langage

Vous pouvez accéder aux modèles de langage en utilisant la méthode `languageModel` sur la registre.
L'identifiant de fournisseur deviendra le préfixe de l'identifiant de modèle : `providerId:modelId`.

```ts highlight={"5"}
import { generateText } from 'ai';
import { registry } from './registry';

const { text } = await generateText({
  model: registry.languageModel('openai:gpt-4-turbo'), // séparateur par défaut
  // ou avec séparateur personnalisé :
  // model: customSeparatorRegistry.languageModel('openai > gpt-4-turbo'),
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
});
```

### Exemple : Utiliser des modèles d'embedage de texte

Vous pouvez accéder aux modèles d'embedage de texte en utilisant la méthode `textEmbeddingModel` sur le registre.
L'identifiant du fournisseur deviendra le préfixe de l'identifiant du modèle : `providerId:modelId`.

```ts highlight={"5"}
import { embed } from 'ai';
import { registry } from './registry';

const { embedding } = await embed({
  model: registry.textEmbeddingModel('openai:text-embedding-3-small'),
  value: 'jour ensoleillé à la plage',
});
```

### Exemple : Utiliser des modèles d'image

Vous pouvez accéder aux modèles d'image en utilisant la méthode `imageModel` sur le registre.
L'identifiant du fournisseur deviendra le préfixe de l'identifiant du modèle : `providerId:modelId`.

```ts highlight={"5"}
import { generateImage } from 'ai';
import { registry } from './registry';

const { image } = await generateImage({
  model: registry.imageModel('openai:dall-e-3'),
  prompt: 'Un coucher de soleil magnifique sur un océan calme',
});
```

## Combinaison de fournisseurs personnalisés, d'un registre de fournisseurs et de middleware

L'idée centrale de la gestion des fournisseurs est de configurer un fichier contenant tous les fournisseurs et les modèles que vous souhaitez utiliser.
Vous pouvez vouloir pré-configurer les paramètres de modèle, fournir des alias de nom de modèle, limiter les modèles disponibles, et plus encore.

Voici un exemple qui implémente les concepts suivants :

- passer un fournisseur complet avec un préfixe de namespace (ici : `xai > *`)
- configurer un fournisseur compatible avec OpenAI avec une clé API personnalisée et une URL de base (ici : `custom > *`)
- configurer des alias de nom de modèle (ici : `anthropic > fast`, `anthropic > writing`, `anthropic > reasoning`)
- pré-configurer les paramètres de modèle (ici : `anthropic > reasoning`)
- valider les options spécifiques au fournisseur (ici : `AnthropicProviderOptions`)
- utiliser un fournisseur de remplacement (ici : `anthropic > *`)
- limiter un fournisseur à certains modèles sans fournisseur de remplacement (ici : `groq > gemma2-9b-it`, `groq > qwen-qwq-32b`)
- définir un séparateur personnalisé pour le registre de fournisseurs (ici : `>`)

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

export const registre = createProviderRegistry(
  {
    // passer un fournisseur complet avec un préfixe de namespace
    xai,

    // accéder à un fournisseur compatible avec OpenAI avec une configuration personnalisée
    custom: createOpenAICompatible({
      name: 'nom-du-fournisseur',
      apiKey: process.env.CUSTOM_API_KEY,
      baseURL: 'https://api.custom.com/v1',
    }),
```

```ts
  // configurer des alias de nom de modèle
  modelAliases: {
    'anthropic > fast': 'fast',
    'anthropic > writing': 'writing',
    'anthropic > reasoning': 'reasoning',
  },

  // pré-configurer les paramètres de modèle
  modelSettings: {
    'anthropic > reasoning': {
      // configuration personnalisée pour le modèle 'anthropic > reasoning'
    },
  },

  // valider les options spécifiques au fournisseur
  validateProviderOptions: {
    'custom': (options: AnthropicProviderOptions) => {
      // validation personnalisée pour les options du fournisseur 'custom'
    },
  },

  // utiliser un fournisseur de remplacement
  fallbackProvider: 'anthropic > *',

  // limiter un fournisseur à

// configuration des noms d'alias pour le modèle
    anthropic: customProvider({
      languageModels: {
        rapide: customProvider({
          languageModels: {
            claude-3-haiku-20240307
          }
        }),

        // modèle simple
        écriture: customProvider({
          languageModels: {
            claude-3-7-sonnet-20250219
          }
        }),

        // configuration du modèle de raisonnement étendu :
        raisonnement: wrapLanguageModel({
          model: customProvider({
            languageModels: {
              claude-3-7-sonnet-20250219
            }
          }),
          middleware: defaultSettingsMiddleware({
            settings: {
              maxTokens: 100000, // exemple de paramètre par défaut
              providerMetadata: {


### Limitation d'un fournisseur à certains modèles sans redirigeement

    // limite un fournisseur à certains modèles sans un redirigeement par défaut
    groq: customProvider({
      languageModels: {
        'gemma2-9b-it': groq('gemma2-9b-it'),
        'qwen-qwq-32b': groq('qwen-qwq-32b'),
      },
    }),
  },
  { séparateur: ' > ' },
);

### Exemple d'utilisation :

```javascript
const modèle = registre.languageModel('anthropic > raisonnement');
```

---
titre : Gestion des erreurs
description : Apprenez à gérer les erreurs dans le no

# Gestion des Erreurs

## Gestion des erreurs régulières

Les erreurs régulières sont lancées et peuvent être gérées à l'aide du bloc `try/catch`.

```ts highlight="3,8-10"
import { generateText } from 'ai';

try {
  const { text } = await generateText({
    model: votreModel,
    prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
  });
} catch (error) {
  // gérer l'erreur
}
```

Consultez [Types d'Erreurs](/docs/reference/ai-sdk-errors) pour plus d'informations sur les différents types d'erreurs qui peuvent être lancées.

## Gestion des erreurs de flux (flux simples)

Lorsque des erreurs se produisent pendant les flux qui ne supportent pas les tronçons d'erreur,
l'erreur est lancée comme une erreur régulière.
Vous pouvez gérer ces erreurs à l'aide du bloc `try/catch`.

```ts highlight="3,12-14"
import { generateText } from 'ai';

try {
  const { textStream } = streamText({
    model: votreModel,
    prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
  });

  for await (const textPart of textStream) {
    process.stdout.write(textPart);
  }
} catch (error) {
  // gérer l'erreur
}
```

## Gestion des erreurs de streaming (streaming avec prise en charge `error`)

Les flux complets prennent en charge les parties d'erreur.
Vous pouvez gérer ces parties de la même manière que les autres parties.
Il est recommandé d'ajouter également un bloc try-catch pour les erreurs qui se produisent en dehors de la streaming.

```ts highlight="13-17"
import { generateText } from 'ai';

try {
  const { fullStream } = streamText({
    model: votreModel,
    prompt: 'Écrivez une recette de lasagnes végétariennes pour 4 personnes.',
  });

  for await (const partie of fullStream) {
    switch (partie.type) {
      // ... gérer les autres types de partie

      case 'error': {
        const erreur = partie.error;
        // gérer l'erreur
        break;
      }
    }
  }
} catch (erreur) {
  // gérer l'erreur
}
```

---
titre : Test
description : Apprenez à utiliser les fournisseurs de simulation de la plateforme AI SDK Core pour les tests.
---

# Test

La mise en œuvre de tests pour les modèles de langage peut être difficile, car ils sont non déterministes
et leur appel est lent et coûteux.

Pour vous permettre de tester unitaire votre code qui utilise le SDK AI, le noyau AI inclut des fournisseurs de simulation et des outils de test. Vous pouvez importer les aides suivantes à partir de `ai/test` :

- `MockEmbeddingModelV1`: Un modèle d'embeddings de simulation utilisant la [spécification du modèle d'embeddings v1](https://github.com/vercel/ai/blob/main/packages/provider/src/embedding-model/v1/embedding-model-v1.ts).
- `MockLanguageModelV1`: Un modèle de langage de simulation utilisant la [spécification du modèle de langage v1](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts).
- `mockId`: fournit un ID entier incrémental.
- `mockValues`: itère sur un tableau de valeurs à chaque appel. Retourne la dernière valeur lorsque le tableau est épuisé.
- [`simulateReadableStream`](/docs/reference/ai-sdk-core/simulate-readable-stream) : Simule un flux lisible avec des retards.

Avec des fournisseurs de simulation et des outils de test, vous pouvez contrôler la sortie du SDK AI
et tester votre code d'une manière répétitive et déterministe sans appeler effectivement un fournisseur de modèle de langage.

## Exemples

Vous pouvez utiliser les outils de test avec les fonctions du noyau AI dans vos tests unitaires :

### generateText

```ts
import { generateText } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';

const result = await generateText({
  model: new MockLanguageModelV1({
    doGenerate: async () => ({
      rawCall: { rawPrompt: null, rawSettings: {} },
      finishReason: 'stop',
      usage: { promptTokens: 10, completionTokens: 20 },
      text: `Bonjour, monde !`,
    }),
  }),
  prompt: 'Bonjour, test !',
});
```

### streamText

```ts
import { streamText, simulateReadableStream } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';

const result = streamText({
  model: new MockLanguageModelV1({
    doStream: async () => ({
      stream: simulateReadableStream({
        chunks: [
          { type: 'text-delta', textDelta: 'Bonjour' },
          { type: 'text-delta', textDelta: ', ' },
          { type: 'text-delta', textDelta: `monde !` },
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
  prompt: 'Bonjour, test !',
});
```

### generateObject

```ts
import { generateObject } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';
import { z } from 'zod';

const result = await generateObject({
  model: new MockLanguageModelV1({
    defaultObjectGenerationMode: 'json',
    doGenerate: async () => ({
      rawCall: { rawPrompt: null, rawSettings: {} },
      finishReason: 'stop',
      usage: { promptTokens: 10, completionTokens: 20 },
      text: `{"content":"Bonjour, monde!"}`,
    }),
  }),
  schema: z.object({ contenu: z.string() }),
  prompt: 'Bonjour, test!',
});
```

### objetDeFlux

```ts
import { streamObject, simulateReadableStream } from 'ai';
import { MockLanguageModelV1 } from 'ai/test';
import { z } from 'zod';

const result = streamObject({
  model: new MockLanguageModelV1({
    defaultObjectGenerationMode: 'json',
    doStream: async () => ({
      stream: simulateReadableStream({
        chunks: [
          { type: 'text-delta', textDelta: '{ ' },
          { type: 'text-delta', textDelta: '"content": ' },
          { type: 'text-delta', textDelta: `"Hello, ` },
          { type: 'text-delta', textDelta: `world` },
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
  schema: z.object({ content: z.string() }),
  prompt: 'Bonjour, test!',
});
```

### Simuler les Réponses du Protocole de Données en Flux

Vous pouvez également simuler [le Protocole de Données en Flux](/docs/ai-sdk-ui/stream-protocol)

# Protocole de données de flux) pour les fins de test, de débogage ou de démonstration.

Voici un exemple Next :

```ts filename="route.ts"
import { simulateReadableStream } from 'ai';

export async function POST(req: Request) {
  return new Response(
    simulateReadableStream({
      initialDelayInMs: 1000, // Retard avant le premier morceau
      chunkDelayInMs: 300, // Retard entre les morceaux
      chunks: [
        `0:"This"\n`,
        `0:" est un"\n`,
        `0:"exemple."\n`,
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
titre : Telemétrie
description : Utilisation d'OpenTelemetry avec AI SDK Core
---

# Telemétrie

<Remarque type="avertissement">
  La telemétrie AI SDK est expérimentale et peut changer à l'avenir.
</Remarque>

L'API AI utilise [OpenTelemetry](https://opentelemetry.io/) pour collecter des données de telemétrie.
OpenTelemetry est un framework d'observabilité open-source conçu pour fournir une instrumentation normalisée pour la collecte de données de telemétrie.

Consultez les [Intégrations d'observabilité AI SDK](/providers/observability)
pour voir les fournisseurs qui proposent des suivi et des tracés pour les applications AI SDK.

## Activation de la telemétrie

Pour les applications Next.js, veuillez suivre la [guide OpenTelemetry de Next.js](https://nextjs.org/docs/app/building-your-application/optimizing/open-telemetry) pour activer la telemétrie en premier lieu.

Vous pouvez ensuite utiliser l'option `experimental_telemetry` pour activer la telemétrie sur des appels de fonction spécifiques pendant que la fonctionnalité est en phase d'expérimentation :

```ts highlight="4"
const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Écrivez une histoire courte sur un chat.',
  experimental_telemetry: { isEnabled: true },
});
```

Lorsque la telemétrie est activée, vous pouvez également contrôler si vous souhaitez enregistrer les valeurs d'entrée et les valeurs de sortie de la fonction.
Par défaut, les deux sont activés. Vous pouvez les désactiver en définissant les options `recordInputs` et `recordOutputs` sur `false`.

La désactivation de l'enregistrement des entrées et des sorties peut être utile pour des raisons de confidentialité, de transfert de données et de performance.
Vous pouvez par exemple vouloir désactiver l'enregistrement des entrées si elles contiennent des informations sensibles.

## Méta-données de telemétrie

Vous pouvez fournir un `functionId` pour identifier la fonction pour laquelle les données de telemétrie sont, 
et `metadata` pour inclure des informations supplémentaires dans les données de telemétrie.

```ts highlight="6-10"
const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Écrivez une histoire courte sur un chat.',
  experimental_telemetry: {
    isEnabled: true,
    functionId: 'ma-fonction-merveilleuse',
    metadata: {
      quelqueChose: 'custom',
      autreChose: 'autre-valeur',
    },
  },
});
```

## Tracer personnalisé

Vous pouvez fournir un `tracer` qui doit retourner un `Tracer` OpenTelemetry. Cela est utile dans des situations où vous souhaitez que vos traces utilisent un `TracerProvider` autre que celui fourni par le singleton `@opentelemetry/api`.

```ts highlight="7"
const tracerProvider = new NodeTracerProvider();
const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Écrivez une histoire courte sur un chat.',
  experimental_telemetry: {
    isEnabled: true,
    tracer: tracerProvider.getTracer('ai'),
  },
});
```

## Données collectées

### fonction generateText

`generateText` enregistre 3 types de spans :

- `ai.generateText` (span) : la longueur complète de l'appel generateText. Il contient 1 ou plusieurs spans `ai.generateText.doGenerate`.
  Il contient les informations de span LLM de base et les attributs suivants :

  - `operation.name` : `ai.generateText` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId` : `"ai.generateText"`
  - `ai.prompt` : la prompt qui a été utilisée lors de l'appel à `generateText`
  - `ai.response.text` : le texte qui a été généré
  - `ai.response.toolCalls` : les appels d'outil qui ont été effectués en tant que partie de la génération (JSON stringifié)
  - `ai.response.finishReason` : la raison pour laquelle la génération a terminé
  - `ai.settings.maxSteps` : le nombre maximum de pas qui a été défini

- `ai.generateText.doGenerate` (span) : un appel doGenerate du fournisseur. Il peut contenir des spans `ai.toolCall`.
  Il contient les informations de span d'appel LLM et

# call-llm-span-information) et les attributs suivants :

  - `operation.name`: `ai.generateText.doGenerate` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.generateText.doGenerate"`
  - `ai.prompt.format`: le format de la demande
  - `ai.prompt.messages`: les messages qui ont été passés dans le fournisseur
  - `ai.prompt.tools`: tableau de définitions de outils stringifiées. Les outils peuvent être de type `function` ou `provider-defined`.
    Les outils de type `function` ont un `name`, une `description` (facultative) et des `parameters` (schéma JSON).
    Les outils définis par le fournisseur ont un `name`, un `id` et des `args` (Record).
  - `ai.prompt.toolChoice`: la définition de l'outil de choix stringifiée (JSON). Il a une propriété `type` (`auto`, `none`, `required`, `tool`) et si le type est `tool`, une propriété `toolName` avec l'outil spécifique.
  - `ai.response.text`: le texte qui a été généré
  - `ai.response.toolCalls`: les appels d'outil qui ont été effectués en tant que partie de la génération (stringifié JSON)
  - `ai.response.finishReason`: la raison pour laquelle la génération s'est terminée

- `ai.toolCall` (span): un appel d'outil effectué en tant que partie de la génération du texte. Voir [Tool call spans](#tool-call-spans) pour plus de détails.

### fonction streamText

`streamText` enregistre 3 types de spans et 2 types d'événements :

- `ai.streamText` (span): la longueur totale de l'appel streamText. Il contient un `ai.streamText.doStream` span.
  Il contient l'[information de span LLM de base](

# Informations sur la span LLM basique) et les attributs suivants :

  - `operation.name`: `ai.streamText` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.streamText"`
  - `ai.prompt`: la prompt qui a été utilisée lors de l'appel à `streamText`
  - `ai.response.text`: le texte qui a été généré
  - `ai.response.toolCalls`: les appels de l'outil qui ont été effectués en tant que partie de la génération (JSON stringifié)
  - `ai.response.finishReason`: la raison pour laquelle la génération s'est terminée
  - `ai.settings.maxSteps`: le nombre maximum de pas qui ont été définis

- `ai.streamText.doStream` (span): un appel doStream fourni par un fournisseur.
  Cette span contient un événement `ai.stream.firstChunk` et des spans `ai.toolCall`.
  Elle contient les [informations sur la span LLM d'appel](

# (call-llm-span-information) et les attributs suivants :

  - `operation.name` : `ai.streamText.doStream` et l'ID de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId` : `"ai.streamText.doStream"`
  - `ai.prompt.format` : le format de la demande
  - `ai.prompt.messages` : les messages qui ont été passés dans le fournisseur
  - `ai.prompt.tools` : tableau de définitions de outils en chaîne. Les outils peuvent être de type `function` ou `provider-defined`.
    Les outils de type `function` ont un `name`, une `description` (facultative) et des `parameters` (schéma JSON).
    Les outils définis par le fournisseur ont un `name`, un `id` et des `args` (Record).
  - `ai.prompt.toolChoice` : la définition de l'outil choisi en chaîne (JSON). Il a une propriété `type` (`auto`, `none`, `required`, `tool`) et si le type est `tool`, une propriété `toolName` avec le nom spécifique de l'outil.
  - `ai.response.text` : le texte généré
  - `ai.response.toolCalls` : les appels d'outil qui ont été effectués en tant que partie de la génération (JSON en chaîne)
  - `ai.response.msToFirstChunk` : le temps mis pour recevoir le premier morceau en millisecondes
  - `ai.response.msToFinish` : le temps mis pour recevoir la fin de la partie LLM en millisecondes
  - `ai.response.avgCompletionTokensPerSecond` : le nombre moyen de tokens de complétion par seconde
  - `ai.response.finishReason` : la raison pour laquelle la génération a terminé

- `ai.toolCall` (span) : un appel d'outil qui est effectué en tant que partie de l'appel `generateText`. Voir [Tool call spans](

#tool-call-spans) pour plus de détails.

- `ai.stream.firstChunk` (événement): un événement émis lorsque le premier morceau du flux est reçu.

  - `ai.response.msToFirstChunk`: le temps mis pour recevoir le premier morceau

- `ai.stream.finish` (événement): un événement émis lorsque la partie fin de la LLM stream est reçue.

Il enregistre également un événement `ai.stream.firstChunk` lorsque le premier morceau du flux est reçu.

### fonction generateObject

`generateObject` enregistre 2 types de spans :

- `ai.generateObject` (span): la durée complète de l'appel generateObject. Il contient 1 ou plusieurs `ai.generateObject.doGenerate` spans.
  Il contient les [informations de span LLM de base](#basic-llm-span-information) et les attributs suivants :

  - `operation.name`: `ai.generateObject` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.generateObject"`
  - `ai.prompt`: la prompt qui a été utilisée lors de l'appel `generateObject`
  - `ai.schema`: la version de schéma JSON stringifiée du schéma qui a été passé dans la fonction `generateObject`
  - `ai.schema.name`: le nom du schéma qui a été passé dans la fonction `generateObject`
  - `ai.schema.description`: la description du schéma qui a été passé dans la fonction `generateObject`
  - `ai.response.object`: l'objet qui a été généré (JSON stringifié)
  - `ai.settings.mode`: le mode de génération d'objet, par exemple `json`
  - `ai.settings.output`: le type de sortie qui a été utilisé, par exemple `object` ou `no-schema`

- `ai.generateObject.doGenerate` (span): un appel doGenerate du fournisseur.
  Il contient les [informations de span d'appel LLM](

# call-llm-span-information) et les attributs suivants :

  - `operation.name`: `ai.generateObject.doGenerate` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.generateObject.doGenerate"`
  - `ai.prompt.format`: le format de la demande
  - `ai.prompt.messages`: les messages qui ont été passés dans le fournisseur
  - `ai.response.object`: l'objet qui a été généré (JSON stringifié)
  - `ai.settings.mode`: le mode de génération d'objet
  - `ai.response.finishReason`: la raison pour laquelle la génération s'est terminée

### fonction streamObject

`streamObject` enregistre 2 types de spans et 1 type d'événement :

- `ai.streamObject` (span) : la longueur totale de l'appel streamObject. Il contient 1 ou plusieurs `ai.streamObject.doStream` spans.
  Il contient l'[information de span LLM de base](

# Informations de span de LLM de base) et les attributs suivants :

  - `operation.name`: `ai.streamObject` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.streamObject"`
  - `ai.prompt`: la prompt qui a été utilisée lors de l'appel `streamObject`
  - `ai.schema`: schéma JSON version stringifiée du schéma qui a été passé dans la fonction `streamObject`
  - `ai.schema.name`: le nom du schéma qui a été passé dans la fonction `streamObject`
  - `ai.schema.description`: la description du schéma qui a été passé dans la fonction `streamObject`
  - `ai.response.object`: l'objet généré (JSON stringifié)
  - `ai.settings.mode`: le mode de génération d'objet, par exemple `json`
  - `ai.settings.output`: le type de sortie utilisé, par exemple `object` ou `no-schema`

- `ai.streamObject.doStream` (span) : une appelle doStream d'un fournisseur.
  Cette span contient un événement `ai.stream.firstChunk`.
  Elle contient les [informations de span de LLM de base](

# (call-llm-span-information) et les attributs suivants :

  - `operation.name`: `ai.streamObject.doStream` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.streamObject.doStream"`
  - `ai.prompt.format`: le format de la prompt
  - `ai.prompt.messages`: les messages qui ont été passés dans le fournisseur
  - `ai.settings.mode`: le mode de génération d'objets
  - `ai.response.object`: l'objet généré (JSON stringifié)
  - `ai.response.msToFirstChunk`: le temps mis pour recevoir le premier morceau
  - `ai.response.finishReason`: la raison pour laquelle la génération s'est terminée

- `ai.stream.firstChunk` (événement): un événement émis lorsque le premier morceau de la stream est reçu.
  - `ai.response.msToFirstChunk`: le temps mis pour recevoir le premier morceau

### fonction d'embed

`embed` enregistre 2 types de spans :

- `ai.embed` (span) : la durée complète de l'appel d'embed. Il contient 1 `ai.embed.doEmbed` spans.
  Il contient les [informations de span d'embedage de base](#basic-embedding-span-information) et les attributs suivants :

  - `operation.name`: `ai.embed` et l'identifiant de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.embed"`
  - `ai.value`: la valeur qui a été passée dans la fonction `embed`
  - `ai.embedding`: un embedage en JSON-stringifié

- `ai.embed.doEmbed` (span) : un appel de doEmbed du fournisseur.
  Il contient les [informations de span d'embedage de base](#basic-embedding-span-information)

# Embedding d'informations de span de base) et les attributs suivants :

  - `operation.name`: `ai.embed.doEmbed` et l'ID de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.embed.doEmbed"`
  - `ai.values`: les valeurs qui ont été passées dans le fournisseur (tableau)
  - `ai.embeddings`: un tableau de chaînes JSON-stringifiées d'embeddings

### fonction embedMany

`embedMany` enregistre 2 types de spans :

- `ai.embedMany` (span) : la longueur complète de l'appel à embedMany. Il contient 1 ou plusieurs spans `ai.embedMany.doEmbed`.
  Il contient les [informations de span d'embedding de base](#basic-embedding-span-information) et les attributs suivants :

  - `operation.name`: `ai.embedMany` et l'ID de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.embedMany"`
  - `ai.values`: les valeurs qui ont été passées dans la fonction `embedMany`
  - `ai.embeddings`: un tableau de chaînes JSON-stringifiées d'embeddings

- `ai.embedMany.doEmbed` (span) : un appel doEmbed du fournisseur.
  Il contient les [informations de span d'embedding de base](#basic-embedding-span-information) et les attributs suivants :

  - `operation.name`: `ai.embedMany.doEmbed` et l'ID de fonction qui a été défini à travers `telemetry.functionId`
  - `ai.operationId`: `"ai.embedMany.doEmbed"`
  - `ai.values`: les valeurs qui ont été envoyées au fournisseur
  - `ai.embeddings`: un tableau de chaînes JSON-stringifiées d'embeddings pour chaque valeur

## Détails de l'espacement

### Informations de base sur l'espacement LLM

De nombreux espacements qui utilisent des LLMs (`ai.generateText`, `ai.generateText.doGenerate`, `ai.streamText`, `ai.streamText.doStream`,
`ai.generateObject`, `ai.generateObject.doGenerate`, `ai.streamObject`, `ai.streamObject.doStream`) contiennent les attributs suivants :

- `resource.name`: l'identifiant de la fonction qui a été défini à travers `telemetry.functionId`
- `ai.model.id`: l'identifiant du modèle
- `ai.model.provider`: le fournisseur du modèle
- `ai.request.headers.*`: les en-têtes de demande qui ont été passés à travers `headers`
- `ai.settings.maxRetries`: le nombre maximum de tentatives qui ont été définies
- `ai.telemetry.functionId`: l'identifiant de la fonction qui a été défini à travers `telemetry.functionId`
- `ai.telemetry.metadata.*`: les métadonnées qui ont été passées à travers `telemetry.metadata`
- `ai.usage.completionTokens`: le nombre de jetons de complétion qui ont été utilisés
- `ai.usage.promptTokens`: le nombre de jetons de prompt qui ont été utilisés

### Informations de l'appel LLM

Les espacements qui correspondent à des appels individuels LLM (`ai.generateText.doGenerate`, `ai.streamText.doStream`, `ai.generateObject.doGenerate`, `ai.streamObject.doStream`) contiennent
[informations de base sur l'espacement LLM](

# Informations sur les espaces de noms LLM basiques et les attributs suivants :

- `ai.response.model`: le modèle utilisé pour générer la réponse. Cela peut être différent du modèle demandé si le fournisseur prend en charge les alias.
- `ai.response.id`: l'ID de la réponse. Utilise l'ID du fournisseur lorsque disponible.
- `ai.response.timestamp`: l'heure de la réponse. Utilise l'heure du fournisseur lorsque disponible.
- [Conventions sémantiques pour les opérations GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/)
  - `gen_ai.system`: le fournisseur utilisé
  - `gen_ai.request.model`: le modèle demandé
  - `gen_ai.request.temperature`: la température définie
  - `gen_ai.request.max_tokens`: le nombre maximum de jetons défini
  - `gen_ai.request.frequency_penalty`: le penalty de fréquence défini
  - `gen_ai.request.presence_penalty`: le penalty de présence défini
  - `gen_ai.request.top_k`: la valeur de topK définie
  - `gen_ai.request.top_p`: la valeur de topP définie
  - `gen_ai.request.stop_sequences`: les séquences d'arrêt
  - `gen_ai.response.finish_reasons`: les raisons de fin retournées par le fournisseur
  - `gen_ai.response.model`: le modèle utilisé pour générer la réponse. Cela peut être différent du modèle demandé si le fournisseur prend en charge les alias.
  - `gen_ai.response.id`: l'ID de la réponse. Utilise l'ID du fournisseur lorsque disponible.
  - `gen_ai.usage.input_tokens`: le nombre de jetons de prompt utilisés
  - `gen_ai.usage.output_tokens`: le nombre de jetons de complétion utilisés

### Informations de base sur l'encartage de span

Beaucoup d'encartages qui utilisent des modèles d'encartage (`ai.embed`, `ai.embed.doEmbed`, `ai.embedMany`, `ai.embedMany.doEmbed`) contiennent les attributs suivants :

- `ai.model.id`: l'identifiant du modèle
- `ai.model.provider`: le fournisseur du modèle
- `ai.request.headers.*`: les en-têtes de requête qui ont été passés à travers `headers`
- `ai.settings.maxRetries`: le nombre maximum de réessais qui ont été définis
- `ai.telemetry.functionId`: l'identifiant de la fonction qui a été défini à travers `telemetry.functionId`
- `ai.telemetry.metadata.*`: les métadonnées qui ont été passées à travers `telemetry.metadata`
- `ai.usage.tokens`: le nombre de jetons qui ont été utilisés
- `resource.name`: l'identifiant de la fonction qui a été défini à travers `telemetry.functionId`

### Encartages d'appel de l'outil

Les encartages d'appel d'outil (`ai.toolCall`) contiennent les attributs suivants :

- `operation.name`: `"ai.toolCall"`
- `ai.operationId`: `"ai.toolCall"`
- `ai.toolCall.name`: le nom de l'outil
- `ai.toolCall.id`: l'identifiant de l'appel d'outil
- `ai.toolCall.args`: les paramètres de l'appel d'outil
- `ai.toolCall.result`: le résultat de l'appel d'outil. Disponible uniquement si l'appel d'outil est réussi et que le résultat est sérialisable.

---
titre : Aperçu
description : Un aperçu de l'interface utilisateur de l'API AI.
---

# SDK UI d'IA

Le SDK UI d'IA est conçu pour vous aider à créer des applications de chat interactif, de complétion et d'assistant avec facilité. Il s'agit d'un **kit de outils indépendant des frameworks**, qui simplifie l'intégration de fonctionnalités d'IA avancées dans vos applications.

Le SDK UI d'IA fournit des abstractions robustes qui simplifient les tâches complexes de gestion des flux de chat et de mise à jour de l'interface utilisateur côté client, vous permettant de développer des interfaces dynamiques pilotées par l'IA plus efficacement. Avec quatre principaux crochets — **`useChat`**, **`useCompletion`**, **`useObject`**, et **`useAssistant`** — vous pouvez intégrer des capacités de chat en temps réel, des complétions de texte, des flux de JSON, et des fonctionnalités d'assistant interactif dans votre application.

- **[`useChat`](/docs/ai-sdk-ui/chatbot)** offre un flux de messages de chat en temps réel, en abstrayant la gestion d'état pour les entrées, les messages, la charge et les erreurs, permettant une intégration fluide dans n'importe quelle conception d'interface utilisateur.
- **[`useCompletion`](/docs/ai-sdk-ui/completion)** vous permet de gérer les complétions de texte dans vos applications, en gérant l'entrée de la prompt et en mettant automatiquement à jour l'interface utilisateur à mesure que de nouvelles complétions sont diffusées.
- **[`useObject`](/docs/ai-sdk-ui/object-generation)** est un crochet qui vous permet de consommer des objets JSON diffusés, fournissant un moyen simple de gérer et de afficher des données structurées dans votre application.
- **[`useAssistant`](/docs/ai-sdk-ui/openai-assistants)** est conçu pour faciliter l'interaction avec les API d'assistants compatibles avec OpenAI, en gérant l'état de l'interface utilisateur et en mettant automatiquement à jour à mesure que les réponses sont diffusées.

Ces crochets sont conçus pour réduire la complexité et le temps nécessaires pour mettre en œuvre les interactions d'IA, vous permettant de vous concentrer sur la création d'expériences utilisateur exceptionnelles.

## Support de Framework UI

La bibliothèque SDK UI prend en charge les frameworks suivants : [React](https://react.dev/), [Svelte](https://svelte.dev/), [Vue.js](https://vuejs.org/), et [SolidJS](https://www.solidjs.com/) (déprécié).
Voici une comparaison des fonctions prises en

| Fonction                                                  | React               | Svelte                               | Vue.js              | SolidJS (déprécié) |
| --------------------------------------------------------- | ------------------- | ------------------------------------ | ------------------- | -------------------- |
| [useChat](/docs/reference/ai-sdk-ui/use-chat)             | <Check size={18} /> | <Check size={18} /> Chat             | <Check size={18} /> | <Check size={18} />  |
| [useCompletion](/docs/reference/ai-sdk-ui/use-completion) | <Check size={18} /> | <Check size={18} /> Completion       | <Check size={18} /> | <Check size={18} />  |
| [useObject](/docs/reference/ai-sdk-ui/use-object)         | <Check size={18} /> | <Check size={18} /> StructuredObject | <Cross size={18} /> | <Check size={18} />  |
| [useAssistant](/docs/reference/ai-sdk-ui/use-assistant)   | <Check size={18} /> | <Cross size={18} />                  | <Check size={18} /> | <Check size={18} />  |

<Note>
  [Contributions](https://github.com/vercel/ai/blob/main/CONTRIBUTING.md) sont
  les bienvenues pour mettre en œuvre les fonctionnalités manquantes pour les frameworks non React.
</Note>

## Référence de l'API

Veuillez consulter la [Référence de l'API UI SDK AI](/docs/reference/ai-sdk-ui) pour plus de détails sur chaque fonction.

---
titre : Chatbot
description : Apprenez à utiliser la fonctionnalité useChat.
---

# Chatbot

La fonctionnalité useChat permet de créer facilement une interface utilisateur de conversation pour votre application de chatbot. Elle permet le streaming des messages de chat de votre fournisseur AI, gère l'état de la conversation et met à jour automatiquement l'interface utilisateur à mesure que de nouveaux messages arrivent.

Pour résumer, la fonctionnalité useChat fournit les fonctionnalités suivantes :

- **Streaming de messages** : Tous les messages du fournisseur AI sont streamés vers l'interface utilisateur de chat en temps réel.
- **États gérés** : La fonctionnalité gère les états pour l'entrée, les messages, le statut, les erreurs et plus encore pour vous.
- **Intégration fluide** : Intégrez facilement votre chat AI dans n'importe quel design ou disposition avec un minimum d'efforts.

Dans ce guide, vous apprendrez à utiliser la fonctionnalité useChat pour créer une application de chatbot avec un streaming de messages en temps réel.
Consultez notre [guide de chatbot avec outils](/docs/ai-sdk-ui/chatbot-with-tool-calling) pour apprendre à utiliser les outils dans votre chatbot.
Commencez par l'exemple suivant.

## Exemple

```tsx fichier='app/page.tsx'
'use client';

import { useChat } from '@ai-sdk/react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({});

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.role === 'user' ? 'Utilisateur : ' : 'IA : '}
          {message.parts ? message.parts.map(part => part.content).join('') : message.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input name="prompt" value={input} onChange={handleInputChange} />
        <button type="submit">Soumettre</button>
      </form>
    </>
  );
}
```

```ts fichier='app/api/chat/route.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

// Autorisez la diffusion de réponses jusqu'à 30 secondes
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4-turbo'),
    system: 'Vous êtes un assistant utile.',
    messages,
  });

  return result.toDataStreamResponse();
}
```

<Remarque>
  Les messages de l'interface utilisateur ont une nouvelle propriété `parts` qui contient les parties du message.
  Nous recommandons de rendre les messages en utilisant la propriété `parts` au lieu de la propriété `content`.
  La propriété `parts` prend en charge différents types de messages, notamment le texte, l'appel à l'outil et le résultat de l'outil, et permet des interfaces de chat plus flexibles et complexes.
</Remarque>

Dans le composant `Page`, la fonction d'hook `useChat` demandera à votre endpoint de fournisseur de IA chaque fois que l'utilisateur soumet un message.
Les messages sont ensuite transmis en temps réel et affichés dans l'interface de chat.

Cela permet une expérience de chat fluide où l'utilisateur peut voir la réponse de l'IA dès qu'elle est disponible,
sans avoir à attendre que la réponse entière soit reçue.

## Interface utilisateur personnalisé

`useChat` fournit également des moyens de gérer les états des messages de chat et de saisie via le code, d'afficher le statut et d'actualiser les messages sans être déclenchés par les interactions de l'utilisateur.

### État

La fonction `useChat` retourne un `status`. Il a les valeurs suivantes possibles :

- `soumis` : Le message a été envoyé à l'API et on attend le début de la flux de réponse.
- `flux` : La réponse est en cours de streaming depuis l'API, recevant des tronçons de données.
- `prêt` : La réponse complète a été reçue et traitée ; un nouveau message utilisateur peut être soumis.
- `erreur` : Une erreur est survenue lors de la requête API, empêchant la réussite de la mise en œuvre.

Vous pouvez utiliser `status` pour des fins telles que :

- Afficher un spinner de chargement pendant que le chatbot traite le message de l'utilisateur.
- Afficher un bouton "Arrêter" pour annuler le message en cours.
- Désactiver le bouton de soumission.

```tsx fichier='app/page.tsx' mise en surbrillance="6,20-27,34"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit, status, stop } =
    useChat({});

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.role === 'user' ? 'Utilisateur : ' : 'IA : '}
          {message.content}
        </div>
      ))}

      {(status === 'soumis' || status === 'flux') && (
        <div>
          {status === 'soumis' && <Spinner />}
          <button type="button" onClick={() => stop()}>
            Arrêter
          </button>
        </div>
      )}
```

```markdown
<form onSubmit={handleSubmit}>
        <input
          name="prompt"
          value={input}
          onChange={handleInputChange}
          disabled={status !== 'ready'}
        />
        <button type="submit">Soumettre</button>


### État d'Erreur

De même, l'état `error` reflète l'objet d'erreur lancé lors de la requête de récupération.
Il peut être utilisé pour afficher un message d'erreur, désactiver le bouton de soumission ou afficher un bouton de réessai :

<Note>
  Nous recommandons d'afficher un message d'erreur générique à l'utilisateur, tel que "Quelque chose s'est mal passé." C'est une bonne pratique pour éviter de révéler des informations provenant du serveur.
</Note>

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
          <div>Une erreur est survenue.</div>
          <button type="button" onClick={() => reload()}>
            Réessayer
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

Veuillez également consulter la [guide de gestion des erreurs](/docs/ai-sdk-ui/error-handling) pour plus d'informations.

### Modifier les messages

Parfois, vous pouvez vouloir modifier directement certains messages existants. Par exemple, un bouton de suppression peut être ajouté à chaque message pour permettre aux utilisateurs de les supprimer de l'historique de discussion.

La fonction `setMessages` peut vous aider à atteindre ces objectifs :

```tsx
const { messages, setMessages, ... } = useChat()

const handleDelete = (id) => {
  setMessages(messages.filter(message => message.id !== id))
}

return <>
  {messages.map(message => (
    <div key={message.id}>
      {message.role === 'user' ? 'Utilisateur : ' : 'IA : '}
      {message.content}
      <button onClick={() => handleDelete(message.id)}>Supprimer</button>
    </div>
  ))}
  ...
```

Vous pouvez penser à `messages` et `setMessages` comme une pair de `state` et `setState` dans React.

### Entrée contrôlée

Dans l'exemple initial, nous avons les appels de retour `handleSubmit` et `handleInputChange` qui gèrent les modifications de l'entrée et les soumissions de formulaire. Ces appels de retour sont utiles pour les cas d'utilisation courants, mais vous pouvez également utiliser des API non contrôlées pour des scénarios plus avancés tels que la validation de formulaire ou des composants personnalisés.

L'exemple suivant démontre comment utiliser des API plus détaillées comme `setInput` et `append` avec vos composants d'entrée et de bouton de soumission personnalisés :

```tsx
const { input, setInput, append } = useChat()

return <>
  <MonEntréePersonnalisée value={input} onChange={value => setInput(value)} />
  <MonBoutonDeSoumission onClick={() => {
    // Envoyer un nouveau message au fournisseur d'IA
    append({
      role: 'user',
      content: input,
    })
  }}/>
  ...
```

### Annulation et régénération

Il s'agit également d'un cas d'utilisation courant pour annuler le message de réponse tout en le faisant remonter en streaming à partir du fournisseur AI. Vous pouvez procéder à cela en appelant la fonction `stop` retournée par l'hook `useChat`.

```tsx
const { stop, status, ... } = useChat()

return <>
  <button onClick={stop} disabled={!(status === 'streaming' || status === 'submitted')}>Arrêter</button>
  ...
```

Lorsque l'utilisateur clique sur le bouton "Arrêter", la requête de fetch sera annulée. Cela évite la consommation de ressources inutiles et améliore l'UX de votre application de chatbot.

De même, vous pouvez également demander au fournisseur AI de retraiter le dernier message en appelant la fonction `reload` retournée par l'hook `useChat` :

```tsx
const { reload, status, ... } = useChat()

return <>
  <button onClick={reload} disabled={!(status === 'ready' || status === 'error')}>Régénérer</button>
  ...
</>
```

Lorsque l'utilisateur clique sur le bouton "Régénérer", le fournisseur AI régénérera le dernier message et le remplacera correspondamment.

### État de mise à jour de l'interface utilisateur

<Note>Cette fonctionnalité est actuellement uniquement disponible pour React.</Note>

Par défaut, l'hook `useChat` déclenchera une mise à jour de l'interface utilisateur à chaque fois qu'un nouveau morceau est reçu.
Vous pouvez mettre en cache les mises à jour de l'interface utilisateur avec l'option `experimental_throttle`.

```tsx filename="page.tsx" highlight="2-3"
const { messages, ... } = useChat({
  // Mettre en cache les messages et les mises à jour de données à 50ms :
  experimental_throttle: 50
})
```

## Appels de rappel d'événement

`useChat` fournit des appels de rappel d'événement optionnels que vous pouvez utiliser pour gérer différentes étapes du cycle de vie du chatbot :

- `onFinish` : Appelé lorsque le message de l'assistant est terminé
- `onError` : Appelé lorsque survenue d'une erreur pendant la requête de récupération.
- `onResponse` : Appelé lorsque la réponse de l'API est reçue.

Ces appels de rappel peuvent être utilisés pour déclencher des actions supplémentaires, telles que la journalisation, les analyses ou les mises à jour de l'interface utilisateur personnalisée.

```tsx
import { Message } from '@ai-sdk/react';

const {
  /* ... */
} = useChat({
  onFinish: (message, { usage, finishReason }) => {
    console.log('Message de streaming terminé :', message);
    console.log('Utilisation du jeton :', usage);
    console.log('Raison de terminaison :', finishReason);
  },
  onError: error => {
    console.error('Une erreur est survenue :', error);
  },
  onResponse: response => {
    console.log('Réponse HTTP reçue du serveur :', response);
  },
});
```

Il est important de noter que vous pouvez annuler le traitement en lançant une erreur dans le callback `onResponse`. Cela déclenchera le callback `onError` et arrêtera le message d'être ajouté à l'interface utilisateur de chat. Cela peut être utile pour gérer les réponses inattendues du fournisseur AI.

## Configuration de la requête

### En-têtes, corps et informations d'identification personnalisés

Par défaut, la fonctionnalité `useChat` envoie une requête HTTP POST vers l'endpoint `/api/chat` avec la liste des messages en tant que corps de la requête. Vous pouvez personnaliser la requête en passant des options supplémentaires à la fonctionnalité `useChat` :

```tsx
const { messages, input, handleInputChange, handleSubmit } = useChat({
  api: '/api/chat-personnalisee',
  en-têtes: {
    Authorization: 'votre_token',
  },
  corps: {
    id_utilisateur: '123',
  },
  informations_d_identification: 'same-origin',
});
```

Dans cet exemple, la fonctionnalité `useChat` envoie une requête POST vers l'endpoint `/api/chat-personnalisee` avec les en-têtes, les champs de corps supplémentaires et les informations d'identification pour cette requête de fetch. Sur votre serveur, vous pouvez gérer la requête avec ces informations supplémentaires.

### Définition de champs de corps personnalisés par requête

Vous pouvez configurer des champs de corps personnalisés par requête en utilisant l'option `body` de la fonction `handleSubmit`.
Cela est utile si vous souhaitez passer des informations supplémentaires à votre serveur qui ne font pas partie de la liste des messages.

```tsx filename="app/page.tsx" highlight="18-20"
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

Vous pouvez récupérer ces champs personnalisés sur votre serveur en déstructurant le corps de la requête :

```ts filename="app/api/chat/route.ts" highlight="3"
export async function POST(req: Request) {
  // Extraire les informations supplémentaires ("customKey") du corps de la requête :
  const { messages, customKey } = await req.json();
  //...
}
```

## Contrôle de la réponse en flux

Avec `streamText`, vous pouvez contrôler comment les messages d'erreur et les informations d'utilisation sont envoyés au client.

### Erreurs de Messages

Par défaut, le message d'erreur est masqué pour des raisons de sécurité.
Le message d'erreur par défaut est "Une erreur est survenue."
Vous pouvez transmettre les messages d'erreur ou envoyer votre propre message d'erreur en fournissant une fonction `getErrorMessage` :

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
        return 'erreur inconnue';
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

### Informations sur l'utilisation

Par défaut, les informations sur l'utilisation sont renvoyées au client. Vous pouvez les désactiver en définissant l'option `sendUsage` sur `false` :

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

### Flux de Texte

`useChat` peut gérer les flux de texte brut en définissant l'option `streamProtocol` sur `text` :

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

Cette configuration fonctionne également avec d'autres serveurs back-end qui envoient des flux de texte brut.
Consultez la [guide du protocole de flux](/docs/ai-sdk-ui/stream-protocol) pour plus d'informations.

<Note>
 Lorsque vous utilisez `streamProtocol: 'text'`, les appels d'outil, les informations d'utilisation et les raisons de fin de session ne sont pas disponibles.
</Note>

## Soumissions Vides

Vous pouvez configurer la fonction `useChat` pour autoriser les soumissions vides en définissant l'option `allowEmptySubmit` sur `true`.

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

## Raisonnement

Certains modèles comme DeepSeek `deepseek-reasoner`
et Anthropic `claude-3-7-sonnet-20250219` supportent les jetons de raisonnement.
Ces jetons sont généralement envoyés avant le contenu du message.
Vous pouvez les transmettre au client avec l'option `sendReasoning` :

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

Du côté client, vous pouvez accéder aux parties de raisonnement de l'objet message.

Ils ont une propriété `details` qui contient le raisonnement et les parties de raisonnement supprimées.
Vous pouvez également utiliser `reasoning` pour accéder uniquement au raisonnement sous forme de chaîne.

```tsx filename="app/page.tsx"
messages.map(message => (
  <div key={message.id}>
    {message.role === 'user' ? 'Utilisateur : ' : 'IA : '}
    {message.parts.map((part, index) => {
      // les parties de texte :
      if (part.type === 'text') {
        return <div key={index}>{part.text}</div>;
      }

// parties de raisonnement :
      if (part.type === 'raisonnement') {
        return (
          <pre key={index}>
            {part.details.map(detail =>
              detail.type === 'texte' ? detail.text : '<censuré>',
            )}
          </pre>
        );
      }
    })}
  </div>
));

## Sources

Certains fournisseurs comme [Perplexity](/providers/ai-sdk-providers/perplexity#sources) et
[Google Generative

# Sources
Les sources sont actuellement limitées aux pages web qui étayent la réponse. Vous pouvez les transmettre au client avec l'option `sendSources` :

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

Du côté client, vous pouvez accéder aux parties sources de l'objet message. Voici un exemple qui rend les sources sous forme de liens en bas du message :

```tsx
fichier="app/page.tsx"
messages.map(message => (
  <div key={message.id}>
    {message.role === 'user' ? 'Utilisateur : ' : 'IA : '}
    {message.parts
      .filtrer(part => part.type !== 'source')
      .map((part, index) => {
        si (part.type === 'text') {
          retourner <div key={index}>{part.text}</div>;
        }
      })}
    {message.parts
      .filtrer(part => part.type === 'source')
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

## Génération d'Images

Certains modèles, comme Google `gemini-2.0-flash-exp`, supportent la génération d'images.
Lorsque des images sont générées, elles sont exposées sous forme de fichiers au client.
Du côté du client, vous pouvez accéder aux parties de fichier de l'objet message
et les afficher sous forme d'images.

```tsx filename="app/page.tsx"
messages.map(message => (
  <div key={message.id}>
    {message.role === 'user' ? 'Utilisateur : ' : 'IA : '}
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

## Pièces Jointes (Expérimental)

La fonction `useChat` prend en charge l'envoi de pièces jointes en même temps qu'un message ainsi que leur affichage sur le client. Cela peut être utile pour construire des applications qui impliquent l'envoi d'images, de fichiers ou d'autres contenus multimédias vers le fournisseur IA.

Il existe deux façons d'envoyer des pièces jointes avec un message, soit en fournissant un objet `FileList` ou une liste d'URLs à la fonction `handleSubmit` :

### FileList

En utilisant `FileList`, vous pouvez envoyer plusieurs fichiers en tant que pièces jointes en même temps qu'un message en utilisant l'élément d'entrée de fichier. La fonction `useChat` convertira automatiquement les fichiers en URLs de données et les enverra au fournisseur IA.

<Note>
  Actuellement, uniquement les types de contenu `image/*` et `text/*` sont convertis automatiquement en [contenus multimodaux](/docs/foundations/prompts)

# Messages Multi-modales). Vous devrez gérer les autres types de contenu manuellement.
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

Note: I've translated the content as per your requirements, preserving the markdown formatting and code examples.

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
      experimental_attachments: fichiers

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
          placeholder="Envoyer un message..."
          onChange={handleInputChange}
          disabled={status !== 'ready'}
        />
      </form>
    </div>
  );

### URLS

Vous pouvez également envoyer des URL en tant qu'attachements avec un message. Cela peut être utile pour envoyer des liens vers des ressources externes ou du contenu multimédia.

> **Note :** L'URL peut également être une URL de données, qui est une chaîne base64 codée représentant le contenu d'un fichier. Actuellement, seuls les types de contenu `image/*` sont automatiquement convertis en [parties de contenu multimodal](/docs/foundations/prompts)

# Messages multimodales). Vous devrez gérer les autres types de contenu manuellement.

```tsx fichier="app/page.tsx"
'use client';

import { useChat } from '@ai-sdk/react';
import { useState } from 'react';
import { Attachment } from '@ai-sdk/ui-utils';

export default function Page() {
  const { messages, input, handleSubmit, handleInputChange, status } =
    useChat();

  const [attachments] = useState<Attachment[]>([
    {
      name: 'earth.png',
      contentType: 'image/png',
      url: 'https://example.com/earth.png',
    },
    {
      name: 'moon.png',
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

<div>
  {message.experimental_attachments
    ?.filtrer(attachment =>
      attachment.contentType?.startsWith('image/'),
    )
    .map((attachment, index) => (
      <img
        key={`${message.id}-${index}`}
        src={attachment.url}
        alt={attachment.name}
      />
   

```jsx
<form
  onSubmit={event => {
    handleSubmit(event, {
      attaques_expérimentales : attachments,
    });
  }}
>
  <input
    value={input}
    placeholder="Envoyez un message..."
    onChange={handleInputChange}
    disabled={status !== 'prêt'}
  />
</form>
</div>
</div>
```

---
titre : Persistance des messages de chatbot
description : Apprenez à stocker et à charger les messages de chat dans un chatbot.
---

# Persistance des Messages de Chat

La capacité de stocker et de charger les messages de chat est cruciale pour la plupart des chatbots AI.
Dans cette guide, nous allons montrer comment implémenter la persistance des messages avec `useChat` et `streamText`.

<Note>
  Cette guide ne couvre pas l'autorisation, la gestion des erreurs ou les autres considérations du monde réel.
  Il s'agit d'un exemple simple de comment implémenter la persistance des messages.
</Note>

## Lancement d'une nouvelle conversation

Lorsque l'utilisateur navigue vers la page de chat sans fournir d'ID de conversation,
nous devons créer une nouvelle conversation et rediriger vers la page de chat avec l'ID de la nouvelle conversation.

```tsx filename="app/chat/page.tsx"
import { redirect } from 'next/navigation';
import { createChat } from '@tools/chat-store';

export default async function Page() {
  const id = await createChat(); // créer une nouvelle conversation
  redirect(`/chat/${id}`); // rediriger vers la page de chat, voir ci-dessous
}
```

Notre exemple d'implémentation de magasin de conversation utilise des fichiers pour stocker les messages de conversation.
Dans une application réelle, vous utiliseriez une base de données ou un service de stockage cloud,
et obtiendriez l'ID de la conversation de la base de données.
Cela dit, les interfaces de fonction sont conçues pour être facilement remplacées par d'autres implémentations.

```tsx filename="tools/chat-store.ts"
import { generateId } from 'ai';
import { existsSync, mkdirSync } from 'fs';
import { writeFile } from 'fs/promises';
import path from 'path';

export async function createChat(): Promise<string> {
  const id = generateId(); // générer un ID de conversation unique
  await writeFile(getChatFile(id), '[]'); // créer un fichier de conversation vide
  return id;
}

function getChatFile(id: string): string {
  const chatDir = path.join(process.cwd(), '.chats');
  if (!existsSync(chatDir)) mkdirSync(chatDir, { recursive: true });
  return path.join(chatDir, `${id}.json`);
}
```

## Chargement d'une conversation existante

Lorsque l'utilisateur navigue vers la page de conversation avec un ID de conversation, nous devons charger les messages de la conversation et les afficher.

```tsx filename="app/chat/[id]/page.tsx"
import { loadChat } from '@tools/chat-store';
import Chat from '@ui/chat';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const { id } = await props.params; // récupérer l'ID de la conversation à partir de l'URL
  const messages = await loadChat(id); // charger les messages de la conversation
  return <Chat id={id} initialMessages={messages} />; // afficher la conversation
}
```

La fonction `loadChat` dans notre magasin de conversations fichier est implémentée comme suit :

```tsx filename="tools/chat-store.ts"
import { Message } from 'ai';
import { readFile } from 'fs/promises';

export async function loadChat(id: string): Promise<Message[]> {
  return JSON.parse(await readFile(getChatFile(id), 'utf8'));
}

// ... reste du fichier
```

Le composant de visualisation est un composant de conversation simple qui utilise la fonction `useChat` pour envoyer et recevoir des messages :

```tsx filename="ui/chat.tsx" highlight="10-12"
'use client';

import { Message, useChat } from '@ai-sdk/react';

export default function Chat({
  id,
  initialMessages,
}: { id?: string | undefined; initialMessages?: Message[] } = {}) {
  const { input, handleInputChange, handleSubmit, messages } = useChat({
    id, // utiliser l'ID de conversation fourni
    initialMessages, // messages initiaux si fournis
    sendExtraMessageFields: true, // envoyer id et createdAt pour chaque message
  });
```

// Code de rendu simplifié, étendre à votre besoin :
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role === 'user' ? 'Utilisateur : ' : 'IA : '}
          {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}

## Stockage des messages

`useChat` envoie l'identifiant de la conversation et les messages vers le backend.
Nous avons activé l'option `sendExtraMessageFields` pour envoyer les champs `id` et `createdAt`,
ce qui signifie que nous stockons les messages dans le format de message `useChat`.

<Remarque>
  Le format de message `useChat` est différent du format `CoreMessage`. Le
  format de message `useChat` est conçu pour la mise en page frontend, et contient
  des champs supplémentaires comme `id` et `createdAt`. Nous recommandons de stocker
  les messages dans le format de message `useChat`.
</Remarque>

Le stockage des messages est effectué dans la fonction de rappel `onFinish` de la fonction `streamText`.
`onFinish` reçoit les messages de la réponse de l'IA sous forme de `CoreMessage[]`,
et nous utilisons l'assistant [`appendResponseMessages`](/docs/reference/ai-sdk-ui/append-response-messages)
pour ajouter les messages de la réponse de l'IA aux messages de la conversation.

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

Le stockage réel des messages est effectué dans la fonction `saveChat`, qui dans
notre magasin de conversation fichier est implémenté comme suit :

```tsx
fichier="tools/chat-store.ts"
import { Message } from 'ai';
import { writeFile } from 'fs/promises';

export async function sauvegarderChat({
  id,
  messages,
}: {
  id: string;
  messages: Message[];
}): Promise<void> {
  const contenu = JSON.stringify(messages, null, 2);
  await writeFile(getChatFile(id), contenu);
}

// ... reste du fichier
```

## Identifiants de Message

En plus d'un identifiant de chat, chaque message possède un identifiant.
Vous pouvez utiliser cet identifiant de message pour manipuler des messages individuels.

Les identifiants pour les messages des utilisateurs sont générés par l'appel `useChat` sur le client,
et les identifiants pour les messages de réponse AI sont générés par `streamText`.

Vous pouvez contrôler la forme de l'identifiant en fournissant des générateurs d'identifiants
(voir [`createIdGenerator()`](/docs/reference/ai-sdk-core/create-id-generator) :

```tsx filename="ui/chat.tsx" highlight="8-12"
import { createIdGenerator } from 'ai';
import { useChat } from '@ai-sdk/react';

const {
  // ...
} = useChat({
  // ...
  // format de l'identifiant pour les messages côté client :
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
    // format de l'identifiant pour les messages côté serveur :
    experimental_generateMessageId: createIdGenerator({
      prefix: 'msgs',
      size: 16,
    }),
  });
  // ...
}
```

## Envoyer uniquement le dernier message

Une fois que vous avez implémenté la persistance des messages, vous pourriez vouloir envoyer uniquement le dernier message au serveur.
Cela réduit la quantité de données envoyées au serveur à chaque requête et peut améliorer les performances.

Pour atteindre cela, vous pouvez fournir une fonction `experimental_prepareRequestBody` à l'hook `useChat` (React uniquement).
Cette fonction reçoit les messages et l'ID de la conversation, et retourne le corps de la requête à envoyer au serveur.

```tsx filename="ui/chat.tsx" highlight="7-10"
import { useChat } from '@ai-sdk/react';

const {
  // ...
} = useChat({
  // ...
  // n'envoyer que le dernier message au serveur :
  experimental_prepareRequestBody({ messages, id }) {
    return { message: messages[messages.length - 1], id };
  },
});
```

Sur le serveur, vous pouvez alors charger les messages précédents et les ajouter au message nouveau :

```tsx filename="app/api/chat/route.ts" highlight="2-9"
import { appendClientMessage } from 'ai';

export async function POST(req: Request) {
  // récupérer le dernier message du client :
  const { message, id } = await req.json();

  // charger les messages précédents du serveur :
  const previousMessages = await loadChat(id);

  // ajouter le nouveau message aux messages précédents :
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

## Gérer les déconnexions du client

Par défaut, la fonction `streamText` de l'API SDK utilise un retour d'arrosage vers le fournisseur de modèle de langage pour empêcher
la consommation de jetons qui n'ont pas encore été demandés.

Cependant, cela signifie que lorsque le client se déconnecte, par exemple en fermant la fenêtre du navigateur ou en raison d'un problème de réseau,
la flotte du LLM sera interrompue et la conversation peut se retrouver dans un état brisé.

En supposant que vous avez une [solution de stockage](

# Stockage des messages

Si vous souhaitez conserver les messages en place, vous pouvez utiliser la méthode `consumeStream` pour consommer le flux sur le serveur, puis enregistrer le résultat de manière habituelle.

`consumeStream` supprime effectivement la pression arrière, ce qui signifie que le résultat est stocké même lorsque le client a déjà été déconnecté.

```tsx fichier="app/api/chat/route.ts" mise en surbrillance="21-23"
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

  // consommer le flux pour s'assurer qu'il s'exécute à la fin et déclenche onFinish
  // même lorsque la réponse du client est annulée :
  result.consumeStream(); // sans await

  return result.toDataStreamResponse();
}
```

Lorsque le client recharge la page après une déconnexion, le chat sera restauré à partir de la solution de stockage.

<Remarque>
  Dans les applications de production, vous suivrez également l'état de la demande (en cours, terminé) dans vos messages stockés et l'utiliserez sur le client pour couvrir le cas où le client recharge la page après une déconnexion, mais le streaming n'est pas encore terminé.
</Remarque>

## Résumation des flux en cours

<Note>Cette fonctionnalité est expérimentale et peut changer dans les futures versions.</Note>

La fonction `useChat` a un support expérimental pour la résumation d'un flux de génération de chat en cours par n'importe quel client, soit après une déconnexion réseau, soit en rechargeant la page de chat. Cela peut être utile pour la construction d'applications impliquant des conversations de longue durée ou pour s'assurer que les messages ne soient pas perdus en cas de défaillances réseau.

Les pré-requis suivants sont nécessaires pour que votre application de chat supporte les flux résumables :

- L'installation du package `resumable-stream` <https://www.npmjs.com/package/resumable-stream> qui aide à créer et à gérer le mécanisme de publication/abonnement des flux.
- La création d'une instance de [Redis](https://vercel.com/marketplace/redis) pour stocker l'état du flux.
- La création d'une table qui suit les identifiants de flux associés à un chat.

Pour résumer un flux de chat, vous utiliserez la fonction `experimental_resume` retournée par la fonction `useChat`. Vous appelez cette fonction lors de la montée initiale de la fonction principale du composant de chat.

```tsx filename="app/components/chat.tsx"
'use client';

import { useChat } from '@ai-sdk/react';
import { Input } from '@/components/input';
import { Messages } from '@/components/messages';

export function Chat() {
  const { experimental_resume } = useChat({ id });

  useEffect(() => {
    experimental_resume();

    // nous utilisons un tableau vide de dépendances pour
    // nous assurer que cet effet s'exécute seulement une fois
  }, []);

  return (
    <div>
      <Messages />
      <Input />
    </div>
  );
}
```

Pour une mise en œuvre plus résiliente qui gère les conditions de course qui peuvent survenir pendant une demande de résumation, vous pouvez utiliser la fonction `useAutoResume` suivante. Cela traitera automatiquement les données SSE `append-message` transmises par le serveur.

```tsx filename="app/hooks/use-auto-resume.ts"
'use client';

```javascript
import { useEffect } from 'react';
import type { UIMessage } from 'ai';
import type { UseChatHelpers } from '@ai-sdk/react';

export type DataPart = { type: 'append-message'; message: string };

export interface Props {
  autoResume: boolean;
  initialMessages: UIMessage[];
  experimental_resume: UseChatHelpers['experimental_resume'];
  data: UseChatHelpers['data'];
  setMessages: UseChatHelpers['setMessages'];
}

export function useAutoResume({
  autoResume,
  initialMessages,
  experimental_resume,
  data,
  setMessages,
}: Props) {
  useEffect(() => {
    if (!autoResume) return;

    const dernierMessage = initialMessages.at(-1);

    if (dernierMessage?.role === 'user') {
      experimental_resume();
    }

    // nous exécutons cela intentionnellement une seule fois
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!data || data.length === 0) return;

    const partieDeDonnees = data[0] as DataPart;

    if (partieDeDonnees.type === 'append-message') {
      const message = JSON.parse(partieDeDonnees.message) as UIMessage;
      setMessages([...initialMessages, message]);
    }
  }, [data, initialMessages, setMessages]);
}
```

Vous pouvez ensuite utiliser cet hook dans votre composant de chat comme suit.

```tsx fichier="app/components/chat.tsx"
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

La fonction `experimental_resume` effectue une requête `GET` vers votre point de terminaison de chat configuré (ou `/api/chat` par défaut) chaque fois que votre client l'appelle. Si il existe un flux actif, il reprend là où il s'est arrêté, sinon il se termine sans erreur.

La requête `GET` ajoute automatiquement le paramètre de requête `chatId` à l'URL pour aider à identifier le chat à qui la requête appartient. En utilisant l'ID de chat, vous pouvez rechercher l'ID du flux le plus récent dans la base de données et reprendre le flux.

```bash
GET /api/chat?chatId=<votre-id-de-chat>
```

Il est nécessaire d'avoir mis en place auparavant le gestionnaire `POST` pour la route `/api/chat` pour créer de nouvelles générations de chat. Lorsque vous utilisez `experimental_resume`, il faut également mettre en place le gestionnaire `GET` pour la route `/api/chat` pour reprendre les flux.

### 1. Implémenter le gestionnaire GET

Ajoutez une méthode `GET` à `/api/chat` qui :

1. Lit `chatId` à partir de la chaîne de requête
2. La valide pour s'assurer qu'elle est présente
3. Charge les IDs de flux stockés pour ce chat
4. Retourne le dernier flux à `streamContext.resumableStream()`
5. Recourt à un flux vide si celui-ci est déjà fermé

```ts fichier="app/api/chat/route.ts"
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
    return new Response('l\'id est requis', { status: 400 });
  }

  const streamIds = await loadStreams(chatId);

  if (!streamIds.length) {
    return new Response('Aucun flux trouvé', { status: 404 });
  }

  const recentStreamId = streamIds.at(-1);

  if (!recentStreamId) {
    return new Response('Aucun flux récent trouvé', { status: 404 });
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
   * Lorsque la génération est "active" pendant SSR mais que le flux
   * resumable a conclu après avoir atteint ce point.
   */

  const messages = await getMessagesByChatId({ id: chatId });
  const mostRecentMessage = messages.at(-1);
```

Si (!mostRecentMessage || mostRecentMessage.role !== 'assistant') {
    return new Response(emptyDataStream, { status: 200 });
  }

  const messageCreatedAt = new Date(mostRecentMessage.createdAt);

  const streamWithMessage = createDataStream({
    execute: buffer => {
      buffer.writeData({
        type: 'append-message',
        message: JSON.stringify(mostRecentMessage),
      });
    },
  });

  return new Response(streamWithMessage, { status: 200 });
}

---

Après avoir implémenté le gestionnaire `GET`, vous pouvez mettre à jour le gestionnaire `POST` pour gérer la création de flux résumables.

### 2. Mettre à jour le gestionnaire de requête POST

Lorsque vous créez un nouveau chat de complétion, vous devez :

1. Générer un `streamId` frais
2. Le persister aux côtés de votre `chatId`
3. Lancer un `createDataStream` qui envoie des jetons à mesure qu'ils arrivent
4. Donner ce nouveau flux à `streamContext.resumableStream()`

```ts fichier="app/api/chat/route.ts"
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
  const { id, messages } = await req.json();
  const streamId = generateId();

  // Enregistrer ce nouveau flux pour pouvoir le reprendre plus tard
  await appendStreamId({ chatId: id, streamId });

  // Construire le flux de données qui émettra des jetons
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

      // Retourner un flux résumable au client
      result.mergeIntoDataStream(dataStream);
    },
  });
```

```javascript
return new Response(
    await streamContext.resumableStream(streamId, () => stream),
);
```

---

### Utilisation de l'outil de chatbot

#### Description
Apprenez à utiliser les outils avec la fonctionnalité `useChat`.

# Utilisation de l'outil de chatbot

Avec [`useChat`](/docs/reference/ai-sdk-ui/use-chat) et [`streamText`](/docs/reference/ai-sdk-core/stream-text), vous pouvez utiliser des outils dans votre application de chatbot.
Le SDK IA prend en charge trois types d'outils dans ce contexte :

1. Outils exécutés automatiquement côté serveur
2. Outils exécutés automatiquement côté client
3. Outils nécessitant une interaction utilisateur, comme les dialogues de confirmation

Le flux est le suivant :

1. L'utilisateur entre un message dans l'interface de chat.
1. Le message est envoyé à la route API.
1. Dans votre route côté serveur, le modèle de langage génère des appels d'outil pendant l'appel `streamText`.
1. Tous les appels d'outil sont redirigés vers le client.
1. Les outils côté serveur sont exécutés en utilisant leur méthode `execute` et leurs résultats sont redirigés vers le client.
1. Les outils côté client qui doivent être exécutés automatiquement sont gérés avec la callback `onToolCall`.
   Vous pouvez retourner le résultat de l'outil à partir de la callback.
1. Les outils côté client qui nécessitent des interactions utilisateur peuvent être affichés dans l'interface.
   Les appels d'outil et les résultats sont disponibles en tant que parties d'invocation d'outil dans la propriété `parts` du dernier message de l'assistant.
1. Lorsque l'interaction utilisateur est terminée, `addToolResult` peut être utilisé pour ajouter le résultat de l'outil à la conversation.
1. Lorsqu'il y a des appels d'outil dans le dernier message de l'assistant et que tous les résultats d'outil sont disponibles, le client envoie les messages mis à jour vers le serveur.
   Cela déclenche une autre itération de ce flux.

Les appels d'outil et les exécutions d'outil sont intégrés dans le message de l'assistant en tant que parties d'invocation d'outil.
Une invocation d'outil est à l'origine un appel d'outil, puis elle devient un résultat d'outil lorsqu'il est exécuté.
Le résultat de l'outil contient toutes les informations sur l'appel d'outil ainsi que le résultat de l'exécution de l'outil.

<Note>
  Pour envoyer automatiquement une autre requête vers le serveur lorsque tous les appels d'outil sont côté serveur, vous devez définir
  [`maxSteps`](/docs/reference/ai-sdk-ui/use-chat#max-steps) sur une valeur supérieure à 1 dans les options `useChat`.
  Cela est désactivé par défaut pour la compatibilité avec les versions précédentes.
</Note>

## Exemple

Dans cet exemple, nous utilisons trois outils :

- `getWeatherInformation`: Un outil côté serveur exécuté automatiquement qui renvoie le temps dans une ville donnée.
- `askForConfirmation`: Un outil client côté utilisateur qui demande à l'utilisateur confirmation.
- `getLocation`: Un outil client côté utilisateur exécuté automatiquement qui renvoie une ville aléatoire.

### Route API

```tsx filename='app/api/chat/route.ts'
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { z } from 'zod';

// Autorisez les réponses en streaming jusqu'à 30 secondes
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();
```

```javascript
const result = streamText({
  model: openai('gpt-4o'),
  messages,
  outils : {
    // Outil serveur avec fonction d'exécution :
    getWeatherInformation : {
      description : 'afficher le temps dans une ville donnée à l\'utilisateur',
      paramètres : z.object({ ville : z.string() }),
      execute : async ({}: { ville : string }) => {
        const optionsMétéo = ['ensoleillé', 'nuageux', 'pluvieux', 'neigeux', 'ventux'];
        return optionsMétéo[
          Math.floor(Math.random() * optionsMétéo.length)
        ];
      },
    },
    // Outil client qui déclenche l\'interaction avec l\'utilisateur :
    demanderConfirmation : {
      description : 'Demander à l\'utilisateur la confirmation.',
      paramètres : z.object({
        message : z.string().describe('Le message à demander à l\'utilisateur pour confirmation.'),
      }),
    },
    // Outil client qui est exécuté automatiquement sur le client :
    obtenirLocalisation : {
      description :
        'Obtenir la localisation de l\'utilisateur. Demandez toujours la confirmation avant d\'utiliser cet outil.',
      paramètres : z.object({}),
    },
  },
});

  return result.toDataStreamResponse();
}
```

### Page client

La page client utilise l'hook `useChat` pour créer une application de chatbot avec un flux de messages en temps réel.
Les invocations de l'outil sont affichées dans l'interface de chat sous forme de parties d'invocation d'outil.
Veuillez vous assurer de rendre les messages en utilisant la propriété `parts` du message.

Il y a trois choses à noter :

1.  Le callback [`onToolCall`](/docs/reference/ai-sdk-ui/use-chat#on-tool-call) est utilisé pour gérer les outils côté client qui devraient être exécutés automatiquement.
    Dans cet exemple, l'outil `getLocation` est un outil côté client qui renvoie une ville aléatoire.

2.  La propriété `toolInvocations` du dernier message de l'assistant contient toutes les appels d'outil et les résultats.
    L'outil côté client `askForConfirmation` est affiché dans l'interface de chat.
    Il demande à l'utilisateur confirmation et affiche le résultat une fois que l'utilisateur confirme ou refuse l'exécution.
    Le résultat est ajouté à la conversation en utilisant `addToolResult`.

3.  Le paramètre [`maxSteps`](/docs/reference/ai-sdk-ui/use-chat#max-steps) est utilisé pour définir le nombre maximum de pas autorisés dans la conversation.

# option max-steps est définie sur 5.
   Cela permet plusieurs itérations d'utilisation d'outils entre le client et le serveur.

```tsx fichier='app/page.tsx' mise-en-surbrillance="9,12,31"
'use client';

import { ToolInvocation } from 'ai';
import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, addToolResult } =
    useChat({
      maxSteps: 5,

      // exécuter les outils côté client qui sont automatiquement exécutés :
      async onToolCall({ toolCall }) {
        if (toolCall.toolName === 'getLocation') {
          const cities = [
            'New York',
            'Los Angeles',
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
              // afficher les parties de texte sous forme de texte simple :
              case 'text':
                return part.text;
```

// pour les invocations de l'outil, distinguer entre les outils et l'état :
              case 'tool-invocation': {
                const callId = part.toolInvocation.toolCallId;

switch (part.toolInvocation.toolName) {
  case 'demandezConfirmation': {
    switch (part.toolInvocation.etat) {
      case 'appel':
        return (
          <div key={callId}>
            {part.toolInvocation.args.message}
            <div>
              <button
                onClick={() =>
                  addToolResult({
                    toolCallId: callId,
                    result: 'Oui,

>
                                Oui
                              </button>
                              <button
                                onClick={() =>
                                  addToolResult({
                                    toolCallId: callId,
                                    result: 'Non, refusé',
                                  })
                                }
                              >
                                Non
                              </button>
                           

</div>
                        );
                      case 'result':
                        return (
                          <div key={callId}>
                            L'accès à la localisation est autorisé :{' '}
                            {part.toolInvocation.result}
                          </div>
                        );
                    }
                    break;

cas 'getLocation' : {
                    switch (part.toolInvocation.etat) {
                      cas 'appel' :
                        retour <div key={callId}>Récupération de la localisation...</div>;
                      cas 'résultat' :
                        retour (
                          <div key={callId}>
                            Localisation : {part.toolInvocation.resultat}
                         

cas 'getWeatherInformation' : {
  switch (part.toolInvocation.etat) {
    // exemple de pré-charge de requêtes de l'outil en streaming :
    cas 'partial-call' :
      return (
        <pre key={callId}>
          {JSON.stringify(part.toolInvocation, null, 2)}
        </pre>
      );
    cas 'call' :
      return (
        <div key={callId}>
          Récupération de l'information météorologique pour{' '}
          {part.toolInvocation.args.ville

cas 'result' :
  return (
    <div key={callId}>
      Le temps à {part.toolInvocation.args.city} : {' '}
      {part.toolInvocation.result}
    </div>
  );
}
break;
}
}
}
}
</div>
</div>
      ))}

<form onSubmit={handleSubmit}>
        <input valeur={input} onChange={handleInputChange} />
      </form>
    </>
  );

## Streaming d'appel d'outil

Vous pouvez diffuser les appels d'outil en temps réel pendant leur génération en activant l'option `toolCallStreaming` dans `streamText`.

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

Lorsque la bande-annonce est activée, les appels d'outil partiels seront diffusés en tant que partie du flux de données.
Ils sont disponibles à travers l'hook `useChat`.
Les parties d'appel d'outil de messages d'invocation de l'assistant seront également contenir des appels d'outil partiels.
Vous pouvez utiliser la propriété `state` de l'invocation d'outil pour afficher l'interface utilisateur correcte.

```tsx filename='app/page.tsx' highlight="9,10"
export default function Chat() {
  // ...
  return (
    <>
      {messages?.map(message => (
        <div key={message.id}>
          {message.parts.map(part => {
            if (part.type === 'tool-invocation') {
              switch (part.toolInvocation.etat) {
                case 'partial-call':
                  return <>rendre appel de l'outil partiel</>;
                case 'call':
                  return <>rendre appel de l'outil complet</>;
                case 'result':
                  return <>rendre le résultat de l'outil</>;
              }
            }
          })}
        </div>
      ))}
    </>
  );
}
```

## Étape de début des parties

Lorsque vous utilisez des appels de outils multi-étapes, le SDK AI ajoutera des parties de début d'étape aux messages de l'assistant.
Si vous souhaitez afficher des limites entre les invocations d'outil, vous pouvez utiliser les parties `step-start` comme suit :

```tsx fichier='app/page.tsx'
// ...
// où vous affichez les parties du message :
message.parts.map((part, index) => {
  switch (part.type) {
    case 'step-start':
      // afficher les limites d'étape sous forme de lignes horizontales :
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

## Appels Multi-Étapes du Serveur

Vous pouvez également utiliser les appels multi-étapes du côté serveur avec `streamText`.
Cela fonctionne lorsque tous les outils invoqués ont une fonction `execute` du côté serveur.

```tsx filename='app/api/chat/route.ts' highlight="15-21,24"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
      getWeatherInformation: {
        description: 'affiche le temps dans une ville donnée à l\'utilisateur',
        parameters: z.object({ city: z.string() }),
        // l\'outil a une fonction execute :
        execute: async ({}: { city: string }) => {
          const weatherOptions = ['sunny', 'cloudy', 'rainy', 'snowy', 'windy'];
          return weatherOptions[
            Math.floor(Math.random() * weatherOptions.length)
          ];
        },
      },
    },
    maxSteps: 5,
  });

  return result.toDataStreamResponse();
}
```

## Erreurs

Les modèles de langage peuvent faire des erreurs lorsqu'ils appellent des outils.
Par défaut, ces erreurs sont masquées pour des raisons de sécurité et apparaissent sous la forme "Une erreur est survenue" dans l'interface utilisateur.

Pour afficher les erreurs, vous pouvez utiliser la fonction `getErrorMessage` lors de l'appel de `toDataStreamResponse`.

```tsx
export function errorHandler(error: unknown) {
  if (error == null) {
    return 'erreur inconnue';
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

Dans le cas où vous utilisez `createDataStreamResponse`, vous pouvez utiliser la fonction `onError` lors de l'appel de `toDataStreamResponse` :

```tsx
const response = createDataStreamResponse({
  // ...
  async execute(dataStream) {
    // ...
  },
  onError: error => `Erreur personnalisée : ${error.message}`,
});
```

---
titre : Interfaces utilisateur génératives
description : Apprenez à construire les UI génératives avec l'API SDK UI.
---

# Interfaces Utilitaires Génératives

Les interfaces utilisateurs génératives (IU génératives) sont le processus qui permet à un grand modèle de langage (MLL) de dépasser le texte et de "générer des IU". Cela crée une expérience plus engageante et native à l'IA pour les utilisateurs.

<WeatherSearch />

Au cœur des IU génératives se trouvent [ les outils ](/docs/ai-sdk-core/tools-and-tool-calling), qui sont des fonctions que vous fournissez au modèle pour effectuer des tâches spécialisées comme obtenir le temps météo dans une localité. Le modèle peut décider quand et comment utiliser ces outils en fonction du contexte de la conversation.

Les IU génératives sont le processus de connecter les résultats d'un appel à outil à un composant React. Voici comment ça marche :

1. Vous fournissez au modèle un prompt ou une histoire de conversation, ainsi qu'un ensemble d'outils.
2. Sur la base du contexte, le modèle peut décider d'appeler un outil.
3. Si un outil est appelé, il exécutera et renverra des données.
4. Ces données peuvent ensuite être transmises à un composant React pour la rendu.

En transmettant les résultats des outils aux composants React, vous pouvez créer une expérience IU générative plus engageante et adaptative à vos besoins.

## Construire une Interface de Chat IU Générative

Créons une interface de chat qui gère les conversations basées sur le texte et incorpore des éléments UI dynamiques en fonction des réponses du modèle.

### Implémentation de base du chat

Commencez par une implémentation de base du chat en utilisant la fonction `useChat` :

```tsx filename="app/page.tsx"
'use client';

import { useChat } from '@ai-sdk/react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          <div>{message.role === 'user' ? 'Utilisateur : ' : 'IA : '}</div>
          <div>{message.content}</div>
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Tapez un message..."
        />
        <button type="submit">Envoyer</button>
      </form>
    </div>
  );
}
```

Pour gérer les requêtes de chat et les réponses du modèle, configurez une route API :

```ts filename="app/api/chat/route.ts"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(request: Request) {
  const { messages } = await request.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system: 'Vous êtes un assistant amical !',
    messages,
    maxSteps: 5,
  });

  return result.toDataStreamResponse();
}
```

Cette route API utilise la fonction `streamText` pour traiter les messages de chat et diffuser les réponses du modèle vers le client.

### Créer un Outil

Avant d'améliorer votre interface de chat avec des éléments UI dynamiques, vous devez créer un outil et le composant React correspondant. Un outil permettra au modèle d'exécuter une action spécifique, comme la récupération d'informations météorologiques.

Créez un nouveau fichier appelé `ai/tools.ts` avec le contenu suivant :

```ts filename="ai/tools.ts"
import { tool as createTool } from 'ai';
import { z } from 'zod';

export const weatherTool = createTool({
  description: 'Affiche le temps pour une localité',
  parameters: z.object({
    location: z.string().describe('La localité pour laquelle récupérer le temps'),
  }),
  execute: async function ({ location }) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    return { weather: 'Ensoleillé', temperature: 75, location };
  },
});

export const tools = {
  afficherLeTemps: weatherTool,
};
```

Dans ce fichier, vous avez créé un outil appelé `weatherTool`. Cet outil simule la récupération d'informations météorologiques pour une localité donnée. Cet outil retournera des données simulées après un délai de 2 secondes. Dans une application réelle, vous remplaceriez cette simulation par une appel réel à une API météorologique.

### Mettre à jour la Route API

Mettez à jour la route API pour inclure l'outil que vous avez défini :

```ts filename="app/api/chat/route.ts" highlight="3,13"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { tools } from '@/ai/tools';

export async function POST(request: Request) {
  const { messages } = await request.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system: 'Vous êtes un assistant amical !',
    messages,
    maxSteps: 5,
    tools,
  });

  return result.toDataStreamResponse();
}
```

Maintenant que vous avez défini l'outil et l'avez ajouté à votre appel `streamText`, passons à la création d'un composant React pour afficher les informations météorologiques qu'il retourne.

### Créer des composants UI

Créez un nouveau fichier appelé `components/weather.tsx` :

```tsx filename="components/weather.tsx"
type WeatherProps = {
  temperature: number;
  weather: string;
  location: string;
};

export const Weather = ({ temperature, weather, location }: WeatherProps) => {
  return (
    <div>
      <h2>Conditions météorologiques actuelles pour {location}</h2>
      <p>État météorologique : {weather}</p>
      <p>Température : {temperature}°C</p>
    </div>
  );
};
```

Ce composant affichera les informations météorologiques pour une localisation donnée. Il prend trois props : `temperature`, `weather` et `location` (exactement ce que `weatherTool` retourne).

### Afficher le composant météo

Maintenant que vous avez votre outil et le composant React correspondant, intégrons-les dans votre interface de chat. Vous afficherez le composant météo lorsque le modèle appelle l'outil météo.

Pour vérifier si le modèle a appelé un outil, vous pouvez utiliser la propriété `toolInvocations` de l'objet message. Cette propriété contient des informations sur les outils appelés lors de cette génération, notamment `toolCallId`, `toolName`, `args`, `toolState` et `result`.

Mettez à jour votre fichier `page.tsx` :

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
          <div>{message.role === 'user' ? 'Utilisateur : ' : 'IA : '}</div>
          <div>{message.content}</div>

          <div>
            {message.toolInvocations?.map(toolInvocation => {
              const { toolName, toolCallId, state } = toolInvocation;
```

Si (l'état est égal à 'result') {
            Si (le nom de l'outil est égal à 'displayWeather') {
              const { result } = l'appel de l'outil ;
              return (
                <div clé={l'ID de l'appel de l'outil}>
                  <Météo { ...result } />
                </div>
              ) ;
            }
          } else {
            return (
              <div clé={l'ID de l'appel de l'outil}>
                {le nom de l'outil est égal à 'displayWeather' ? (
                  <div>Chargement de la météo...</div>
                ) : null}
              </div

<form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type un message..."
        />
        <button type="submit">Envoyer</button>
      </form>
    </div>
  );
}
```

Dans ce code mis à jour, vous :

1. Vérifiez si le message contient `toolInvocations`.
2. Vérifiez si l'état d'appel de l'outil est 'result'.
3. Si c'est un résultat et que le nom de l'outil est 'displayWeather', affichez le composant Weather.
4. Si l'état d'appel de l'outil n'est pas 'result', affichez un message de chargement.

Cette approche vous permet de rendre dynamiquement des composants UI en fonction des réponses du modèle, créant une expérience de chat plus interactive et plus consciente du contexte.

## Élargir votre Application de UI Générative

Vous pouvez améliorer votre application de chat en ajoutant davantage d'outils et de composants, créant ainsi une expérience utilisateur plus riche et plus polyvalente. Voici comment vous pouvez élargir votre application :

## Adding a New Component

To add a new component, you can create a new class that extends the `Component` class. The `Component` class is the base class for all

### Ajouter Plus d'Outils

Pour ajouter plus d'outils, il suffit de les définir dans votre fichier `ai/tools.ts` :

```ts
// Ajouter un nouvel outil de bourse
export const stockTool = createTool({
  description: 'Obtenir le prix d'une action',
  parameters: z.object({
    symbol: z.string().describe('Le symbole de l\'action pour obtenir le prix'),
  }),
  execute: async function ({ symbol }) {
    // Appel simulé de l\'API
    await new Promise(resolve => setTimeout(resolve, 2000));
    return { symbol, price: 100 };
  },
});

// Mettre à jour l\'objet d\'outils
export const tools = {
  afficherMétéo: weatherTool,
  getPrixAction: stockTool,
};
```

Créez ensuite un nouveau fichier appelé `components/stock.tsx` :

```tsx
type StockProps = {
  price: number;
  symbol: string;
};

export const Stock = ({ price, symbol }: StockProps) => {
  return (
    <div>
      <h2>Informations sur l\'action</h2>
      <p>Symbol : {symbol}</p>
      <p>Prix : ${price}</p>
    </div>
  );
};
```

Enfin, mettez à jour votre fichier `page.tsx` pour inclure le nouveau composant Stock :

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
              const { nomDeLoutil, toolCallId, etat } = toolInvocation;

Si (l'état est égal à 'result') {
                Si (toolName est égal à 'displayWeather') {
                  const { result } = toolInvocation;
                  return (
                    <div key={toolCallId}>
                      <Weather {...result} />
                    </div>
                  );
                } else if (toolName est égal à 'getStockPrice') {
                  const { result } = toolInvocation;
                  return <Stock key={toolCallId} {...result} />;
                }
              } else {
                return (
                  <div key={toolCallId}>
                    {toolName est égal à 'displayWeather' ? (
                      <div>Chargement du temps météorologique...</div>
                    ) : toolName est égal à 'getStockPrice' ? (
                      <div>Chargement du cours de l'action...</div>
                    ) :

<div>Loading...</div>
                    )}
                  </div>
                );
              }
            })}
          </div>
        </div>
      }}

<form onSubmit={handleSubmit}>
        <input
          type="text"
          valeur={input}
          onChange={event => {
            setInput(event.target.value);
          }}
        />
        <button type="submit">Envoyer</button>
      </form>
    </div>
  );
}
```

En suivant ce modèle, vous pouvez continuer à ajouter davantage d'outils et de composants, élargissant ainsi les capacités de votre application UI générative.

---
titre : Completion
description : Apprenez à utiliser la fonctionnalité de hook useCompletion.
---

# Completion

La fonctionnalité `useCompletion` vous permet de créer une interface utilisateur pour gérer les compléments de texte dans votre application. Elle permet la diffusion en continu des compléments de texte de votre fournisseur AI, gère l'état de l'entrée de chat et met à jour automatiquement l'interface utilisateur à mesure que de nouveaux messages sont reçus.

Dans ce guide, vous apprendrez à utiliser la fonctionnalité `useCompletion` dans votre application pour générer des compléments de texte et les diffuser en temps réel vers vos utilisateurs.

## Exemple

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
      <button type="submit">Soumettre</button>
      <div>{completion}</div>
    </form>
  );
}
```

```ts filename='app/api/completion/route.ts'
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

// Permettre le streaming de réponses jusqu'à 30 secondes
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

Dans le composant `Page`, la fonction de crochet `useCompletion` demandera à votre fournisseur d'API IA chaque fois que l'utilisateur soumet un message. La complétion est ensuite diffusée en temps réel et affichée dans l'interface utilisateur.

Cela permet une expérience de complétion de texte fluide où l'utilisateur peut voir la réponse IA dès qu'elle est disponible, sans avoir à attendre que la réponse entière soit reçue.

## Interface utilisateur personnalisée

`useCompletion` fournit également des moyens de gérer le prompt via le code, d'afficher les états de chargement et d'erreur, et de mettre à jour les messages sans déclencher les interactions de l'utilisateur.

### Chargement et états d'erreur

Pour afficher un spinner de chargement pendant que le chatbot traite le message de l'utilisateur, vous pouvez utiliser l'état `isLoading` retourné par l'hook `useCompletion` :

```tsx
const { isLoading, ... } = useCompletion()

return(
  <>
    {isLoading ? <Spinner /> : null}
  </>
)
```

De même, l'état `error` reflète l'objet d'erreur lancé lors de la requête de fetch. Il peut être utilisé pour afficher un message d'erreur, ou pour afficher une notification de toast :

```tsx
const { error, ... } = useCompletion()

useEffect(() => {
  if (error) {
    toast.error(error.message)
  }
}, [error])

// Ou afficher le message d'erreur dans l'interface utilisateur :
return (
  <>
    {error ? <div>{error.message}</div> : null}
  </>
)
```

### Entrée contrôlée

Dans l'exemple initial, nous avons les appels de callback `handleSubmit` et `handleInputChange` qui gèrent les modifications de l'entrée et les soumissions de formulaire. Ces appels de callback sont utiles pour les cas d'utilisation courants, mais vous pouvez également utiliser des API non contrôlées pour des scénarios avancés comme la validation de formulaire ou des composants personnalisés.

L'exemple suivant démontre comment utiliser des API plus granulaires comme `setInput` avec vos composants d'entrée et de bouton de soumission personnalisés :

```tsx
const { input, setInput } = useCompletion();

return (
  <>
    <MonComposantCustomInput value={input} onChange={value => setInput(value)} />
  </>
);
```

### Annulation

Il s'agit également d'un cas d'utilisation courant pour annuler le message de réponse tout en cours de streaming depuis le fournisseur AI. Vous pouvez faire cela en appelant la fonction `stop` retournée par le hook `useCompletion`.

```tsx
const { stop, isLoading, ... } = useCompletion()

return (
  <>
    <button onClick={stop} disabled={!isLoading}>Arrêter</button>
  </>
)
```

Lorsque l'utilisateur clique sur le bouton "Arrêter", la requête de récupération sera annulée. Cela évite la consommation de ressources inutiles et améliore l'UX de votre application.

### Étalement des mises à jour de l'interface utilisateur

<Note>Cette fonctionnalité est actuellement uniquement disponible pour React.</Note>

Par défaut, le hook `useCompletion` déclenchera une mise à jour de l'interface utilisateur à chaque fois qu'un nouveau morceau est reçu.
Vous pouvez étalement les mises à jour de l'interface utilisateur avec l'option `experimental_throttle`.

```tsx filename="page.tsx" highlight="2-3"
const { completion, ... } = useCompletion({
  // Étalement des mises à jour de la completion et des données à 50ms :
  experimental_throttle: 50
})
```

## Appels de rappel d'événement

`useCompletion` fournit également des appels de rappel d'événement optionnels que vous pouvez utiliser pour gérer différentes étapes du cycle de vie du chatbot. Ces appels de rappel peuvent être utilisés pour déclencher des actions supplémentaires, telles que la journalisation, les analyses ou les mises à jour de l'interface utilisateur personnalisées.

```tsx
const { ... } = useCompletion({
  onResponse: (response: Response) => {
    console.log('Réponse reçue du serveur :', response)
  },
  onFinish: (message: Message) => {
    console.log('Fin de la mise en file d'attente du message :', message)
  },
  onError: (error: Error) => {
    console.error('Une erreur est survenue :', error)
  },
})
```

Il est important de noter que vous pouvez annuler le traitement en lançant une erreur dans le callback `onResponse`. Cela déclenchera le callback `onError` et arrêtera le message d'être ajouté à l'interface utilisateur du chat. Cela peut être utile pour gérer les réponses inattendues du fournisseur AI.

## Configurer les options de requête

Par défaut, l'appel de la fonction `useCompletion` envoie une requête HTTP POST vers l'endpoint `/api/completion` avec le prompt en tant que corps de la requête. Vous pouvez personnaliser la requête en passant des options supplémentaires à la fonction `useCompletion` :

```tsx
const { messages, input, handleInputChange, handleSubmit } = useCompletion({
  api: '/api/completion-personnalisée',
  en-têtes: {
    Autorisation: 'votre_token',
  },
  corps: {
    id_utilisateur: '123',
  },
  credentials: 'same-origin',
});
```

Dans cet exemple, la fonction `useCompletion` envoie une requête POST vers l'endpoint `/api/completion` avec les en-têtes, les champs de corps supplémentaires et les informations de connexion spécifiés pour cette requête. Vous pouvez gérer la requête sur votre serveur avec ces informations supplémentaires.

---
Titre : Génération d'objets
Description : Apprenez à utiliser la fonction `useObject`.
---

# Génération d'objets

<Note>`useObject` est une fonction expérimentale et n'est disponible que dans React.</Note>

La fonction [`useObject`](/docs/reference/ai-sdk-ui/use-object) vous permet de créer des interfaces qui représentent un objet JSON structuré qui est transmis en flux.

Dans ce guide, vous apprendrez à utiliser la fonction `useObject` dans votre application pour générer des interfaces de données structurées en temps réel.

## Exemple

L'exemple montre une petite application de notifications qui génère des notifications fictives en temps réel.

### Schéma

Il est utile de définir le schéma dans un fichier séparé qui est importé à la fois sur le client et sur le serveur.

```ts fichier='app/api/notifications/schema.ts'
import { z } from 'zod';

// Définir un schéma pour les notifications
export const notificationSchema = z.object({
  notifications: z.array(
    z.object({
      nom: z.string().describe('Nom d\'une personne fictive.'),
      message: z.string().describe('Message. N\'utilisez pas d\'émoticônes ou de liens.'),
    }),
  ),
});
```

### Client

Le client utilise `useObject` pour diffuser le processus de génération d'objet.

Les résultats sont partiels et sont affichés dès qu'ils sont reçus.
Veuillez noter le code pour gérer les valeurs `undefined` dans le JSX.

```tsx fichier='app/page.tsx'
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
      <button onClick={() => submit('Messages pendant la semaine des finales.')}>
        Générer des notifications
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

### Serveur

Sur le serveur, nous utilisons [`streamObject`](/docs/reference/ai-sdk-core/stream-object) pour diffuser le processus de génération d'objets.

```typescript filename='app/api/notifications/route.ts'
import { openai } from '@ai-sdk/openai';
import { streamObject } from 'ai';
import { notificationSchema } from './schema';

// Autoriser les réponses en flux jusqu'à 30 secondes
export const maxDuration = 30;

export async function POST(req: Request) {
  const context = await req.json();

  const result = streamObject({
    model: openai('gpt-4-turbo'),
    schema: notificationSchema,
    prompt:
      `Générer 3 notifications pour une application de messages dans ce contexte :` + context,
  });

  return result.toTextStreamResponse();
}
```

## Interface personnalisée

`useObject` fournit également des moyens de montrer les états de chargement et d'erreur :

### État de Chargement

L'état `isLoading` retourné par l'hook `useObject` peut être utilisé à plusieurs fins :

- Pour afficher un spinner de chargement pendant que l'objet est généré.
- Pour désactiver le bouton de soumission.

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
        onClick={() => submit('Messages pendant la semaine des finales.')}
        disabled={isLoading}
      >
        Générer des notifications
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

### Gestionnaire d'arrêt

La fonction `stop` peut être utilisée pour arrêter le processus de génération d'objets. Cela peut être utile si l'utilisateur souhaite annuler la demande ou si le serveur prend trop de temps pour répondre.

```tsx filename='app/page.tsx' highlight="6,14-16"
'use client';

import { useObject } from '@ai-sdk/react';

export default function Page() {
  const { isLoading, stop, object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <>
      {isLoading && (
        <button type="button" onClick={() => stop()}>
          Arrêter
        </button>
      )}

      <button onClick={() => submit('Messages pendant la semaine des finales.')}>
        Générer des notifications
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

### État d'Erreur

De même, l'état `error` reflète l'objet d'erreur lancé lors de la requête de récupération.
Il peut être utilisé pour afficher un message d'erreur, ou pour désactiver le bouton de soumission :

<Note>
  Nous recommandons de montrer un message d'erreur générique à l'utilisateur, tel que "Quelque chose s'est mal passé." C'est une bonne pratique pour éviter de faire transparaître des informations du serveur.
</Note>

```tsx fichier="app/page.tsx" mise-en-évidence="6,13"
'use client';

import { useObject } from '@ai-sdk/react';

export default function Page() {
  const { error, object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <>
      {error && <div>Une erreur est survenue.</div>}

      <button onClick={() => submit('Messages pendant la semaine des finales.')}>
        Générer des notifications
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

## Appels de rappel d'événement

`useObject` fournit des appels de rappel d'événement optionnels que vous pouvez utiliser pour gérer les événements de cycle de vie.

- `onFinish`: Appelé lorsque la génération de l'objet est terminée.
- `onError`: Appelé lorsque survenue d'une erreur lors de la requête de récupération.

Ces appels de rappel peuvent être utilisés pour déclencher des actions supplémentaires, telles que la journalisation, l'analytique ou les mises à jour de l'interface utilisateur personnalisée.

```tsx filename='app/page.tsx' highlight="10-20"
'use client';

import { experimental_useObject as useObject } from '@ai-sdk/react';
import { notificationSchema } from './api/notifications/schema';

export default function Page() {
  const { object, submit } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
    onFinish({ object, error }) {
      // objet typé, indéfini si la validation du schéma échoue :
      console.log('Génération de l\'objet terminée :', object);

      // erreur, indéfini si la validation du schéma réussit :
      console.log('Erreur de validation du schéma :', error);
    },
    onError(error) {
      // erreur lors de la requête de récupération :
      console.error('Une erreur est survenue :', error);
    },
  });

  return (
    <div>
      <button onClick={() => submit('Messages pendant la semaine des finaux.')}>
        Générer des notifications
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

## Configurer les Options de Demande

Vous pouvez configurer l'endpoint de l'API, les en-têtes facultatifs et les informations d'identification en utilisant les paramètres `api`, `headers` et `credentials`.

```tsx highlight="2-5"
const { submit, object } = useObject({
  api: '/api/use-object',
  headers: {
    'X-Custom-Header': 'CustomValue',
  },
  credentials: 'include',
  schema: votreSchema,
});
```

---
titre : Assistants OpenAI
description : Apprenez à utiliser la fonctionnalité useAssistant.
---

# Assistants OpenAI

La fonctionnalité `useAssistant` vous permet de gérer l'état du client lors de l'interaction avec une API compatible assistant OpenAI.
Cette fonctionnalité est utile lorsque vous souhaitez intégrer les capacités d'assistant dans votre application,
avec l'interface utilisateur mise à jour automatiquement pendant l'exécution de l'assistant.

La fonctionnalité `useAssistant` est prise en charge dans `@ai-sdk/react`, `ai/svelte` et `ai/vue`.

## Exemple

```tsx fichier='app/page.tsx'
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

## Utilisation

Pour utiliser ce composant, vous devez importer le module `@ai-sdk/react` et le composant `

```jsx
<form onSubmit={soumettreMessage}>
        <input
          disabled={etat !== 'en_attente_de_message'}
          value={input}
          placeholder="Quel est la température du salon ?"
          onChange={changerInput}
        />
      </form>
    </div>
  );
}
```

```tsx fichier='app/api/assistant/route.ts'
import { AssistantResponse } from 'ai';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || '',
});

// Permettre le streaming des réponses jusqu'à 30 secondes
export const maxDuration = 30;

export async function POST(req: Request) {
  // Parser le corps de la demande
  const input: {
    threadId: string | null;
    message: string;
  } = await req.json();

  // Créer un fil s'il est nécessaire
  const threadId = input.threadId ?? (await openai.beta.threads.create({})).id;

  // Ajouter un message au fil
  const createdMessage = await openai.beta.threads.messages.create(threadId, {
    role: 'user',
    content: input.message,
  });
```

```markdown
retourner AssistantResponse(
    { threadId, messageId: createdMessage.id },
    async ({ forwardStream, sendDataMessage }) => {
      // Exécuter l'assistant sur le fil de discussion
      const runStream = openai.beta.threads.runs.stream(threadId, {
        assistant_id:
          process.env.ASSISTANT_ID ?? 
          () => {
            throw new Error('ASSISTANT_ID n\'est pas défini');
          }(),
      });

      // Envoyer le statut de l'exécution de l'assistant serait un flux de messages delta
      let runResult = await forwardStream(runStream);

      // Le statut peut être : en attente, en cours de traitement, nécessite une action, annulation, annulé, échec, terminé ou expiré
      while (
        runResult?.status === 'requires_action' &&
        runResult.required_action?.type === 'submit_tool_outputs'
      ) {
        const tool_outputs =
          runResult.required_action.submit_tool_outputs.tool_calls.map(
            (toolCall: any) => {
              const parameters = JSON.parse(toolCall.function.arguments);

              switch (toolCall.function.name) {
                // configurer vos appels de fonction ici
```

```javascript
default:
  lancer une nouvelle erreur (
    `Fonction d'appel d'outil inconnue : ${toolCall.function.name}`,
  );
},
```

Note : J'ai utilisé la traduction directe des mots pour conserver la signification, mais si vous souhaitez une traduction plus fluide, je peux vous aider.

## Interface personnalisée

`useAssistant` fournit également des moyens de gérer les états des messages de chat et de saisie via le code et d'afficher les états de chargement et d'erreur.

### États de chargement et d'erreur

Pour afficher un spinner de chargement pendant que l'assistant exécute le thread, vous pouvez utiliser l'état `status` retourné par l'appel à la fonction `useAssistant` :

```tsx
const { status, ... } = useAssistant()

return(
  <>
    {status === "in_progress" ? <Spinner /> : null}
  </>
)
```

De même, l'état `error` reflète l'objet d'erreur lancé lors de la requête de récupération. Il peut être utilisé pour afficher un message d'erreur ou pour afficher une notification de toast :

```tsx
const { error, ... } = useAssistant()

useEffect(() => {
  if (error) {
    toast.error(error.message)
  }
}, [error])

// Ou afficher le message d'erreur dans l'interface utilisateur :
return (
  <>
    {error ? <div>{error.message}</div> : null}
  </>
)
```

### Saisie contrôlée

Dans l'exemple initial, nous avons les appels à `handleSubmit` et `handleInputChange` qui gèrent les modifications de saisie et les soumissions de formulaire. Ces appels sont utiles pour les cas d'utilisation courants, mais vous pouvez également utiliser des API non contrôlées pour des scénarios plus avancés tels que la validation de formulaire ou des composants personnalisés.

L'exemple suivant montre comment utiliser des API plus granulaires comme `append` avec vos composants de saisie personnalisés et de bouton de soumission :

```tsx
const { append } = useAssistant();

return (
  <>
    <MonBoutonDeSoumission
      onClick={() => {
        // Envoyer un nouveau message au fournisseur d'IA
        append({
          role: 'user',
          content: input,
        });
      }}
    />
  </>
);
```

## Configurer les Options de Demande

Par défaut, l'hook `useAssistant` envoie une requête HTTP POST vers l'endpoint `/api/assistant` avec le prompt comme partie du corps de la demande. Vous pouvez personnaliser la demande en passant des options supplémentaires à l'hook `useAssistant` :

```tsx
const { messages, input, handleInputChange, handleSubmit } = useAssistant({
  api: '/api/custom-completion',
  headers: {
    Authorization: 'votre_token',
  },
  body: {
    user_id: '123',
  },
  credentials: 'same-origin',
});
```

Dans cet exemple, l'hook `useAssistant` envoie une requête POST vers l'endpoint `/api/custom-completion` avec les en-têtes, les champs du corps de la demande et les informations de connexion spécifiés pour la requête de fetch. Sur votre serveur, vous pouvez gérer la demande avec ces informations supplémentaires.

---
titre : Streaming de Données Custom
description : Apprenez à streamer des données custom vers le client.
---

# Streaming de Données Custom

Il est souvent utile d'envoyer des données supplémentaires en parallèle de la réponse du modèle.
Par exemple, vous pouvez vouloir envoyer des informations de statut, les identifiants de message après les avoir stockés,
ou des références au contenu auquel se réfère le modèle de langage.

Le SDK de l'IA fournit plusieurs outils qui permettent de streamer des données supplémentaires vers le client
et de les attacher soit au `Message` soit à l'objet `data` de l'hook `useChat` :

- `createDataStream`: crée un flux de données
- `createDataStreamResponse`: crée un objet de réponse qui streame des données
- `pipeDataStreamToResponse`: pipe un flux de données vers un objet de réponse du serveur

Les données sont streamées en tant que partie du flux de réponse.

## Envoi de Données Custom du Serveur

Dans votre gestionnaire de route côté serveur, vous pouvez utiliser `createDataStreamResponse` et `pipeDataStreamToResponse` en combinaison avec `streamText`.
Vous devez :

1. Appeler `createDataStreamResponse` ou `pipeDataStreamToResponse` pour obtenir une fonction de rappel avec un `DataStreamWriter`.
2. Écrire dans le `DataStreamWriter` pour diffuser des données supplémentaires.
3. Mélanger le résultat de `streamText` dans le `DataStreamWriter`.
4. Retourner la réponse de `createDataStreamResponse` (si cette méthode est utilisée)

Voici un exemple :

```tsx filename="route.ts" highlight="7-10,16,19-23,25-26,30"
import { openai } from '@ai-sdk/openai';
import { generateId, createDataStreamResponse, streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  // démarrer immédiatement la diffusion (résout les problèmes RAG avec le statut, etc.)
  return createDataStreamResponse({
    execute: dataStream => {
      dataStream.writeData('appel initialisé');

      const result = streamText({
        model: openai('gpt-4o'),
        messages,
        onChunk() {
          dataStream.writeMessageAnnotation({ chunk: '123' });
        },
        onFinish() {
          // annotation de message :
          dataStream.writeMessageAnnotation({
            id: generateId(), // par exemple, id à partir d'un enregistrement DB sauvegardé
            autre: 'information',
          });

          // annotation d'appel :
          dataStream.writeData('appel terminé');
        },
      });
```

```javascript
result.mergeIntoDataStream(dataStream);
},
onError: erreur => {
  // Les messages d'erreur sont masqués par défaut pour des raisons de sécurité.
  // Si vous souhaitez exposer le message d'erreur au client, vous pouvez le faire ici :
  return erreur instanceof Error ? erreur.message : String(erreur);
},
```

<Note>
  Vous pouvez également envoyer des données de flux à partir de backends personnalisés, par exemple Python / FastAPI,
  en utilisant le [Protocole de flux de données](/docs/ai-sdk-ui/stream-protocol)

# Protocole de flux de données).

</Note>

## Envoyer des sources personnalisées

Vous pouvez envoyer des sources personnalisées au client en utilisant la méthode `writeSource` sur l'objet `DataStreamWriter` :

```tsx filename="route.ts" highlight="9-15"
import { openai } from '@ai-sdk/openai';
import { createDataStreamResponse, streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  return createDataStreamResponse({
    execute: dataStream => {
      // écrire une source URL personnalisée dans le flux :
      dataStream.writeSource({
        sourceType: 'url',
        id: 'source-1',
        url: 'https://example.com',
        title: 'Exemple de source',
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

## Traitement de données personnalisées dans `useChat`

La fonction hook `useChat` traite automatiquement les données en flux et les rend disponibles pour vous.

### Accéder aux données

Sur le client, vous pouvez déstructurer `data` de la fonction hook `useChat` qui stocke toutes les `StreamData` sous forme de `JSONValue[]`.

```tsx filename="page.tsx"
import { useChat } from '@ai-sdk/react';

const { data } = useChat();
```

### Accéder aux Annotations de Message

Chaque message de l'hook `useChat` possède une propriété facultative `annotations` qui contient les annotations de message envoyées par le serveur.

Puisque la forme des annotations dépend de ce que vous envoyez du côté serveur,
vous devez les déstructurer d'une manière sécurisée par type côté client.

Ici, nous affichons simplement les annotations sous forme de chaîne JSON :

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

### Mettre à jour et Effacer les Données

Vous pouvez mettre à jour et effacer l'objet `data` de l'hook `useChat` en utilisant la fonction `setData`.

```tsx filename="page.tsx"
const { setData } = useChat();

// effacer les données existantes
setData(undefined);

// définir de nouvelles données
setData([{ test: 'value' }]);

// transformer les données existantes, par exemple en ajoutant des valeurs supplémentaires :
setData(currentData => [...currentData, { test: 'value' }]);
```

#### Exemple : Nettoyer à la soumission

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
          setData(undefined); // Effacer les données de flux
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
title: Gestion des Erreurs
description: Apprenez à gérer les erreurs dans l'interface utilisateur de l'API AI
---

# Gestion des Erreurs

### Objet d'aide aux erreurs

Chaque hook de l'interface utilisateur de l'API AI renvoie également un [erreur](/docs/reference/ai-sdk-ui/use-chat)

# Erreur) objet que vous pouvez utiliser pour afficher l'erreur dans votre interface utilisateur.
Vous pouvez utiliser l'objet erreur pour afficher un message d'erreur, désactiver le bouton de soumission ou afficher un bouton de réessayer.

<Note>
  Nous recommandons d'afficher un message d'erreur générique à l'utilisateur, tel que "Quelque chose s'est mal passé." C'est une bonne pratique pour éviter de révéler des informations du serveur.
</Note>

```tsx fichier="app/page.tsx" mise en surbrillance="7,17-24,30"
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
          <div>Une erreur est survenue.</div>
          <button type="button" onClick={() => reload()}>
            Réessayer
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

#### Alternative : remplacez le dernier message

Alternativement, vous pouvez écrire un gestionnaire de soumission personnalisé qui remplace le dernier message lorsque des erreurs sont présentes.

```tsx fichier="app/page.tsx" highlight="15-21,33"
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
      setMessages(messages.slice(0, -1)); // supprimez le dernier message
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

      {error && <div>Une erreur est survenue.</div>}

      <form onSubmit={customSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

### Callback de gestion des erreurs

Les erreurs peuvent être traitées en passant un [`onError`](/docs/reference/ai-sdk-ui/use-chat)

# (on-error) fonction de rappel en tant qu'option pour les hooks [`useChat`](/docs/reference/ai-sdk-ui/use-chat), [`useCompletion`](/docs/reference/ai-sdk-ui/use-completion) ou [`useAssistant`](/docs/reference/ai-sdk-ui/use-assistant).
La fonction de rappel reçoit un objet d'erreur en argument.

```tsx fichier="app/page.tsx" highlight="8-11"
import { useChat } from '@ai-sdk/react';

export default function Page() {
  const {
    /* ... */
  } = useChat({
    // gérer l'erreur :
    onError: erreur => {
      console.error(erreur);
    },
  });
}
```

### Injection d'erreurs pour les tests

Vous pouvez peut-être vouloir créer des erreurs pour les tests.
Vous pouvez facilement le faire en lançant une erreur dans votre gestionnaire de route :

```ts fichier="app/api/chat/route.ts"
export async function POST(req: Request) {
  throw new Error('Ceci est une erreur de test');
}
```

---
titre : Streaming fluide du texte japonais
description : Apprenez à streamer du texte japonais de manière fluide
---

# Streaming fluide du texte japonais

Vous pouvez streamer du texte japonais de manière fluide en utilisant la fonction `smoothStream` et le regex suivant qui divise soit sur les mots de caractères japonais :

```tsx fichier="page.tsx"
import { smoothStream } from 'ai';
import { useChat } from '@ai-sdk/react';

const { data } = useChat({
  experimental_transform: smoothStream({
    chunking: /[\u3040-\u309F\u30A0-\u30FF]|\S+\s+/,
  }),
});
```

---
titre : Streaming fluide du texte chinois
description : Apprenez à streamer du texte chinois de manière fluide
---

# Flux de streaming chinois

Vous pouvez fluxer de manière smooth le texte chinois en utilisant la fonction `smoothStream` et la regex suivante qui sépare soit sur des mots soit sur des caractères chinois :

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
titre : AI_APICallError
description : Apprenez à résoudre l'erreur AI_APICallError
---

# AI_APICallError

Cette erreur se produit lorsqu'une appel API échoue.

## Propriétés

- `url` : L'URL de la requête API qui a échoué
- `requestBodyValues` : Les valeurs du corps de la requête envoyées à l'API
- `statusCode` : Le code de statut HTTP retourné par l'API
- `responseHeaders` : Les en-têtes de réponse retournés par l'API
- `responseBody` : Le corps de réponse retourné par l'API
- `isRetryable` : Si la requête peut être réessayée en fonction du code de statut
- `data` : Toute donnée supplémentaire associée à l'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_APICallError` en utilisant :

```typescript
import { APICallError } from 'ai';

if (APICallError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_DownloadError
description : Apprenez à résoudre l'erreur AI_DownloadError
---

# AI_DownloadError

Cette erreur se produit lorsqu'un téléchargement échoue.

## Propriétés

- `url` : L'URL qui a échoué à télécharger
- `statusCode` : Le code de statut HTTP retourné par le serveur
- `statusText` : Le texte de statut HTTP retourné par le serveur
- `message` : Le message d'erreur contenant des détails sur l'échec du téléchargement

## Vérification de cet Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_DownloadError` en utilisant :

```typescript
import { DownloadError } from 'ai';

if (DownloadError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_EmptyResponseBodyError
description : Apprenez à résoudre AI_EmptyResponseBodyError
---

# AI_EmptyResponseBodyError

Cette erreur se produit lorsque le serveur retourne un corps de réponse vide.

## Propriétés

- `message`: Le message d'erreur

## Vérification de cet Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_EmptyResponseBodyError` en utilisant :

```typescript
import { EmptyResponseBodyError } from 'ai';

if (EmptyResponseBodyError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidArgumentError
description : Apprenez à résoudre AI_InvalidArgumentError
---

# AI_InvalidArgumentError

Cette erreur se produit lorsque des arguments invalides ont été fournis.

## Propriétés

- `parameter`: Le nom du paramètre qui est invalide
- `value`: La valeur invalide
- `message`: Le message d'erreur

## Vérification de cet Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidArgumentError` en utilisant :

```typescript
import { InvalidArgumentError } from 'ai';

if (InvalidArgumentError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidDataContentError
description : Comment résoudre AI_InvalidDataContentError
---

# AI_InvalidDataContentError

Cette erreur se produit lorsque le contenu de données fourni dans une partie de message multimodal est invalide. Consultez les [ exemples de requêtes pour les messages multimodaux ](/docs/foundations/prompts#message-prompts).

## Propriétés

- `content`: La valeur de contenu invalide
- `message`: Le message d'erreur décrivant les types de contenu attendus et reçus

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidDataContentError` en utilisant :

```typescript
import { InvalidDataContentError } from 'ai';

if (InvalidDataContentError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidDataContent
description : Apprenez à corriger AI_InvalidDataContent
---

# AI_InvalidDataContent

Cette erreur se produit lorsque du contenu de données non valide est fourni.

## Propriétés

- `content` : La valeur de contenu non valide
- `message` : Le message d'erreur
- `cause` : La cause de l'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidDataContent` en utilisant :

```typescript
import { InvalidDataContent } from 'ai';

if (InvalidDataContent.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidMessageRoleError
description : Apprenez à corriger AI_InvalidMessageRoleError
---

# AI_InvalidMessageRoleError

Cette erreur se produit lorsque un rôle de message non valide est fourni.

## Propriétés

- `role` : La valeur de rôle non valide
- `message` : Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidMessageRoleError` en utilisant :

```typescript
import { InvalidMessageRoleError } from 'ai';

if (InvalidMessageRoleError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidPromptError
description : Apprenez à corriger AI_InvalidPromptError
---

# AI_InvalidPromptError

Cette erreur se produit lorsque la prompt fournie est non valide.

## Propriétés

- `prompt` : La valeur de prompt non valide
- `message` : Le message d'erreur
- `cause` : La cause de l'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidPromptError` en utilisant :

```typescript
import { InvalidPromptError } from 'ai';

if (InvalidPromptError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidResponseDataError
description : Apprenez à résoudre AI_InvalidResponseDataError
---

# AI_InvalidResponseDataError

Cette erreur se produit lorsque le serveur retourne une réponse avec un contenu de données invalides.

## Propriétés

- `data`: La valeur de données de réponse invalides
- `message`: Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidResponseDataError` en utilisant :

```typescript
import { InvalidResponseDataError } from 'ai';

if (InvalidResponseDataError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_InvalidToolArgumentsError
description : Apprenez à résoudre AI_InvalidToolArgumentsError
---

# AI_InvalidToolArgumentsError

Cette erreur se produit lorsque des arguments de l'outil invalides ont été fournis.

## Propriétés

- `toolName`: Le nom de l'outil avec des arguments invalides
- `toolArgs`: Les arguments de l'outil invalides
- `message`: Le message d'erreur
- `cause`: La cause de l'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_InvalidToolArgumentsError` en utilisant :

```typescript
import { InvalidToolArgumentsError } from 'ai';

if (InvalidToolArgumentsError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_JSONParseError
description : Apprenez à résoudre AI_JSONParseError
---

# AI_JSONParseError

Cette erreur se produit lorsque JSON ne parvient pas à s'analyser.

## Propriétés

- `text`: La valeur de texte qui ne peut pas être analysée
- `message`: Le message d'erreur incluant les détails de l'erreur d'analyse

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_JSONParseError` en utilisant :

```typescript
import { JSONParseError } from 'ai';

if (JSONParseError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_LoadAPIKeyError
description : Apprenez à résoudre AI_LoadAPIKeyError
---

# AI_LoadAPIKeyError

Cette erreur se produit lorsque la clé API n'est pas chargée avec succès.

## Propriétés

- `message`: Le message d'erreur

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_LoadAPIKeyError` en utilisant :

```typescript
import { LoadAPIKeyError } from 'ai';

if (LoadAPIKeyError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_LoadSettingError
description : Apprenez à résoudre AI_LoadSettingError
---

# AI_LoadSettingError

Cette erreur se produit lorsque l'enregistrement n'est pas chargé avec succès.

## Propriétés

- `message`: Le message d'erreur

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_LoadSettingError` en utilisant :

```typescript
import { LoadSettingError } from 'ai';

if (LoadSettingError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_MessageConversionError
description : Apprenez à résoudre AI_MessageConversionError
---

# AI_MessageConversionError

Cette erreur se produit lorsque la conversion de message échoue.

## Propriétés

- `originalMessage`: Le message original qui a échoué à la conversion
- `message`: Le message d'erreur

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_MessageConversionError` en utilisant :

```typescript
import { MessageConversionError } from 'ai';

if (MessageConversionError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_NoAudioGeneratedError
description : Apprenez à résoudre AI_NoAudioGeneratedError
---

# Erreur_AI_NoAudioGeneratedError

Cette erreur se produit lorsque l'audio ne peut pas être généré à partir de l'entrée.

## Propriétés

- `réponses` : Tableau de réponses
- `message` : Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoAudioGeneratedError` en utilisant :

```typescript
import { NoAudioGeneratedError } from 'ai';

if (NoAudioGeneratedError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : Erreur_AI_NoContentGeneratedError
description : Apprenez à résoudre l'erreur AI_NoContentGeneratedError
---

 # Erreur_AI_NoContentGeneratedError

Cette erreur se produit lorsque le fournisseur d'IA échoue à générer du contenu.

## Propriétés

- `message` : Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoContentGeneratedError` en utilisant :

```typescript
import { NoContentGeneratedError } from 'ai';

if (NoContentGeneratedError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : Erreur_AI_NoImageGeneratedError
description : Apprenez à résoudre l'erreur AI_NoImageGeneratedError
---

 # Erreur_AI_NoImageGeneratedError

Cette erreur se produit lorsque le fournisseur d'IA échoue à générer une image.
Elle peut survenir en raison des raisons suivantes :

- Le modèle a échoué à générer une réponse.
- Le modèle a généré une réponse non valide.

## Propriétés

- `message` : Le message d'erreur.
- `réponses` : Métadonnées sur les réponses du modèle d'image, y compris la date, le modèle et les en-têtes.
- `cause` : La cause de l'erreur. Vous pouvez utiliser cela pour une gestion d'erreur plus détaillée.

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoObjectGeneratedError` en utilisant :

```typescript
import { generateImage, NoImageGeneratedError } from 'ai';

try {
  await generateImage({ model, prompt });
} catch (error) {
  if (NoImageGeneratedError.isInstance(error)) {
    console.log('NoImageGeneratedError');
    console.log('Cause:', error.cause);
    console.log('Réponses:', error.responses);
  }
}
```

---
Titre : AI_NoObjectGeneratedError
Description : Apprenez à résoudre AI_NoObjectGeneratedError
---

# AI_NoObjectGeneratedError

Cette erreur se produit lorsque le fournisseur d'IA échoue à générer un objet pouvant être analysé qui correspond au schéma.
Elle peut survenir en raison des raisons suivantes :

- Le modèle a échoué à générer une réponse.
- Le modèle a généré une réponse qui ne pouvait pas être analysée.
- Le modèle a généré une réponse qui ne pouvait pas être validée par rapport au schéma.

## Propriétés

- `message`: Le message d'erreur.
- `text`: Le texte généré par le modèle. Cela peut être le texte brut ou le texte de l'appel de l'outil, en fonction du mode de génération d'objet.
- `response`: Métadonnées sur la réponse du modèle de langage, y compris l'ID de la réponse, la date et l'heure, et le modèle.
- `usage`: Utilisation du jeton de demande.
- `finishReason`: Raison de fin de la demande. Par exemple 'length' si le modèle a généré le nombre maximum de jetons, ce qui pourrait entraîner une erreur de parsing JSON.
- `cause`: La cause de l'erreur (par exemple une erreur de parsing JSON). Vous pouvez utiliser cela pour une gestion d'erreur plus détaillée.

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoObjectGeneratedError` en utilisant :

```typescript
import { generateObject, NoObjectGeneratedError } from 'ai';

try {
  await generateObject({ model, schema, prompt });
} catch (error) {
  if (NoObjectGeneratedError.isInstance(error)) {
    console.log('NoObjectGeneratedError');
    console.log('Cause:', error.cause);
    console.log('Text:', error.text);
    console.log('Response:', error.response);
    console.log('Usage:', error.usage);
    console.log('Reason de Fin:', error.finishReason);
  }
}
```

---
titre : AI_NoOutputSpecifiedError
description : Apprenez à corriger AI_NoOutputSpecifiedError
---

# AI_NoOutputSpecifiedError

Cette erreur se produit lorsqu'aucune format de sortie n'a été spécifié pour la réponse de l'IA, et que des méthodes liées à la sortie sont appelées.

## Propriétés

- `message`: Le message d'erreur (par défaut 'Aucune sortie spécifiée.')

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoOutputSpecifiedError` en utilisant :

```typescript
import { NoOutputSpecifiedError } from 'ai';

if (NoOutputSpecifiedError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_NoSuchModelError
description : Apprenez à corriger AI_NoSuchModelError
---

# AI_NoSuchModelError

Cette erreur se produit lorsqu'un ID de modèle n'est pas trouvé.

## Propriétés

- `modelId`: L'ID du modèle qui n'a pas été trouvé
- `modelType`: Le type de modèle
- `message`: Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoSuchModelError` en utilisant :

```typescript
import { NoSuchModelError } from 'ai';

if (NoSuchModelError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_NoSuchProviderError
description : Apprenez à résoudre l'erreur AI_NoSuchProviderError
---

# AI_NoSuchProviderError

Cette erreur se produit lorsque l'ID d'un fournisseur n'est pas trouvé.

## Propriétés

- `providerId`: L'ID du fournisseur qui n'a pas été trouvé
- `availableProviders`: Tableau des ID de fournisseurs disponibles
- `modelId`: L'ID du modèle
- `modelType`: Le type de modèle
- `message`: Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoSuchProviderError` en utilisant :

```typescript
import { NoSuchProviderError } from 'ai';

if (NoSuchProviderError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_NoSuchToolError
description : Apprenez à résoudre l'erreur AI_NoSuchToolError
---

# AI_NoSuchToolError

Cette erreur se produit lorsque le modèle tente d'appeler un outil non disponible.

## Propriétés

- `toolName`: Le nom de l'outil qui n'a pas été trouvé
- `availableTools`: Tableau des noms d'outils disponibles
- `message`: Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoSuchToolError` en utilisant :

```typescript
import { NoSuchToolError } from 'ai';

if (NoSuchToolError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_NoTranscriptGeneratedError
description : Apprenez à résoudre l'erreur AI_NoTranscriptGeneratedError
---

# AI_NoTranscriptGeneratedError

Cette erreur se produit lorsque aucun transcript n'a pu être généré à partir de l'entrée.

## Propriétés

- `responses`: Tableau de réponses
- `message`: Le message d'erreur

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_NoTranscriptGeneratedError` à l'aide de :

```typescript
import { NoTranscriptGeneratedError } from 'ai';

if (NoTranscriptGeneratedError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_RetryError
description : Apprenez à résoudre AI_RetryError
---

# AI_RetryError

Cette erreur se produit lorsqu'une opération de réessai échoue.

## Propriétés

- `reason`: La raison de l'échec de la réessai
- `lastError`: L'erreur la plus récente qui s'est produite pendant les tentatives de réessai
- `errors`: Tableau de toutes les erreurs qui se sont produites pendant les tentatives de réessai
- `message`: Le message d'erreur

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_RetryError` à l'aide de :

```typescript
import { RetryError } from 'ai';

if (RetryError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_TooManyEmbeddingValuesForCallError
description : Apprenez à résoudre AI_TooManyEmbeddingValuesForCallError
---

# AI_TooManyEmbeddingValuesForCallError

Cette erreur se produit lorsqu'un trop grand nombre de valeurs sont fournies dans une seule appelle d'embeddings.

## Propriétés

- `provider`: Le nom du fournisseur d'IA
- `modelId`: L'ID du modèle d'embeddings
- `maxEmbeddingsPerCall`: Le nombre maximum d'embeddings autorisé par appel
- `values`: Le tableau de valeurs qui a été fourni

## Vérifier cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_TooManyEmbeddingValuesForCallError` à l'aide de :

```typescript
import { TooManyEmbeddingValuesForCallError } from 'ai';

if (TooManyEmbeddingValuesForCallError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : ToolCallRepairError
description : Apprenez à résoudre AI SDK ToolCallRepairError
---

# ErreurDeRéparationDeLaFonctionD'outillage

Cette erreur se produit lorsqu'il y a une erreur lors de la tentative de réparation d'une appelle d'outillage non valide.
Cela se produit généralement lorsque l'IA tente de corriger soit
une `ErreurDeNonExistanceDeL'outillage` ou une `ErreurDeParamètresD'outillageInvalides`.

## Propriétés

- `originalError`: L'erreur originale qui a déclenché l'essai de réparation (soit `ErreurDeNonExistanceDeL'outillage` ou `ErreurDeParamètresD'outillageInvalides`)
- `message`: Le message d'erreur
- `cause`: L'erreur sous-jacente qui a causé la réparation à échouer

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `ErreurDeRéparationDeLaFonctionD'outillage` à l'aide de :

```typescript
import { ToolCallRepairError } from 'ai';

if (ToolCallRepairError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : ErreurD'ExécutionDeL'IA
description : Apprenez à résoudre l'erreur d'exécution de l'IA
---

# ErreurD'ExécutionDeL'IA

Cette erreur se produit lorsqu'il y a une erreur lors de l'exécution d'un outillage.

## Propriétés

- `toolName`: Le nom de l'outillage qui a échoué
- `toolArgs`: Les arguments passés à l'outillage
- `toolCallId`: L'ID de l'appel d'outillage qui a échoué
- `message`: Le message d'erreur
- `cause`: L'erreur sous-jacente qui a causé l'exécution de l'outillage à échouer

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `ErreurD'ExécutionDeL'IA` à l'aide de :

```typescript
import { ToolExecutionError } from 'ai';

if (ToolExecutionError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : ErreurDeValidationDeTypeDeL'IA
description : Apprenez à résoudre l'erreur de validation de type de l'IA
---

# ErreurDeValidationDeTypeDeL'IA

Cette erreur se produit lorsqu'il y a une erreur lors de la validation de type.

## Propriétés

- `value`: La valeur qui a échoué à la validation
- `message`: Le message d'erreur incluant les détails de validation

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_TypeValidationError` en utilisant :

```typescript
import { TypeValidationError } from 'ai';

if (TypeValidationError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : AI_UnsupportedFunctionalityError
description : Apprenez à résoudre l'erreur AI_UnsupportedFunctionalityError
---

# AI_UnsupportedFunctionalityError

Cette erreur se produit lorsque la fonctionnalité n'est pas prise en charge.

## Propriétés

- `functionality`: Le nom de la fonctionnalité non prise en charge
- `message`: Le message d'erreur

## Vérification de cette Erreur

Vous pouvez vérifier si une erreur est une instance de `AI_UnsupportedFunctionalityError` en utilisant :

```typescript
import { UnsupportedFunctionalityError } from 'ai';

if (UnsupportedFunctionalityError.isInstance(error)) {
  // Gérer l'erreur
}
```

---
titre : xAI Grok
description : Apprenez à utiliser xAI Grok.
---

# Fournisseur xAI Grok

Le [fournisseur xAI Grok](https://x.ai) contient le support du modèle de langage pour l'[API xAI](https://x.ai/api).

## Configuration

Le fournisseur xAI Grok est disponible via le module `@ai-sdk/xai`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `xai` à partir de `@ai-sdk/xai` :

```ts
import { xai } from '@ai-sdk/xai';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createXai` à partir de `@ai-sdk/xai` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createXai } from '@ai-sdk/xai';

const xai = createXai({
  apiKey: 'votre-clé-api',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur xAI :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  La valeur par défaut est `https://api.x.ai/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. La valeur par défaut est la variable d'environnement `XAI_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). La valeur par défaut est la fonction `fetch` globale.
  Vous pouvez l'utiliser comme middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour les tests, par exemple.

## Modèles de Langage

Vous pouvez créer des [modèles xAI](https://console.x.ai) à l'aide d'une instance de fournisseur. La première argument est l'ID du modèle, par exemple `grok-beta`.

```ts
const model = xai('grok-3');
```

### Exemple

Vous pouvez utiliser les modèles de langage xAI pour générer du texte avec la fonction `generateText` :

```ts
import { xai } from '@ai-sdk/xai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: xai('grok-3'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage xAI peuvent également être utilisés dans les fonctions `streamText`, `generateObject`, et `streamObject`
(voir [Core de l'API AI](/docs/ai-sdk-core)).

### Modèles de conversation

Les modèles de conversation xAI supportent également certaines paramètres spécifiques au modèle qui ne font pas partie
des [paramètres de l'appel standard](/docs/ai-sdk-core/settings). Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = xai('grok-3', {
  user: 'test-user', // identifiant utilisateur unique facultatif
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles de conversation xAI :

- **user** _chaîne_

  Un identifiant unique représentant votre utilisateur final, qui peut aider xAI à
  surveiller et détecter les abus.

Les modèles de conversation xAI supportent également certaines options spécifiques au fournisseur. Vous pouvez les passer dans l'argument `providerOptions` :

```ts
const model = xai('grok-3');

await generateText({
  model,
  providerOptions: {
    xai: {
      raisonningEffort: 'high',
    },
  },
});
```

Les options facultatives de fournisseur suivantes sont disponibles pour les modèles de conversation xAI :

- **raisonningEffort** _'faible' | 'moyen' | 'élevé'_

  Effort de raisonnement pour les modèles de raisonnement. Par défaut, il est fixé à `moyen`. Si vous utilisez les options `providerOptions` pour définir l'option `raisonningEffort`, ce paramètre de modèle sera ignoré.

## Capacités du Modèle

| Modèle                | Entrée d'Image         | Génération d'Objet   | Utilisation d'Outil          | Streaming d'Outil      |
| -------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `grok-3`             | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-3-fast`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-3-mini`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-3-mini-fast`   | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-2-1212`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-2-vision-1212` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-beta`          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `grok-vision-beta`   | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter les [docs xAI](https://docs.x.ai/docs)

# Modèles) pour une liste complète des modèles disponibles. La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID du modèle de fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

## Modèles d'images

Vous pouvez créer des modèles d'images xAI à l'aide de la méthode de fabrication `.imageModel()`. Pour plus d'informations sur la génération d'images avec le kit de développement logiciel AI, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { xai } from '@ai-sdk/xai';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: xai.image('grok-2-image'),
  prompt: 'Une ville futuriste au coucher du soleil',
});
```

<Note>
  Le modèle d'image xAI ne prend pas actuellement en charge les paramètres `aspectRatio` ou `size`.
  La taille de l'image par défaut est de 1024x768.
</Note>

### Options spécifiques au modèle

Vous pouvez personnaliser le comportement de génération d'images avec des paramètres spécifiques au modèle :

```ts
import { xai } from '@ai-sdk/xai';
import { experimental_generateImage as generateImage } from 'ai';

const { images } = await generateImage({
  model: xai.image('grok-2-image', {
    maxImagesPerCall: 5, // Valeur par défaut : 10
  }),
  prompt: 'Une ville futuriste au coucher du soleil',
  n: 2, // Générer 2 images
});
```

### Capacités du Modèle

| Modèle          | Tailles              | Notes                                                                                                                                                                                                    |
| -------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grok-2-image` | 1024x768 (par défaut) | Le modèle de génération d'image texte-image de xAI, conçu pour créer des images de haute qualité à partir de prompts texte. Il est entraîné sur un ensemble de données divers et peut générer des images dans divers styles, sujets et environnements. |

---
titre : Vercel
description : Apprenez à utiliser les modèles Vercel v0 avec le SDK AI.
---

# Fournisseur Vercel

Le [fournisseur Vercel](https://vercel.com) vous donne accès à l'[API v0](https://vercel.com/docs/v0/api), conçue pour la construction d'applications web modernes. Le modèle `v0-1.0-md` prend en charge les entrées de texte et d'image et fournit des réponses de streaming rapides.

Vous pouvez créer votre clé API Vercel sur [v0.dev](https://v0.dev/chat/settings/keys).

<Note>
  L'API v0 est actuellement en bêta et nécessite un plan Premium ou Team avec la facturation basée sur l'utilisation activée. Pour plus de détails, visitez la [page de tarification](https://v0.dev/pricing). Pour demander une limite supérieure, contactez Vercel à l'adresse support@v0.dev.
</Note>

## Fonctionnalités

- **Complétions conscientes des frameworks** : Évaluées sur des piles modernes comme Next.js et Vercel
- **Auto-réparation** : Identifie et corrige les problèmes de codage courants pendant la génération
- **Édition rapide** : Flux de modifications en ligne en temps réel
- **Compatibilité OpenAI** : Peut être utilisée avec tout outil ou SDK qui prend en charge le format d'API d'OpenAI
- **Multimodal** : Prend en charge les entrées de texte et d'image

## Configuration

Le fournisseur Vercel est disponible via le module `@ai-sdk/vercel`. Vous pouvez l'installer avec :

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `vercel` à partir de `@ai-sdk/vercel` :

```ts
import { vercel } from '@ai-sdk/vercel';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createVercel` à partir de `@ai-sdk/vercel` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createVercel } from '@ai-sdk/vercel';

const vercel = createVercel({
  apiKey: process.env.VERCEL_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Vercel :

- **baseURL** _chaîne_

  Utilisez une adresse URL de prefixe différente pour les appels API. Le prefixe par défaut est `https://api.v0.dev/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. Il prend par défaut la valeur de la variable d'environnement `VERCEL_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de la fonction [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). La valeur par défaut est la fonction `fetch` globale. Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes, ou pour fournir une implémentation de fetch personnalisée pour des tests, par exemple.

## Modèles de Langue

Vous pouvez créer des modèles de langue à l'aide d'une instance de fournisseur. Le premier argument est l'ID du modèle, par exemple :

```ts
import { vercel } from '@ai-sdk/vercel';
import { generateText } from 'ai';

const { text } = await generateText({
  model: vercel('v0-1.0-md'),
  prompt: 'Créer un chatbot AI Next.js',
});
```

Les modèles de langage Vercel peuvent également être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

## Exemple avec AI SDK

```ts
import { generateText } from 'ai';
import { createVercel } from '@ai-sdk/vercel';

const vercel = createVercel({
  baseURL: 'https://api.v0.dev/v1',
  apiKey: process.env.VERCEL_API_KEY,
});

const { text } = await generateText({
  model: vercel('v0-1.0-md'),
  prompt: 'Créer un chatbot AI Next.js avec une authentication',
});
```

## Modèles

### v0-1.0-md

Le modèle `v0-1.0-md` est le modèle par défaut servi par l'API v0.

Capacités :

- Supporte les entrées de texte et d'image (multimodal)
- Supporte les appels de fonctions/outils
- Réponses en flux avec une faible latence
- Optimisé pour le développement web frontend et full-stack

## Capacités du Modèle

| Modèle        | Entrée d'Image         | Génération d'Objet   | Utilisation d'Outil          | Flux d'Outil      |
| ------------- | -------------------- | -------------------- | ---------------------------- | ----------------- |
| `v0-1.0-md`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titre: OpenAI
description: Découvrez comment utiliser le fournisseur OpenAI pour le SDK AI.
---

# Fournisseur OpenAI

Le [fournisseur OpenAI](https://openai.com/) contient un support de modèle de langage pour les API de réponse, de conversation et de complétion OpenAI, ainsi qu'un support de modèle d'embedding pour l'API d'embedding OpenAI.

## Configuration

Le fournisseur OpenAI est disponible dans le module `@ai-sdk/openai`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `openai` à partir de `@ai-sdk/openai` :

```ts
import { openai } from '@ai-sdk/openai';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createOpenAI` à partir de `@ai-sdk/openai` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createOpenAI } from '@ai-sdk/openai';

const openai = createOpenAI({
  // paramètres personnalisés, par exemple
  compatibility: 'strict', // mode strict, activer lors de l'utilisation de l'API OpenAI
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur OpenAI :

- **baseURL** _chaîne_

  Utilisez une URL de prefixage différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  La valeur par défaut est `https://api.openai.com/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  La valeur par défaut est la variable d'environnement `OPENAI_API_KEY`.

- **name** _chaîne_

  Le nom du fournisseur. Vous pouvez définir cela lors de l'utilisation de fournisseurs OpenAI compatibles
  pour changer la propriété du modèle du fournisseur. La valeur par défaut est `openai`.

- **organization** _chaîne_

  Organisation OpenAI.

- **project** _chaîne_

  Projet OpenAI.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  La valeur par défaut est la fonction globale `fetch`.
  Vous pouvez l'utiliser en tant que middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour des tests par exemple.

- **compatibility** _"strict" | "compatible"_

Mode de compatibilité avec OpenAI. Doit être défini sur `strict` lors de l'utilisation de l'API OpenAI,
  et `compatible` lors de l'utilisation de fournisseurs tiers. Dans le mode `compatible`, les informations plus récentes telles que `streamOptions` ne sont pas envoyées, ce qui entraîne une utilisation de jetons `NaN`. Par défaut, il est défini sur 'compatible'.

## Modèles de Langage

L'instance du fournisseur OpenAI est une fonction que vous pouvez invoquer pour créer un modèle de langage :

```ts
const model = openai('gpt-4-turbo');
```

Elle sélectionne automatiquement l'API correcte en fonction de l'identifiant du modèle.
Vous pouvez également passer des paramètres supplémentaires en deuxième argument :

```ts
const model = openai('gpt-4-turbo', {
  // paramètres supplémentaires
});
```

Les options disponibles dépendent de l'API qui est automatiquement choisie pour le modèle (voir ci-dessous).
Si vous souhaitez sélectionner explicitement une API spécifique pour un modèle, vous pouvez utiliser `.chat` ou `.completion`.

### Exemple

Vous pouvez utiliser les modèles de langage OpenAI pour générer du texte avec la fonction `generateText` :

```ts
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage OpenAI peuvent également être utilisés dans les fonctions `streamText`, `generateObject`, et `streamObject` (voir [Core de l'API AI](/docs/ai-sdk-core)).

### Modèles de Chat

Vous pouvez créer des modèles qui appellent l'[API de chat OpenAI](https://platform.openai.com/docs/api-reference/chat) en utilisant la méthode de fabrication `.chat()`.
La première argument est l'identifiant du modèle, par exemple `gpt-4`.
Les modèles de chat OpenAI supportent les appels d'outil et certains ont des capacités multi-modales.

```ts
const model = openai.chat('gpt-3.5-turbo');
```

Les modèles de chat OpenAI supportent également certaines paramètres spécifiques au modèle qui ne font pas partie des [paramètres de l'appel standard](/docs/ai-sdk-core/settings).
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = openai.chat('gpt-3.5-turbo', {
  logitBias: {
    // likelihood optionnelle pour des jetons spécifiques
    '50256': -100,
  },
  user: 'test-user', // identifiant d'utilisateur unique optionnel
});
```

Les paramètres optionnels suivants sont disponibles pour les modèles de chat OpenAI :

- **logitBias** _Record&lt;nombre, nombre&gt;_

  Modifie la probabilité de sélection de jetons spécifiques dans la réponse.

  Accepte un objet JSON qui associe les jetons (spécifiés par leur ID de jeton dans le tokenizeur GPT) à une valeur de biais associée comprise entre -100 et 100. Vous pouvez utiliser cet outil de tokenizeur pour convertir le texte en ID de jeton. Mathématiquement, le biais est ajouté aux logits générés par le modèle avant l'échantillonnage. L'effet exact variera en fonction du modèle, mais les valeurs comprises entre -1 et 1 devraient diminuer ou augmenter la probabilité de sélection ; des valeurs comme -100 ou 100 devraient entraîner une sélection exclusive ou une interdiction du jeton pertinent.

  Par exemple, vous pouvez passer `{"50256": -100}` pour empêcher le jeton de être généré.

- **logprobs** _booléen | nombre_

  Retourne les probabilités logarithmiques des jetons. Inclure logprobs augmentera la taille de la réponse et peut ralentir les temps de réponse. Cependant, cela peut être utile pour mieux comprendre le comportement du modèle.

  Définir à true retournera les probabilités logarithmiques des jetons qui ont été générés.

- **Définir à un nombre** *retourne les probabilités logarithmiques des n premiers tokens générés.*

- **parallelToolCalls** _boolean_

  Activer ou non l'appel parallèle des fonctions lors de l'utilisation des outils. Valeur par défaut : `true`.

- **useLegacyFunctionCalls** _boolean_

  Utiliser l'appel de fonctions legacy. Valeur par défaut : `false`.

  Requis par certains moteurs d'inference open source qui ne supportent pas l'API `tools`. Il peut également fournir un moyen de contourner l'appel parallèle des outils, qui cause le fournisseur à stocker les appels d'outils, ce qui rend `streamObject` non en flux.

  Préférez définir `parallelToolCalls : false` plutôt que cette option.

- **structuredOutputs** _boolean_

  Utiliser [les sorties structurées](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concepts/output-of-azure-computer-vision-model)

# Sorties structurées).
  Par défaut, il est défini sur `false` pour les modèles normaux, et `true` pour les modèles de raisonnement.

  Lorsqu'il est activé, les appels d'outil et la génération d'objets seront stricts et suivront le schéma fourni.

- **utilisateur** _chaîne de caractères_

  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à surveiller et détecter les abus. [En savoir plus](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

- **téléchargerImages** _booléen_

  Télécharge automatiquement les images et passe l'image comme données au modèle.
  OpenAI prend en charge les URL d'images pour les modèles publics, il n'est donc nécessaire que pour les modèles privés ou lorsque les images ne sont pas accessibles publiquement.
  Par défaut, il est défini sur `false`.

- **simulerFlux** _booléen_

  Simule un flux en utilisant une appelle de génération normale et en le renvoyant sous forme de flux.
  Activez cela si le modèle que vous utilisez ne prend pas en charge le flux.
  Par défaut, il est défini sur `false`.

- **effortDeRaisonnement** _'faible' | 'moyen' | 'élevé'_

  Effort de raisonnement pour les modèles de raisonnement. Par défaut, il est défini sur `moyen`. Si vous utilisez `providerOptions` pour définir l'option `reasoningEffort`, cette configuration du modèle sera ignorée.

#### Raisonnement

OpenAI a introduit la série de modèles de raisonnement `o1`, `o3` et `o4` ([modèles de raisonnement](https://platform.openai.com/docs/guides/reasoning)).
Actuellement, `o4-mini`, `o3`, `o3-mini`, `o1`, `o1-mini` et `o1-preview` sont disponibles.

Les modèles de raisonnement génèrent actuellement uniquement du texte, ont plusieurs limitations et ne sont pris en charge que via `generateText` et `streamText`.

Ils prennent en charge des paramètres supplémentaires et des métadonnées de réponse :

- Vous pouvez utiliser `providerOptions` pour définir

  - l'option `reasoningEffort` (ou l'option de modèle `reasoningEffort`), qui détermine la quantité de raisonnement effectué par le modèle.

- Vous pouvez utiliser les métadonnées de réponse `providerMetadata` pour accéder au nombre de jetons de raisonnement générés par le modèle.

```ts highlight="4,7-11,17"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text, usage, providerMetadata } = await generateText({
  model: openai('o3-mini'),
  prompt: 'Inventez un nouveau jour férié et décrivez ses traditions.',
  providerOptions: {
    openai: {
      reasoningEffort: 'faible',
    },
  },
});

console.log(text);
console.log('Utilisation:', {
  ...usage,
  jetonsDeRaisonnement: providerMetadata?.openai?.reasoningTokens,
});
```

<Note>
  Les messages du système sont automatiquement convertis en messages du développeur OpenAI pour les modèles de raisonnement lorsqu'ils sont pris en charge. Pour les modèles qui ne prennent pas en charge les messages du développeur, tels que `o1-preview`, les messages du système sont supprimés et un avertissement est ajouté.
</Note>

<Note>
  Les modèles de raisonnement comme `o1-mini` et `o1-preview` nécessitent une inférence runtime supplémentaire pour terminer leur phase de raisonnement avant de générer une réponse. Cela introduit une latence plus longue par rapport à d'autres modèles, avec `o1-preview` présentant une inférence significativement plus longue que `o1-mini`.
</Note>

<Note>
  `maxTokens` est automatiquement mappé à `max_completion_tokens` pour les modèles de raisonnement.
</Note>

#### Sorties Structurées

Vous pouvez activer les [sorties structurées d'OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/) en définissant l'option `structuredOutputs` sur `true`.
Les sorties structurées sont une forme de génération guidée par la grammaire.
Le schéma JSON est utilisé comme grammaire et les sorties se conformeront toujours au schéma.

```ts highlight="7"
import { openai } from '@ai-sdk/openai';
import { generateObject } from 'ai';
import { z } from 'zod';

const result = await generateObject({
  model: openai('gpt-4o-2024-08-06', {
    structuredOutputs: true,
  }),
  schemaName: 'recipe',
  schemaDescription: 'Une recette de lasagna.',
  schema: z.object({
    name: z.string(),
    ingredients: z.array(
      z.object({
        name: z.string(),
        amount: z.string(),
      }),
    ),
    steps: z.array(z.string()),
  }),
  prompt: 'Générez une recette de lasagna.',
});

console.log(JSON.stringify(result.object, null, 2));
```

<Note type="warning">
 Les sorties structurées d'OpenAI ont plusieurs
 [limites](https://openai.com/index/introducing-structured-outputs-in-the-api),
 en particulier autour des [schémas pris en charge](https://platform.openai.com/docs/guides/structured-outputs/supported-schemas),
 et sont donc optionnelles.

Par exemple, les propriétés de schéma facultatives ne sont pas prises en charge.
Vous devez modifier Zod `.nullish()` et `.optional()` en `.nullable()`.

</Note>

#### Support de PDF

L'API Chat OpenAI prend en charge la lecture des fichiers PDF.
Vous pouvez passer des fichiers PDF en tant que contenu du message en utilisant le type `file` :

```ts
const result = await generateText({
  model: openai('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: 'Qu'est-ce qu\'un modèle d\'embedding ?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
          filename: 'ai.pdf', // facultatif
        },
      ],
    },
  ],
});
```

Le modèle aura accès au contenu du fichier PDF et répondra aux questions à ce sujet.
Le fichier PDF doit être passé en utilisant le champ `data`, et le `mimeType` doit être défini sur `'application/pdf'`.

#### Sorties Prédites

OpenAI prend en charge les [sorties prédites](https://platform.openai.com/docs/guides/latency-optimization)

# Utiliser les sorties prédites) pour `gpt-4o` et `gpt-4o-mini`.
Les sorties prédites vous aident à réduire la latence en vous permettant de spécifier un texte de base que le modèle devrait modifier.
Vous pouvez activer les sorties prédites en ajoutant l'option `prediction` à l'objet `providerOptions.openai` :

```ts highlight="15-18"
const result = streamText({
  model: openai('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: 'Remplacez la propriété Username par une propriété Email.',
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

OpenAI fournit des informations sur l'utilisation des sorties prédites (`acceptedPredictionTokens` et `rejectedPredictionTokens`).
Vous pouvez y accéder dans l'objet `providerMetadata`.

```ts highlight="11"
const openaiMetadata = (await result.providerMetadata)?.openai;

const acceptedPredictionTokens = openaiMetadata?.acceptedPredictionTokens;
const rejectedPredictionTokens = openaiMetadata?.rejectedPredictionTokens;
```

<Note type="warning">
  Les sorties prédites d'OpenAI ont plusieurs
  [limites](https://platform.openai.com/docs/guides/predicted-outputs#limitations),
  par exemple des paramètres API non pris en charge et pas de support pour les appels de l'outil.
</Note>

#### Détail de l'image

Vous pouvez utiliser l'option `openai` du fournisseur pour définir le [détail d'entrée d'image](https://platform.openai.com/docs/guides/images-vision?api-mode=responses

# Spécifier le niveau de détail de l'entrée d'image à `élevé`, `faible` ou `auto` :

```ts highlight="13-16"
const result = await generateText({
  model: openai('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Décrivez l\'image en détail.' },
        {
          type: 'image',
          image:
            'https://github.com/vercel/ai/blob/main/examples/ai-core/data/comic-cat.png?raw=true',

          // Options spécifiques à OpenAI - détail de l\'image :
          providerOptions: {
            openai: { imageDetail: 'low' },
          },
        },
      ],
    },
  ],
});
```

<Note type="warning">
  Puisque le type `UIMessage` (utilisé par les hooks UI SDK AI comme `useChat`) ne prend pas en charge la propriété `providerOptions`, vous pouvez utiliser `convertToCoreMessages` avant de passer les messages aux fonctions comme `generateText` ou `streamText`. Pour plus de détails sur l'utilisation de `providerOptions`, voir [ici](/docs/foundations/prompts#provider-options).
</Note>

#### Distillation

OpenAI supporte la distillation de modèle pour certains modèles.
Si vous souhaitez stocker une génération pour l'utiliser dans le processus de distillation, vous pouvez ajouter l'option `store` à l'objet `providerOptions.openai`.

Cela sauvegardera la génération sur la plateforme OpenAI pour une utilisation ultérieure dans la distillation.

```typescript highlight="9-16"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';
import 'dotenv/config';

async function main() {
  const { text, usage } = await generateText({
    model: openai('gpt-4o-mini'),
    prompt: 'Qui a travaillé sur l\'ordinateur Macintosh original ?',
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
  console.log('Utilisation:', usage);
}

main().catch(console.error);
```

#### Caching de Prompt

OpenAI a introduit [Caching de Prompt](https://platform.openai.com/docs/guides/prompt-caching) pour les modèles pris en charge,
y compris `gpt-4o`, `gpt-4o-mini`, `o1-preview`, et `o1-mini`.

- Le caching de prompt est automatiquement activé pour ces modèles, lorsque la longueur du prompt dépasse 1024 tokens. Il n'est
  pas nécessaire de l'activer explicitement.
- Vous pouvez utiliser les métadonnées de réponse `providerMetadata` pour accéder au nombre de tokens de prompt qui ont été un
  cache hit.
- Notez que le comportement de caching dépend de la charge sur l'infrastructure d'OpenAI. Les préfixes de prompt restent généralement
  dans le cache pendant 5-10 minutes d'inactivité avant d'être évacués, mais pendant les périodes hors pointe, ils peuvent persister
  pendant une heure.

```ts highlight="11"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const { text, usage, providerMetadata } = await generateText({
  model: openai('gpt-4o-mini'),
  prompt: `Un prompt de 1024 tokens ou plus long...`,
});

console.log(`usage:`, {
  ...usage,
  cachedPromptTokens: providerMetadata?.openai?.cachedPromptTokens,
});
```

#### Entrée Audio

Avec le modèle `gpt-4o-audio-preview`, vous pouvez passer des fichiers audio au modèle.

<Note type="warning">
  Le modèle `gpt-4o-audio-preview` est actuellement en préversion et nécessite au moins
  quelques entrées audio. Il ne fonctionnera pas avec des données non audio.
</Note>

```ts highlight="12-14"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const result = await generateText({
  model: openai('gpt-4o-audio-preview'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Qu'est-ce que l\'audio dit ?' },
        {
          type: 'file',
          mimeType: 'audio/mpeg',
          data: fs.readFileSync('./data/galileo.mp3'),
        },
      ],
    },
  ],
});
```

### Modèles de Réponses

Vous pouvez utiliser l'API de réponses OpenAI avec la méthode de fabrication `openai.responses(modelId)`.

```ts
const model = openai.responses('gpt-4o-mini');
```

Une configuration supplémentaire peut être effectuée en utilisant les options du fournisseur OpenAI.
Vous pouvez valider les options du fournisseur en utilisant le type `OpenAIResponsesProviderOptions`.

```ts
import { openai, OpenAIResponsesProviderOptions } from '@ai-sdk/openai';
import { generateText } from 'ai';

const result = await generateText({
  model: openai.responses('gpt-4o-mini'),
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

Les options de fournisseur suivantes sont disponibles :

- **parallelToolCalls** _boolean_
  Utiliser des appels parallèles des outils. Par défaut à `true`.

- **store** _boolean_
  Stocker la génération. Par défaut à `true`.

- **metadata** _Record&lt;string, string&gt;_
  Métadonnées supplémentaires à stocker avec la génération.

- **previousResponseId** _string_
  L'ID de la réponse précédente. Vous pouvez l'utiliser pour continuer une conversation. Par défaut à `undefined`.

- **instructions** _string_
  Instructions pour le modèle.
  Elles peuvent être utilisées pour changer le message du système ou du développeur lors de la poursuite d'une conversation en utilisant l'option `previousResponseId`.
  Par défaut à `undefined`.

- **user** _string_
  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à surveiller et détecter les abus. Par défaut à `undefined`.

- **effortDeRaisonnement** _'faible' | 'moyen' | 'fort'_
  Effort de raisonnement pour les modèles de raisonnement. Par défaut, il est défini sur `moyen`. Si vous utilisez `providerOptions` pour définir l'option `reasoningEffort`, ce paramètre de modèle sera ignoré.

- **résuméDeRaisonnement** _'auto' | 'détail'_
  Contrôle si le modèle retourne son processus de raisonnement. Défini sur `'auto'` pour un résumé condensé, `'détail'` pour une raison plus complète. Par défaut, il est défini sur `undefined` (aucun résumé de raisonnement). Lorsqu'il est activé, les résumés de raisonnement apparaissent dans la flux comme des événements de type `'reasoning'` et dans les réponses non-flux dans le champ `reasoning`.

- **schémasStricte** _boolean_
  Utiliser des schémas JSON stricts dans les outils et lors de la génération de sorties JSON. Par défaut, il est défini sur `true`.

Le fournisseur de réponses OpenAI retourne également des métadonnées spécifiques au fournisseur :

```ts
const { providerMetadata } = await generateText({
  model: openai.responses('gpt-4o-mini'),
});

const openaiMetadata = providerMetadata?.openai;
```

Les métadonnées spécifiques à OpenAI suivantes sont retournées :

- **idDeRéponse** _chaîne de caractères_
  L'ID de la réponse. Peut être utilisé pour continuer une conversation.

- **tokensDePromptCachés** _nombre_
  Le nombre de tokens de prompt qui ont été un hit de cache.

- **tokensDeRaisonnement** _nombre_
  Le nombre de tokens de raisonnement que le modèle a générés.

#### Recherche Web

Le fournisseur de réponses OpenAI prend en charge la recherche web à travers l'outil `openai.tools.webSearchPreview`.

Vous pouvez forcer l'utilisation de l'outil de recherche web en définissant le paramètre `toolChoice` sur `{ type: 'tool', toolName: 'web_search_preview' }`.

```ts
const result = await generateText({
  model: openai.responses('gpt-4o-mini'),
  prompt: 'Qu'est-ce qui s'est passé à San Francisco la semaine dernière ?',
  tools: {
    web_search_preview: openai.tools.webSearchPreview({
      // configuration optionnelle :
      searchContextSize: 'high',
      userLocation: {
        type: 'approximatif',
        ville: 'San Francisco',
        région: 'Californie',
      },
    }),
  },
  // Forcer l'outil de recherche web :
  toolChoice: { type: 'tool', toolName: 'web_search_preview' },
});

// Sources URL
const sources = result.sources;
```

#### Résumés de raisonnement

Pour les modèles de raisonnement comme `o3-mini`, `o3` et `o4-mini`, vous pouvez activer les résumés de raisonnement pour voir le processus de pensée du modèle. Les différents modèles supportent différents résumés—for example, `o4-mini` supporte des résumés détaillés. Définissez `reasoningSummary: "auto"` pour recevoir automatiquement le niveau le plus riche disponible.

```ts highlight="8-9,16"
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

const result = streamText({
  model: openai.responses('o4-mini'),
  prompt: 'M'expliquez le débat sur le Mission burrito à San Francisco.',
  providerOptions: {
    openai: {
      reasoningSummary: 'détail', // 'auto' pour condensé ou 'détail' pour complet
    },
  },
});

for await (const part of result.fullStream) {
  if (part.type === 'raisonnement') {
    console.log(`Raisonnement : ${part.textDelta}`);
  } else if (part.type === 'text-delta') {
    process.stdout.write(part.textDelta);
  }
}
```

Pour les appels non en flux avec `generateText`, les résumés de raisonnement sont disponibles dans le champ `raisonnement` de la réponse :

```ts highlight="8-9,13"
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const result = await generateText({
  model: openai.responses('o3-mini'),
  prompt: 'M'expliquez le débat sur le Mission burrito à San Francisco.',
  providerOptions: {
    openai: {
      reasoningSummary: 'auto',
    },
  },
});
console.log('Raisonnement:', result.reasoning);
```

En savoir plus sur les résumés de raisonnement dans la [documentation OpenAI](https://platform.openai.com/docs/guides/reasoning?api-mode=responses

# Résumés-de-réflexion).

#### Support de PDF

L'API de réponses OpenAI prend en charge la lecture de fichiers PDF.
Vous pouvez passer des fichiers PDF en tant que contenu de message en utilisant le type `file` :

```ts
const result = await generateText({
  model: openai.responses('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: 'Qu'est-ce qu'un modèle d'embedding ?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
          filename: 'ai.pdf', // facultatif
        },
      ],
    },
  ],
});
```

Le modèle aura accès au contenu du fichier PDF et répondra aux questions à son sujet.
Le fichier PDF doit être passé en utilisant le champ `data`, et le `mimeType` doit être défini sur `'application/pdf'`.

#### Sorties Structurées

L'API de Réponses OpenAI prend en charge les sorties structurées. Vous pouvez forcer les sorties structurées en utilisant `generateObject` ou `streamObject`, qui exposent une option `schema`. De plus, vous pouvez passer un objet Zod ou JSON Schema à l'option `experimental_output` lors de l'utilisation de `generateText` ou `streamText`.

```ts
// En utilisant generateObject
const result = await generateObject({
  model: openai.responses('gpt-4.1'),
  schema: z.object({
    recette: z.object({
      nom: z.string(),
      ingrédients: z.array(
        z.object({
          nom: z.string(),
          quantité: z.string(),
        }),
      ),
      étapes: z.array(z.string()),
    }),
  }),
  prompt: 'Générez une recette de lasagna.',
});

// En utilisant generateText
const result = await generateText({
  model: openai.responses('gpt-4.1'),
  prompt: 'Comment faire une pizza?',
  experimental_output: Output.object({
    schema: z.object({
      ingrédients: z.array(z.string()),
      étapes: z.array(z.string()),
    }),
  }),
});
```

### Modèles de complétion

Vous pouvez créer des modèles qui appellent l'[API de complétion OpenAI](https://platform.openai.com/docs/api-reference/completions) à l'aide de la méthode de fabrication `.completion()`.
Le premier argument est l'identifiant du modèle.
Actuellement, seul `gpt-3.5-turbo-instruct` est pris en charge.

```ts
const model = openai.completion('gpt-3.5-turbo-instruct');
```

Les modèles de complétion OpenAI prennent également en charge certaines paramètres spécifiques au modèle qui ne font pas partie des [paramètres de l'appel standard](/docs/ai-sdk-core/settings).
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = openai.completion('gpt-3.5-turbo-instruct', {
  echo: true, // optionnel, écho du prompt en plus de la complétion
  logitBias: {
    // optionnel, probabilité de spécifier des jetons
    '50256': -100,
  },
  suffix: 'quelques textes', // optionnel, suffixe qui vient après une complétion de texte inséré
  user: 'test-user', // optionnel, identifiant d'utilisateur unique
});
```

Les paramètres optionnels suivants sont disponibles pour les modèles de complétion OpenAI :

- **echo** _booléen_

  Écho du prompt en plus de la complétion.

- **logitBias** _Record&lt;number, number&gt;_

  Modifie la probabilité de spécifier des jetons dans la complétion.

  Accepte un objet JSON qui associe des jetons (spécifiés par leur ID de jeton dans le tokenizeur GPT) à une valeur de biais associée comprise entre -100 et 100. Vous pouvez utiliser cet outil de tokenizeur pour convertir du texte en ID de jeton. Mathématiquement, le biais est ajouté aux logits générés par le modèle avant l'échantillonnage.
  L'effet exact variera par modèle, mais les valeurs comprises entre -1 et 1 devraient diminuer ou augmenter la probabilité de sélection ; les valeurs comme -100 ou 100 devraient entraîner un bannissement ou une sélection exclusive du jeton pertinent.

  Par exemple, vous pouvez passer `{"50256": -100}` pour empêcher le jeton `<|endoftext|>` d'être généré.

- **logprobs** _booléen | nombre_

Renvoyez les probabilités logiques des tokens. Inclure les logprobs augmente la taille de la réponse et peut ralentir les temps de réponse. Cependant, cela peut être utile pour mieux comprendre le comportement du modèle.

  Définir à true renvoie les probabilités logiques des tokens qui ont été générés.

  Définir à un nombre renvoie les probabilités logiques des n premiers tokens qui ont été générés.

- **suffix** _chaîne de caractères_

  L'extension qui suit une complétion d'insertion de texte.

- **user** _chaîne de caractères_

  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à surveiller et détecter les abus. [En savoir plus](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

### Capacités du Modèle

### Description

| Modèle                  | Entrée d'image         | Entrée audio         | Génération d'objet   | Utilisation de l'outil          |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `gpt-4.1`              | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4.1-mini`         | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4.1-nano`         | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o`               | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-mini`          | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-audio-preview` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4-turbo`          | <Check size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4`                | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `gpt-3.5-turbo`        | <Croix size={18} /> | <Croix size={18} /> | <Coche size={18} /> | <Coche size={18} /> |
| `o1`                   | <Coche size={18} /> | <Croix size={18} /> | <Coche size={18} /> | <Coche size={18} /> |
| `o1-mini`              | <Coche size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `o1-preview`           | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `o3-mini`              | <Croix size={18} /> | <Croix size={18} /> | <Coche size={18} /> | <Coche size={18} /> |
| `o3`                   | <Coche size={18} /> | <Croix size={18} /> | <Coche size={18} /> | <Coche size={18} /> |
| `o4-mini`              | <Coche size={18} /> | <Croix size={18} /> | <Coche size={18} /> | <Coche size={18} /> |
| `chatgpt-4o-latest`    | <Coche size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter la [documentation OpenAI](https://platform.openai.com/docs/models) pour une liste complète des modèles disponibles. La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID du modèle d'un fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

## Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'[API d'embeddings d'OpenAI](https://platform.openai.com/docs/api-reference/embeddings) 
à l'aide de la méthode de fabrication `.embedding()`.

```ts
const model = openai.embedding('text-embedding-3-large');
```

Les modèles d'embeddings d'OpenAI prennent en charge plusieurs paramètres supplémentaires.
Vous pouvez les passer en tant qu'argument d'option :

```ts
const model = openai.embedding('text-embedding-3-large', {
  dimensions: 512 // optionnel, nombre de dimensions pour l'embedding
  user: 'test-user' // identifiant d'utilisateur unique optionnel
})
```

Les paramètres facultatifs suivants sont disponibles pour les modèles d'embeddings d'OpenAI :

- **dimensions** : _nombre_

  Le nombre de dimensions que les embeddings de sortie résultants devraient avoir.
  Seul pris en charge dans les modèles `text-embedding-3` et ultérieurs.

- **user** _chaîne de caractères_

  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à 
  surveiller et détecter les abus. [En savoir plus](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

### Capacités des Modèles

| Modèle                    | Dimensions Par Défaut | Dimensions Customisées   |
| ------------------------ | ------------------ | ------------------------- |
| `text-embedding-3-large` | 3072               | <Check size={18} />       |
| `text-embedding-3-small` | 1536               | <Check size={18} />       |
| `text-embedding-ada-002` | 1536               | <Cross size={18} />       |

## Modèles d'Images

Vous pouvez créer des modèles qui appellent l'[API de génération d'images OpenAI](https://platform.openai.com/docs/api-reference/images)
en utilisant la méthode de fabrication `.image()`.

```ts
const model = openai.image('dall-e-3');
```

<Note>
 Les modèles Dall-E ne supportent pas le paramètre `aspectRatio`. Utilisez le paramètre `size` à la place.
</Note>

### Capabilités du Modèle

| Modèle         | Tailles                           |
| ------------- | ------------------------------- |
| `gpt-image-1` | 1024x1024, 1536x1024, 1024x1536 |
| `dall-e-3`    | 1024x1024, 1792x1024, 1024x1792 |
| `dall-e-2`    | 256x256, 512x512, 1024x1024     |

Vous pouvez passer des options `providerOptions` facultatives au modèle d'image. Ces options sont sujettes à changement par OpenAI et sont dépendantes du modèle. Par exemple, le modèle `gpt-image-1` prend en charge l'option `quality` :

```ts
const { image } = await generateImage({
  model: openai.image('gpt-image-1'),
  prompt: 'Un triton au lever du soleil dans un étang forestier aux Seychelles.',
  providerOptions: {
    openai: { quality: 'high' },
  },
});
```

Pour plus d'informations sur `generateImage()` voir [Génération d'images](/docs/ai-sdk-core/image-generation).

Pour plus d'informations sur les options de modèle d'image OpenAI disponibles, voir la [référence de l'API OpenAI](https://platform.openai.com/docs/api-reference/images/create).

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription OpenAI](https://platform.openai.com/docs/api-reference/audio/transcribe)
à l'aide de la méthode de fabrication `.transcription()`.

La première argument est l'identifiant du modèle, par exemple `whisper-1`.

```ts
const model = openai.transcription('whisper-1');
```

Vous pouvez également passer des options spécifiques au fournisseur à l'aide de l'argument `providerOptions`. Par exemple, fournir la langue d'entrée au format ISO-639-1 (par exemple `en`) améliorera l'exactitude et la latence.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: new Uint8Array([1, 2, 3, 4]),
  providerOptions: { openai: { language: 'en' } },
});
```

Les options de fournisseur suivantes sont disponibles :

- **timestampGranularities** _string[]_
  La granularité des horodatages dans la transcription.
  Par défaut, il s'agit de `['segment']`.
  Les valeurs possibles sont `['word']`, `['segment']` et `['word', 'segment']`.
  Remarque : Il n'y a pas de latence supplémentaire pour les horodatages de segment, mais la génération d'horodatages de mot entraîne une latence supplémentaire.

- **language** _string_
  La langue de l'audio d'entrée. Fournir la langue d'entrée au format ISO-639-1 (par exemple 'en') améliorera l'exactitude et la latence.
  Facultatif.

- **prompt** _string_
  Un texte optionnel pour guider le style du modèle ou continuer un segment audio précédent. Le prompt doit correspondre à la langue audio.
  Facultatif.

- **température** _nombre_
  La température d'échantillonnage, comprise entre 0 et 1. Des valeurs plus élevées comme 0,8 feront en sorte que la sortie soit plus aléatoire, tandis que des valeurs plus basses comme 0,2 feront en sorte qu'elle soit plus ciblée et déterministe. Si elle est fixée à 0, le modèle utilisera la probabilité logarithmique pour augmenter automatiquement la température jusqu'à ce que certains seuils soient atteints.
  Défaut : 0.
  Facultatif.

- **inclure** _chaîne[]_
  Informations supplémentaires à inclure dans la réponse de transcription.

### Capacités du Modèle

| Modèle                     | Transcription       | Durée            |Segments            | Langue            |
| ---------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper-1`                  | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-mini-transcribe` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `gpt-4o-transcribe`          | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

## Modèles de parole

Vous pouvez créer des modèles qui appellent l'[API de parole OpenAI](https://platform.openai.com/docs/api-reference/audio/speech)
en utilisant la méthode de fabrication `.speech()`.

La première argument est l'identifiant du modèle par exemple `tts-1`.

```ts
const model = openai.speech('tts-1');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, fournir une voix à utiliser pour l'audio généré.

```ts highlight="6"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Bonjour, monde!',
  providerOptions: { openai: {} },
});
```

- **instructions** _chaîne de caractères_
  Contrôlez la voix de votre audio généré avec des instructions supplémentaires par exemple "Parlez d'une voix lente et régulière".
  Ne fonctionne pas avec `tts-1` ou `tts-1-hd`.
  Facultatif.

- **response_format** _chaîne de caractères_
  Le format de l'audio.
  Les formats pris en charge sont `mp3`, `opus`, `aac`, `flac`, `wav`, et `pcm`.
  Par défaut, `mp3`.
  Facultatif.

- **speed** _nombre_
  La vitesse de l'audio généré.
  Sélectionnez une valeur comprise entre 0,25 et 4,0.
  Par défaut, 1,0.
  Facultatif.

### Capacités du Modèle

| Modèle             | Instructions        |
| ----------------- | ------------------- |
| `tts-1`           | <Check size={18} /> |
| `tts-1-hd`        | <Check size={18} /> |
| `gpt-4o-mini-tts` | <Check size={18} /> |

---
titre : Azure OpenAI
description : Apprenez à utiliser le fournisseur Azure OpenAI pour le SDK AI.
---

# Fournisseur Azure OpenAI

Le [fournisseur Azure OpenAI](https://azure.microsoft.com/fr-fr/products/ai-services/openai-service) contient le support des modèles de langage pour l'API de discussion Azure OpenAI.

## Configuration

Le fournisseur Azure OpenAI est disponible dans le module `@ai-sdk/azure`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `azure` à partir de `@ai-sdk/azure` :

```ts
import { azure } from '@ai-sdk/azure';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createAzure` à partir de `@ai-sdk/azure` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createAzure } from '@ai-sdk/azure';

const azure = createAzure({
  resourceName: 'votre-nom-de-resource', // Nom de la ressource Azure
  apiKey: 'votre-clé-api',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur OpenAI :

- **resourceName** _chaîne_

  Nom de la ressource Azure.
  Il est défini par défaut sur la variable d'environnement `AZURE_RESOURCE_NAME`.

  Le nom de la ressource est utilisé dans l'URL assemblée : `https://{resourceName}.openai.azure.com/openai/deployments/{modelId}{path}`.
  Vous pouvez utiliser `baseURL` à la place pour spécifier le préfixe d'URL.

- **apiKey** _chaîne_

  Clé API qui est envoyée en tant que header `api-key`.
  Il est défini par défaut sur la variable d'environnement `AZURE_API_KEY`.

- **apiVersion** _chaîne_

  Définit une version d'API personnalisée [version d'API](https://learn.microsoft.com/fr-fr/azure/ai-services/openai/api-version-deprecation).
  Défaut à `2024-10-01-preview`.

- **baseURL** _chaîne_

  Utilise un préfixe d'URL différent pour les appels API, par exemple pour utiliser des serveurs proxy.

  Soit ce paramètre ou `resourceName` est utilisé.
  Lorsqu'un `baseURL` est fourni, le `resourceName` est ignoré.

  Avec un `baseURL`, l'URL résolue est `{baseURL}/{modelId}{path}`.

- **headers** _Record&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

Implémentation personnalisée de [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  Par défaut, elle utilise la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour des tests par exemple.

## Modèles de Langue

L'instance du fournisseur Azure OpenAI est une fonction que vous pouvez invoquer pour créer un modèle de langue :

```ts
const model = azure('votre-nom-de-déploiement');
```

Vous devez passer votre nom de déploiement en tant qu'argument de première partie.

### Modèles de Raisonnement

Azure expose la pensée de `DeepSeek-R1` dans le texte généré à l'aide de l'étiquette `<think>`.
Vous pouvez utiliser `extractReasoningMiddleware` pour extraire cette raison et l'exposer en tant que propriété `reasoning` sur le résultat :

```ts
import { azure } from '@ai-sdk/azure';
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const modelAmélioré = wrapLanguageModel({
  model: azure('votre-nom-de-déploiement-deepseek-r1'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Vous pouvez ensuite utiliser ce modèle amélioré dans les fonctions comme `generateText` et `streamText`.

### Exemple

Vous pouvez utiliser les modèles de langue OpenAI pour générer du texte avec la fonction `generateText` :

```ts
import { azure } from '@ai-sdk/azure';
import { generateText } from 'ai';

const { text } = await generateText({
  model: azure('votre-nom-de-déploiement'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langue OpenAI peuvent également être utilisés dans les fonctions `streamText`, `generateObject` et `streamObject` (voir [AI SDK Core](/docs/ai-sdk-core)).

<Note>
  Azure OpenAI envoie des blocs plus importants que OpenAI. Cela peut conduire à la perception
  que la réponse est plus lente. Voir [Résolution des problèmes : Azure OpenAI lent à la mise en flux](/docs/troubleshooting/common-issues/azure-stream-slow)
</Note>

### Options du fournisseur

Lorsque vous utilisez les modèles de langage OpenAI sur Azure, vous pouvez configurer des options spécifiques au fournisseur à l'aide de `providerOptions.openai`. Plus d'informations sur les options de configuration disponibles sont disponibles sur [la page du fournisseur OpenAI](/providers/ai-sdk-providers/openai#modèles-de-langage).

```ts highlight="12-14,22-24"
const messages = [
  {
    role: 'user',
    content: [
      {
        type: 'text',
        text: 'Quel est le capitol de la lune?',
      },
      {
        type: 'image',
        image: 'https://example.com/image.png',
        providerOptions: {
          openai: { imageDetail: 'faible' },
        },
      },
    ],
  },
];

const { text } = await generateText({
  model: azure('votre-nom-de-déploiement'),
  providerOptions: {
    openai: {
      effortDeRaisonnement: 'faible',
    },
  },
});
```

### Modèles de Chat

<Note>
  L'URL pour appeler les modèles de chat Azure sera construite comme suit :
  `https://RESOURCE_NAME.openai.azure.com/openai/deployments/DEPLOYMENT_NAME/chat/completions?api-version=API_VERSION`
</Note>

Les modèles de chat Azure OpenAI prennent également en charge certaines paramètres spécifiques au modèle qui ne font pas partie des [paramètres de l'appel standard](/docs/ai-sdk-core/settings).
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = azure('your-deployment-name', {
  logitBias: {
    // likelihood optionnelle pour des tokens spécifiques
    '50256': -100,
  },
  user: 'test-user', // identifiant d'utilisateur unique facultatif
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles de chat OpenAI :

- **logitBias** _Record&lt;number, number&gt;_

  Modifie la probabilité de spécifier des tokens apparaissant dans la fin de la phrase.

  Accepte un objet JSON qui mappe des tokens (spécifiés par leur ID de token dans le GPT tokenizer) à une valeur de biais associée comprise entre -100 et 100. Vous pouvez utiliser cet outil de tokenizer pour convertir du texte en ID de token. Mathématiquement, le biais est ajouté aux logits générés par le modèle avant l'échantillonnage. L'effet exact variera par modèle, mais les valeurs comprises entre -1 et 1 devraient diminuer ou augmenter la probabilité de sélection ; les valeurs comme -100 ou 100 devraient entraîner un bannissement ou une sélection exclusive du token pertinent.

  Par exemple, vous pouvez passer `{"50256": -100}` pour empêcher le token d'être généré.

- **logprobs** _boolean | number_

  Retourne les probabilités logarithmiques des tokens. Inclure logprobs augmentera la taille de la réponse et peut ralentir les temps de réponse. Cependant, cela peut être utile pour mieux comprendre le comportement du modèle.

  Définir à true retournera les probabilités logarithmiques des tokens générés.

  Définir à un nombre retournera les probabilités logarithmiques des n premiers tokens générés.

- **parallelToolCalls** _boolean_

- **user** _chaîne de caractères_

  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à surveiller et détecter les abus. En savoir plus.

### Modèles de Réponses

Vous pouvez utiliser l'API de réponses Azure OpenAI avec la méthode de fabrication `azure.responses(deploymentName)`.

```ts
const model = azure.responses('votre-nom-de-déploiement');
```

Une configuration supplémentaire peut être effectuée en utilisant les options du fournisseur OpenAI.
Vous pouvez valider les options du fournisseur en utilisant le type `OpenAIResponsesProviderOptions`.

```ts
import { azure, OpenAIResponsesProviderOptions } from '@ai-sdk/azure';
import { generateText } from 'ai';

const result = await generateText({
  model: azure.responses('votre-nom-de-déploiement'),
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

Les options du fournisseur suivantes sont disponibles :

- **parallelToolCalls** _boolean_
  Utiliser des appels de outils parallèles. Par défaut à `true`.

- **store** _boolean_
  Stocker la génération. Par défaut à `true`.

- **metadata** _Record&lt;string, string&gt;_
  Métadonnées supplémentaires à stocker avec la génération.

- **previousResponseId** _string_
  L'ID de la réponse précédente. Vous pouvez l'utiliser pour continuer une conversation. Par défaut à `undefined`.

- **instructions** _string_
  Instructions pour le modèle.
  Elles peuvent être utilisées pour changer le message du système ou du développeur lors de la poursuite d'une conversation en utilisant l'option `previousResponseId`.
  Par défaut à `undefined`.

- **user** _string_
  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à surveiller et détecter les abus. Par défaut à `undefined`.

- **effortDeRaisonnement** _'faible' | 'moyen' | 'élevé'_
  Effort de raisonnement pour les modèles de raisonnement. Par défaut, il est défini sur `moyen`. Si vous utilisez `providerOptions` pour définir l'option `effortDeRaisonnement`, ce paramètre de modèle sera ignoré.

- **schémasStrict** _boolean_
  Utiliser des schémas JSON strict dans les outils et lors de la génération de sorties JSON. Par défaut, il est défini sur `true`.

Le fournisseur de réponses Azure OpenAI retourne également des métadonnées spécifiques au fournisseur :

```ts
const { providerMetadata } = await generateText({
  model: azure.responses('your-deployment-name'),
});

const openaiMetadata = providerMetadata?.openai;
```

Les métadonnées spécifiques à OpenAI suivantes sont renvoyées :

- **responseId** _chaîne de caractères_
  L'ID de la réponse. Peut être utilisé pour continuer une conversation.

- **cachedPromptTokens** _nombre_
  Le nombre de jetons de prompt qui ont été un coup de cache.

- **reasoningTokens** _nombre_
  Le nombre de jetons de raisonnement que le modèle a générés.

#### Support de PDF

L'API Azure OpenAI Responses prend en charge la lecture de fichiers PDF.
Vous pouvez passer des fichiers PDF en tant que contenu de message en utilisant le type `file` :

```ts
const result = await generateText({
  model: azure.responses('your-deployment-name'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: 'Qu'est-ce qu'un modèle d'embedding ?',
        },
        {
          type: 'file',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
          filename: 'ai.pdf', // facultatif
        },
      ],
    },
  ],
});
```

Le modèle aura accès au contenu du fichier PDF et répondra aux questions à son sujet.
Le fichier PDF devrait être passé en utilisant le champ `data`, et le `mimeType` devrait être défini sur `'application/pdf'`.

### Modèles de complétion

Vous pouvez créer des modèles qui appellent l'API de complétion en utilisant la méthode de fabrication `.completion()`.
La première argument est l'ID du modèle.
Actuellement, seul `gpt-35-turbo-instruct` est pris en charge.

```ts
const model = azure.completion('votre-déploiement-gpt-35-turbo-instruct');
```

Les modèles de complétion OpenAI prennent également en charge certaines réglages spécifiques au modèle qui ne font pas partie des [paramètres de l'appel standard](/docs/sdk-azure-ai/settings).
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = azure.completion('votre-déploiement-gpt-35-turbo-instruct', {
  echo: true, // optionnel, écho du prompt en plus de la complétion
  logitBias: {
    // optionnel, probabilité de spécifier des jetons
    '50256': -100,
  },
  suffix: 'quelques textes', // optionnel, suffixe qui vient après une complétion de texte inséré
  user: 'test-utilisateur', // optionnel, identifiant d'utilisateur unique
});
```

Les paramètres suivants sont disponibles pour les modèles de complétion Azure OpenAI :

- **echo** _boolean_

  Écho du prompt en plus de la complétion.

- **logitBias** _Record&lt;number, number&gt;_

  Modifie la probabilité de spécifier des jetons dans la complétion.

  Accepte un objet JSON qui cartographie les jetons (spécifiés par leur ID de jeton dans le GPT tokenizer) à une valeur de biais associée comprise entre -100 et 100. Vous pouvez utiliser cet outil de tokenizer pour convertir du texte en ID de jeton. Mathématiquement, le biais est ajouté aux logits générés par le modèle avant l'échantillonnage.
  L'effet exact varie par modèle, mais les valeurs comprises entre -1 et 1 devraient diminuer ou augmenter la probabilité de sélection ; les valeurs comme -100 ou 100 devraient entraîner un bannissement ou une sélection exclusive du jeton pertinent.

  Par exemple, vous pouvez passer `{"50256": -100}` pour empêcher le jeton `<|endoftext|>` d'être généré.

- **logprobs** _boolean | number_

Rendre les probabilités logarithmiques des tokens. Inclure les logprobs augmente la taille des réponses et peut ralentir les temps de réponse. Cependant, cela peut être utile pour mieux comprendre le comportement du modèle.

  Définir à `true` retournera les probabilités logarithmiques des tokens qui ont été générés.

  Définir à un nombre retournera les probabilités logarithmiques des n tokens les plus élevés qui ont été générés.

- **suffix** _chaîne de caractères_

  La suffixe qui suit une complétion de texte inséré.

- **user** _chaîne de caractères_

  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à surveiller et détecter les abus. En savoir plus.

## Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'API de embeddings Azure OpenAI
en utilisant la méthode de fabrication `.embedding()`.

```ts
const model = azure.embedding('votre-déploiement-embedding');
```

Les modèles d'embeddings Azure OpenAI prennent en charge plusieurs paramètres supplémentaires.
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = azure.embedding('votre-déploiement-embedding', {
  dimensions: 512 // optionnel, nombre de dimensions pour l'embedding
  user: 'test-user' // identifiant d'utilisateur unique facultatif
})
```

Les paramètres facultatifs suivants sont disponibles pour les modèles d'embeddings Azure OpenAI :

- **dimensions** _nombre_

  Le nombre de dimensions que les embeddings de sortie résultants devraient avoir.
  Seulement pris en charge dans les modèles text-embedding-3 et ultérieurs.

- **user** _chaîne_

  Un identifiant unique représentant votre utilisateur final, qui peut aider OpenAI à
  surveiller et détecter les abus. En savoir plus.

## Modèles d'Images

Vous pouvez créer des modèles qui appellent l'API de génération d'images Azure OpenAI (DALL-E) en utilisant la méthode de fabrication `.imageModel()`.
Le premier argument est le nom de déploiement pour le modèle DALL-E.

```ts
const model = azure.imageModel('votre-nom-de-déploiement-dalle');
```

Les modèles d'images Azure OpenAI prennent en charge plusieurs paramètres supplémentaires.
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = azure.imageModel('votre-nom-de-déploiement-dalle', {
  user: 'test-user', // identifiant d'utilisateur unique facultatif
  responseFormat: 'url', // 'url' ou 'b64_json', par défaut 'url'
});
```

### Exemple

Vous pouvez utiliser les modèles d'image Azure OpenAI pour générer des images avec la fonction `generateImage` :

```ts
import { azure } from '@ai-sdk/azure';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: azure.imageModel('le-nom-de-votre-déploiement-dalle'),
  prompt: 'Une image photoréaliste d\'un chat astronaute flottant dans l\'espace',
  size: '1024x1024', // '1024x1024', '1792x1024', ou '1024x1792' pour DALL-E 3
});

// image contient l'URL ou les données base64 de l'image générée
console.log(image);
```

### Capabilités du Modèle

Azure OpenAI prend en charge les modèles DALL-E 2 et DALL-E 3 à travers les déploiements. Les capacités dépendent de la version du modèle que votre déploiement utilise :

| Version du Modèle | Tailles                         |
| ------------------ | ----------------------------- |
| DALL-E 3           | 1024x1024, 1792x1024, 1024x1792 |
| DALL-E 2           | 256x256, 512x512, 1024x1024     |

<Note>
  Les modèles DALL-E ne prennent pas en charge le paramètre `aspectRatio`. Utilisez le paramètre `size` à la place.
</Note>

<Note>
  Lors de la création de votre déploiement Azure OpenAI, assurez-vous de définir la version du modèle DALL-E que vous souhaitez utiliser.
</Note>

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'API de transcription Azure OpenAI en utilisant la méthode de fabrication `.transcription()`.

La première argument est l'identifiant du modèle par exemple `whisper-1`.

```ts
const model = azure.transcription('whisper-1');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, en fournissant la langue d'entrée sous la forme ISO-639-1 (par exemple `en`) améliorera l'exactitude et la latence.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { azure } from '@ai-sdk/azure';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: azure.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
  providerOptions: { azure: { language: 'en' } },
});
```

Les options de fournisseur suivantes sont disponibles :

- **timestampGranularities** _string[]_
  La granularité des horodatages dans la transcription.
  Par défaut, `['segment']`.
  Les valeurs possibles sont `['word']`, `['segment']`, et `['word', 'segment']`.
  Remarque : Il n'y a pas de latence supplémentaire pour les horodatages de segment, mais la génération d'horodatages de mot entraîne une latence supplémentaire.

- **language** _string_
  La langue de l'audio d'entrée. Fournir la langue d'entrée sous la forme ISO-639-1 (par exemple 'en') améliorera l'exactitude et la latence.
  Optionnel.

- **prompt** _string_
  Un texte optionnel pour guider le style du modèle ou continuer un segment audio précédent. Le prompt doit correspondre à la langue audio.
  Optionnel.

- **temperature** _number_
  La température d'échantillonnage, comprise entre 0 et 1. Des valeurs plus élevées comme 0,8 feront sortir une sortie plus aléatoire, tandis que des valeurs plus basses comme 0,2 feront sortir une sortie plus focalisée et déterministe. Si défini à 0, le modèle utilisera la probabilité logarithmique pour augmenter automatiquement la température jusqu'à ce que certains seuils soient atteints.
  Par défaut, 0.
  Optionnel.

- **inclure** `_string[]_`
  Informations supplémentaires à inclure dans la réponse de transcription.

### Capacités du Modèle

| Modèle                    | Transcription       | Durée            | Segments            | Langue            |
| ------------------------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper-1`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gpt-4o-mini-transcribe` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `gpt-4o-transcribe`      | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

---
titre : Anthropic
description : Apprenez à utiliser le fournisseur Anthropic pour le SDK AI.
---

# Fournisseur Anthropic

Le [fournisseur Anthropic](https://www.anthropic.com/) contient des fonctionnalités de support pour les modèles de langage de l'[API Messages Anthropic](https://docs.anthropic.com/claude/reference/messages_post).

## Configuration

Le fournisseur Anthropic est disponible dans le module `@ai-sdk/anthropic`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `anthropic` à partir de `@ai-sdk/anthropic` :

```ts
import { anthropic } from '@ai-sdk/anthropic';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createAnthropic` à partir de `@ai-sdk/anthropic` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createAnthropic } from '@ai-sdk/anthropic';

const anthropic = createAnthropic({
  // paramètres personnalisés
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Anthropic :

- **baseURL** _chaîne_

  Utilisez une chaîne de caractères différente pour le préfixe des appels API, par exemple pour utiliser des serveurs proxy.
  Le préfixe par défaut est `https://api.anthropic.com/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée avec l'en-tête `x-api-key`.
  Elle est par défaut définie par la variable d'environnement `ANTHROPIC_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input : RequestInfo, init ?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Les valeurs par défaut sont la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour les tests, par exemple.

## Modèles de Langue

Vous pouvez créer des modèles qui appellent l'[API Messages d'Anthropic](https://docs.anthropic.com/claude/reference/messages_post) à l'aide de l'instance du fournisseur.
La première argument est l'identifiant du modèle, par exemple `claude-3-haiku-20240307`.
Certains modèles disposent de capacités multi-modales.

```ts
const model = anthropic('claude-3-haiku-20240307');
```

Vous pouvez utiliser les modèles de langage d'Anthropic pour générer du texte avec la fonction `generateText` :

```ts
import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

const { text } = await generateText({
  model: anthropic('claude-3-haiku-20240307'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage d'Anthropic peuvent également être utilisés dans les fonctions `streamText`, `generateObject` et `streamObject`
(voir [AI SDK Core](/docs/ai-sdk-core)).

<Note>
  L'API d'Anthropic retourne des appels de la fonction de flux tous ensemble après un délai. Cela
  cause la fonction `streamObject` à générer l'objet entièrement après un délai
  au lieu de le transmettre de manière incrémentale.
</Note>

Les paramètres facultatifs suivants sont disponibles pour les modèles d'Anthropic :

- `sendReasoning` _boolean_

  Facultatif. Inclure le contenu de raisonnement dans les requêtes envoyées au modèle. Par défaut à `true`.

  Si vous rencontrez des problèmes avec le modèle pour traiter les requêtes impliquant du contenu de raisonnement, vous pouvez définir cela sur `false` pour les omettre de la requête.

### Raisonnement

Anthropic propose des fonctionnalités de raisonnement pour les modèles `claude-4-opus-20250514`, `claude-4-sonnet-20250514` et `claude-3-7-sonnet-20250219`.

Vous pouvez l'activer en utilisant l'option de fournisseur `thinking` et en spécifiant un budget de tokens.

```ts
import { anthropic, AnthropicProviderOptions } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

const { text, raisonnement, detailsRaisonnement } = await generateText({
  model: anthropic('claude-4-opus-20250514'),
  prompt: 'Combien de personnes vivront dans le monde en 2040 ?',
  providerOptions: {
    anthropic: {
      thinking: { type: 'enabled', budgetTokens: 12000 },
    } satisfies AnthropicProviderOptions,
  },
});

console.log(raisonnement); // texte de raisonnement
console.log(detailsRaisonnement); // détails du raisonnement incluant le raisonnement masqué
console.log(text); // réponse au texte
```

Voir [UI SDK AI : Chatbot](/docs/ai-sdk-ui/chatbot#raisonnement) pour plus de détails sur la mise en œuvre du raisonnement dans votre chatbot.

### Contrôle de Cache

<Note>
  Le contrôle de cache anthropique était à l'origine une fonctionnalité bêta et nécessitait la transmission d'une option `cacheControl` lors de la création de l'instance du modèle. Il est maintenant généralement disponible et activé par défaut. L'option `cacheControl` n'est plus nécessaire et sera supprimée dans une future mise à jour.
</Note>

Dans les messages et les parties de message, vous pouvez utiliser la propriété `providerOptions` pour définir les points de rupture de contrôle de cache.
Vous devez définir la propriété `anthropic` dans l'objet `providerOptions` sur `{ cacheControl: { type: 'ephemeral' } }` pour définir un point de rupture de contrôle de cache.

Les jetons d'entrée de création de cache sont ensuite retournés dans l'objet `providerMetadata` pour `generateText` et `generateObject`, encore une fois sous la propriété `anthropic`.
Lorsque vous utilisez `streamText` ou `streamObject`, la réponse contient une promesse qui se résout sur les métadonnées. Alternativement, vous pouvez les recevoir dans le callback `onFinish`.

```ts highlight="8,18-20,29-30"
import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';

const errorMessage = '... longue erreur de message ...';
```

```javascript
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20240620'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Vous êtes un expert en JavaScript.' },
        {
          type: 'text',
          text: `Message d'erreur : ${errorMessage}`,
          providerOptions: {
            anthropic: { cacheControl: { type: 'ephemeral' } },
          },
        },
        { type: 'text', text: 'Expliquez le message d\'erreur.' },
      ],
    },
  ],
});

console.log(result.text);
console.log(result.providerMetadata?.anthropic);
// e.g. { cacheCreationInputTokens: 2118, cacheReadInputTokens: 0 }
```

Vous pouvez également utiliser la gestion de cache sur les messages système en fournissant plusieurs messages système en tête de votre tableau de messages :
```markdown
### Exemple
```javascript
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20240620'),
  messages: [
    {
      role: 'assistant',
      content: [
        { type: 'text',

```ts highlight="3,7-9"
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20240620'),
  messages: [
    {
      role: 'system',
      content: 'Partie de message système en cache',
      providerOptions: {
        anthropic: { cacheControl: { type: 'éphémère' } },
      },
    },
    {
      role: 'system',
      content: 'Partie de message système non en cache',
    },
    {
      role: 'user',
      content: 'Invite de l'utilisateur',
    },
  ],
});
```

La longueur minimale d'un prompt pouvant être mis en cache est :

- 1024 jetons pour Claude 3.7 Sonnet, Claude 3.5 Sonnet et Claude 3 Opus
- 2048 jetons pour Claude 3.5 Haïku et Claude 3 Haïku

Les prompts plus courts ne peuvent pas être mis en cache, même si ils sont marqués avec `cacheControl`. Toute demande de mise en cache d'un nombre inférieur de jetons sera traitée sans mise en cache.

Pour plus d'informations sur la mise en cache des prompts avec Anthropic, voir la [documentation de contrôle de cache d'Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching).

<Note type="avertissement">
  Puisque le type `UIMessage` (utilisé par les hooks UI SDK d'IA comme `useChat`) ne
  supporte pas la propriété `providerOptions`, vous pouvez utiliser `convertToCoreMessages`
  avant de passer les messages aux fonctions comme `generateText` ou `streamText`. Pour plus de détails sur l'utilisation de `providerOptions`, voir
  [ici](/docs/foundations/prompts)

# options du fournisseur).

</Note>

### Utilisation de l'ordinateur

Anthropic fournit trois outils intégrés pouvant être utilisés pour interagir avec des systèmes externes :

1. **Outil Bash** : Permet d'exécuter des commandes bash.
2. **Outil d'édition de texte** : Fournit des fonctionnalités pour afficher et modifier des fichiers texte.
3. **Outil ordinateur** : Permet de contrôler les actions de la souris et du clavier sur un ordinateur.

Ils sont disponibles via la propriété `tools` de l'instance du fournisseur.

#### Outil Bash

L'Outil Bash permet d'exécuter des commandes bash. Voici comment le créer et l'utiliser :

```ts
const bashTool = anthropic.tools.bash_20241022({
  execute: async ({ command, restart }) => {
    // Implémentez ici votre logique d'exécution de la commande bash
    // Retournez le résultat de l'exécution de la commande
  },
});
```

Paramètres :

- `command` (chaîne de caractères) : La commande bash à exécuter. Obligatoire à moins que l'outil soit redémarré.
- `restart` (booléen, facultatif) : Spécifier true redémarrera cet outil.

#### Outil de l'éditeur de texte

L'outil de l'éditeur de texte fournit des fonctionnalités pour afficher et modifier les fichiers de texte :

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
    // Implémentez votre logique d'édition de texte ici
    // Retournez le résultat de l'opération d'édition de texte
  },
});
```

Paramètres :

- `command` ('view' | 'create' | 'str_replace' | 'insert' | 'undo_edit'): La commande à exécuter.
- `path` (chaîne de caractères): Chemin absolu vers un fichier ou un répertoire, par exemple `/repo/file.py` ou `/repo`.
- `file_text` (chaîne de caractères, facultatif): Obligatoire pour la commande `create`, contenant le contenu du fichier à créer.
- `insert_line` (nombre, facultatif): Obligatoire pour la commande `insert`. Le numéro de ligne après lequel insérer la nouvelle chaîne de caractères.
- `new_str` (chaîne de caractères, facultatif): Nouvelle chaîne de caractères pour les commandes `str_replace` ou `insert`.
- `old_str` (chaîne de caractères, facultatif): Obligatoire pour la commande `str_replace`, contenant la chaîne de caractères à remplacer.
- `view_range` (tableau de nombres, facultatif): Facultatif pour la commande `view` pour spécifier la plage de lignes à afficher.

Lorsque vous utilisez l'outil de l'éditeur de texte, assurez-vous de nommer la clé dans l'objet des outils `str_replace_editor`.

```ts
const response = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  prompt:
    "Créez un nouveau fichier appelé example.txt, écrivez 'Hello World' à l'intérieur, et exécutez 'cat example.txt' dans la console",
  tools: {
    str_replace_editor: textEditorTool,
  },
});
```

#### Outil Informatique

L'Outil Informatique permet le contrôle des actions de clavier et souris sur un ordinateur :

```ts
const computerTool = anthropic.tools.computer_20241022({
  largeurEcranPx: 1920,
  hauteurEcranPx: 1080,
  numeroEcran: 0, // Optionnel, pour les environnements X11

  execute: async ({ action, coordinate, text }) => {
    // Implémentez votre logique de contrôle de l'ordinateur ici
    // Retournez le résultat de l'action

    // Exemple de code :
    switch (action) {
      case 'screenshot': {
        // résultat multipart :
        return {
          type: 'image',
          data: fs
            .readFileSync('./data/screenshot-editor.png')
            .toString('base64'),
        };
      }
      default: {
        console.log('Action:', action);
        console.log('Coordonnées:', coordinate);
        console.log('Texte:', text);
        return `exécuté ${action}`;
      }
    }
  },

  // mapper vers le contenu de la résultat de l'outil pour la consommation LLM :
  experimental_toToolResultContent(result) {
    return typeof result === 'string'
      ? [{ type: 'text', text: result }]
      : [{ type: 'image', data: result.data, mimeType: 'image/png' }];
  },
});
```

Paramètres :

- `action` ('clé' | 'type' | 'déplacement_souris' | 'clique_gauche' | 'clique_gauche_drag' | 'clique_droit' | 'clique_milieu' | 'double_clique' | 'capture_ecran' | 'position_souris'): L'action à effectuer.
- `coordinate` (number[], facultatif): Obligatoire pour les actions `déplacement_souris` et `clique_gauche_drag`. Spécifie les coordonnées (x, y).
- `text` (string, facultatif): Obligatoire pour les actions `type` et `clé`.

Ces outils peuvent être utilisés en conjonction avec le modèle `sonnet-3-5-sonnet-20240620` pour permettre des interactions et des tâches plus complexes.

### Support de PDF

Anthropic Sonnet `claude-3-5-sonnet-20241022` prend en charge la lecture de fichiers PDF.
Vous pouvez passer des fichiers PDF en tant que contenu du message en utilisant le type `file` :

Option 1 : Document PDF basé sur l'URL

```ts
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: 'Quelle est une modèle d'embedding selon ce document ?',
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

Option 2 : Document PDF encodé en Base64

```typescript
const result = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: 'Qu\'est-ce qu\'un modèle d\'embedding selon ce document ?',
        },
        {
          type: 'fichier',
          data: fs.readFileSync('./data/ai.pdf'),
          mimeType: 'application/pdf',
        },
      ],
    },
  ],
});
```

Le modèle aura accès au contenu du fichier PDF et répondra aux questions à ce sujet.
Le fichier PDF doit être passé à l'aide du champ `data` et le `mimeType` doit être défini sur `'application/pdf'`.

### Capacités du Modèle

### Pr

| Modèle                        | Entrée d'image         | Génération d'objet   | Utilisation de l'outil          | Utilisation de l'ordinateur        |
| ---------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `claude-4-opus-20250514`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-4-sonnet-20250514`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-7-sonnet-20250219` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-5-sonnet-20241022` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `claude-3-5-sonnet-20240620` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-5-haiku-20241022`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-opus-20240229`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `claude-3-sonnet-20240229`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

| `claude-3-haiku-20240307`    | <Vérifieur size={18} /> | <Vérifieur size={18} /> | <Vérifieur size={18} /> | <Croix size={18} />

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter la [documentation d'Anthropic](https://docs.anthropic.com/en/docs/about-claude/models) pour une liste complète des modèles disponibles. La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID du modèle d'un fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

---
titre : Amazon Bedrock
description : Apprenez à utiliser le fournisseur Amazon Bedrock.
---

# Fournisseur Amazon Bedrock

Le fournisseur Amazon Bedrock pour le [SDK AI](/docs) contient un support de modèle de langage pour les [APIs Amazon Bedrock](https://aws.amazon.com/bedrock).

## Configuration

Le fournisseur Bedrock est disponible dans le module `@ai-sdk/amazon-bedrock`. Vous pouvez l'installer avec

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

### Prérequis

L'accès aux modèles de fondation d'Amazon Bedrock n'est pas autorisé par défaut. Pour obtenir accès à un modèle de fondation, un utilisateur IAM disposant des permissions suffisantes doit demander l'accès à travers le console. Une fois l'accès fourni à un modèle, il est disponible pour tous les utilisateurs de l'account.

Voir les [Documents d'accès aux modèles](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) pour plus d'informations.

### Authentication

#### Utilisation de la clé d'accès IAM et de la clé secrète

**Étape 1 : Création de la clé d'accès AWS et de la clé secrète**

Pour commencer, vous aurez besoin de créer une clé d'accès AWS et une clé secrète. Voici comment faire :

**Connexion à AWS Management Console**

- Allez sur la [AWS Management Console](https://console.aws.amazon.com/) et connectez-vous avec vos identifiants de compte AWS.

**Création d'un utilisateur IAM**

- Naviguez vers le [tableau de bord IAM](https://console.aws.amazon.com/iam/home) et cliquez sur "Utilisateurs" dans le menu de navigation de gauche.
- Cliquez sur "Créer un utilisateur" et renseignez les détails requis pour créer un nouvel utilisateur IAM.
- Assurez-vous de sélectionner "Accès programmatique" comme type d'accès.
- Le compte utilisateur nécessite la politique `AmazonBedrockFullAccess` attachée à elle.

**Création de la clé d'accès**

- Cliquez sur l'onglet "Certificats de sécurité" puis cliquez sur "Créer une clé d'accès".
- Cliquez sur "Créer une clé d'accès" pour générer un nouveau paire de clés d'accès.
- Téléchargez le fichier `.csv` contenant l'ID de la clé d'accès et la clé secrète d'accès.

**Étape 2 : Configuration de la clé d'accès et de la clé secrète**

Dans votre projet, ajoutez un fichier `.env` si vous n'en avez pas déjà un. Ce fichier sera utilisé pour définir les clés d'accès et les clés secrètes en tant que variables d'environnement. Ajoutez les lignes suivantes au fichier `.env` :

```makefile
AWS_ACCESS_KEY_ID=VOTRE_ID_DE_CLÉ_D_ACCÈS
AWS_SECRET_ACCESS_KEY=VOTRE_CLÉ_SECRÈTE_D_ACCÈS
AWS_REGION=VOTRE_REGION
```

<Note>
  Beaucoup de frameworks comme [Next.js](https://nextjs.org/) chargent automatiquement le fichier `.env`.
  Si vous utilisez un autre framework, vous devrez peut-être charger le fichier `.env` manuellement à l'aide d'un package comme
  [`dotenv`](https://github.com/motdotla/dotenv).
</Note>

N'oubliez pas de remplacer `VOTRE_ID_DE_CLÉ_D_ACCÈS`, `VOTRE_CLÉ_SECRÈTE_D_ACCÈS` et `VOTRE_REGION` par les valeurs réelles de votre compte AWS.

#### Utilisation de la chaîne de crédentials AWS SDK (profils d'instance, rôles d'instance, rôles ECS, comptes de service EKS, etc.)

Lors de l'utilisation de l'AWS SDK, le SDK utilisera automatiquement la chaîne de crédentials pour déterminer les crédentials à utiliser. Cela inclut les profils d'instance, les rôles d'instance, les rôles ECS, les comptes de service EKS, etc. Un comportement similaire est possible en utilisant l'AI SDK en ne spécifiant pas les propriétés `accessKeyId` et `secretAccessKey`, `sessionToken` dans les paramètres du fournisseur et en passant au lieu de cela une propriété `credentialProvider`.

_Usage:_

Le package `@aws-sdk/credential-providers` fournit un ensemble de fournisseurs de crédentials qui peuvent être utilisés pour créer une chaîne de fournisseurs de crédentials.

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `bedrock` à partir de `@ai-sdk/amazon-bedrock` :

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createAmazonBedrock` à partir de `@ai-sdk/amazon-bedrock` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createAmazonBedrock } from '@ai-sdk/amazon-bedrock';

const bedrock = createAmazonBedrock({
  region: 'us-east-1',
  accessKeyId: 'xxxxxxxxx',
  secretAccessKey: 'xxxxxxxxx',
  sessionToken: 'xxxxxxxxx',
});
```

<Note>
  Les paramètres de clés d'accès tombent par défaut sur les valeurs décrites ci-dessous pour les variables d'environnement. Ces valeurs peuvent être définies par votre environnement sans serveur sans que vous en ayez conscience, ce qui peut entraîner des valeurs de clés d'accès fusionnées ou en conflit et des erreurs de fournisseur lors de l'authentification. Si vous rencontrez des problèmes, assurez-vous d'avoir explicitement spécifié toutes les valeurs (même si elles sont indéfinies) pour éviter les valeurs par défaut.
</Note>

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Amazon Bedrock :

- **region** _chaîne_

  La région AWS que vous souhaitez utiliser pour les appels API.
  Il utilise la variable d'environnement `AWS_REGION` par défaut.

- **accessKeyId** _chaîne_

  La clé d'accès AWS que vous souhaitez utiliser pour les appels API.
  Il utilise la variable d'environnement `AWS_ACCESS_KEY_ID` par défaut.

- **secretAccessKey** _chaîne_

  La clé secrète d'accès AWS que vous souhaitez utiliser pour les appels API.
  Il utilise la variable d'environnement `AWS_SECRET_ACCESS_KEY` par défaut.

- **sessionToken** _chaîne_

  Optionnel. Le jeton de session AWS que vous souhaitez utiliser pour les appels API.
  Il utilise la variable d'environnement `AWS_SESSION_TOKEN` par défaut.

- **credentialProvider** _() =&gt; Promise&lt;

#123; accessKeyId: string; secretAccessKey: string; sessionToken?: string; &#125;&gt;_

  Optionnel. La chaîne de fournisseur de clés AWS que vous souhaitez utiliser pour les appels API.
  Elle utilise les clés spécifiées par défaut.

## Modèles de Langue

Vous pouvez créer des modèles qui appellent l'API Bedrock en utilisant l'instance de fournisseur.
Le premier argument est l'identifiant du modèle, par exemple `meta.llama3-70b-instruct-v1:0`.

```ts
const model = bedrock('meta.llama3-70b-instruct-v1:0');
```

Les modèles Amazon Bedrock prennent également en charge certaines paramètres spécifiques au modèle qui ne font pas partie des [paramètres de l'appel standard](/docs/ai-sdk-core/settings).
Vous pouvez les passer comme argument d'option :

```ts
const model = bedrock('anthropic.claude-3-sonnet-20240229-v1:0', {
  additionalModelRequestFields: { top_k: 350 },
});
```

La documentation pour les paramètres supplémentaires en fonction du modèle sélectionné peut être trouvée dans la [documentation des paramètres d'inference d'Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html).

Vous pouvez utiliser les modèles de langage Amazon Bedrock pour générer du texte avec la fonction `generateText` :

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const { text } = await generateText({
  model: bedrock('meta.llama3-70b-instruct-v1:0'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage Amazon Bedrock peuvent également être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

### Entrées de fichiers

<Note type="warning">
  Le fournisseur Amazon Bedrock prend en charge les entrées de fichiers en combinaison avec des modèles spécifiques,
  par exemple `anthropic.claude-3-haiku-20240307-v1:0`.
</Note>

Le fournisseur Amazon Bedrock prend en charge les entrées de fichiers, par exemple des fichiers PDF.

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const result = await generateText({
  model: bedrock('anthropic.claude-3-haiku-20240307-v1:0'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Décrivez le PDF en détail.' },
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

### Garde-fous

Vous pouvez utiliser les options du fournisseur `bedrock` pour prendre en charge les [Garde-fous Amazon Bedrock](https://aws.amazon.com/bedrock/guardrails/):

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

Les informations de suivi seront retournées dans les métadonnées du fournisseur si vous avez activé la traçabilité.

```ts
if (result.providerMetadata?.bedrock.trace) {
  // ...
}
```

Voir la [documentation des Garde-fous Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html

### Points de cache

<Note>
  La mise en cache des prompts Amazon Bedrock est actuellement en version prévue. Pour demander l'accès, visitez la [page de mise en cache des prompts Amazon Bedrock](https://aws.amazon.com/bedrock/prompt-caching/).
</Note>

Dans les messages, vous pouvez utiliser la propriété `providerOptions` pour définir les points de cache. Définissez la propriété `bedrock` dans l'objet `providerOptions` sur `{ cachePoint: { type: 'default' } }` pour créer un point de cache.

Les informations sur l'utilisation de la cache sont retournées dans l'objet `providerMetadata``. Voir les exemples ci-dessous.

<Note>
  Les points de cache ont des minimums et des limites spécifiques pour chaque modèle. Par exemple, Claude 3.5 Sonnet v2 nécessite au moins 1 024 tokens pour un point de cache et permet jusqu'à 4 points de cache. Voir la [documentation de mise en cache des prompts Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) pour plus d'informations sur les modèles pris en charge, les régions et les limites.
</Note>

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const analyseCyberpunk =
  '... analyse littéraire des thèmes et des concepts cyberpunk ...';

const result = await generateText({
  model: bedrock('anthropic.claude-3-5-sonnet-20241022-v2:0'),
  messages: [
    {
      role: 'system',
      content: `Vous êtes un expert sur la littérature et les thèmes cyberpunk de William Gibson. Vous avez accès à l'analyse académique suivante : ${analyseCyberpunk}`,
      providerOptions: {
        bedrock: { cachePoint: { type: 'default' } },
      },
    },
    {
      role: 'user',
      content:
        'Quels sont les thèmes cyberpunk clés que Gibson explore dans Neuromancer ?',
    },
  ],
});
```

```javascript
console.log(result.text);
console.log(result.providerMetadata?.bedrock?.usage);
// Affiche l'utilisation des jetons de lecture/écriture de cache, par exemple :
// {
//   cacheReadInputTokens: 1337,
//   cacheWriteInputTokens: 42,
// }
```

Les points de cache fonctionnent également avec les réponses en flux :

```typescript
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamText } from 'ai';

const cyberpunkAnalysis =
  '... analyse littéraire des thèmes et concepts cyberpunk ...';

const result = streamText({
  model: bedrock('anthropic.claude-3-5-sonnet-20241022-v2:0'),
  messages: [
    {
      role: 'assistant',
      content: [
        { type: 'text', text: 'Vous êtes un expert en littérature cyberpunk.' },
        { type: 'text', text: `Analyse universitaire : ${cyberpunkAnalysis}` },
      ],
      providerOptions: { bedrock: { cachePoint: { type: 'default' } } },
    },
    {
      role: 'user',
      content:
        'Comment Gibson explore-t-il la relation entre l'humanité et la technologie ?',
    },
  ],
});

for await (const textPart of result.textStream) {
  process.stdout.write(textPart);
}

console.log(
  'Utilisation des jetons de cache :',
  (await result.providerMetadata)?.bedrock?.usage,
);
// Affiche l'utilisation des jetons de lecture/écriture de cache, par exemple :
// {
//   cacheReadInputTokens: 1337,
//   cacheWriteInputTokens: 42,
// }
```

## Raisonnement

Amazon Bedrock offre un support de raisonnement pour le modèle `claude-3-7-sonnet-20250219`.

Vous pouvez l'activer en utilisant l'option `reasoning_config` du fournisseur et en spécifiant un budget de pensée en jetons (minimum : `1024`, maximum : `64000`).

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const { text, reasoning, reasoningDetails } = await generateText({
  model: bedrock('us.anthropic.claude-3-7-sonnet-20250219-v1:0'),
  prompt: 'Combien de personnes vivront dans le monde en 2040 ?',
  providerOptions: {
    bedrock: {
      reasoningConfig: { type: 'enabled', budgetTokens: 1024 },
    },
  },
});

console.log(reasoning); // texte de raisonnement
console.log(reasoningDetails); // détails du raisonnement, y compris le raisonnement masqué
console.log(text); // réponse de texte
```

Voir [AI SDK UI : Chatbot](/docs/ai-sdk-ui/chatbot#raisonnement) pour plus de détails sur la mise en œuvre de raisonnement dans votre chatbot.

### Capacités du Modèle

### Description

| Modèle                                       | Entrée d'image         | Génération d'objets   | Utilisation de l'outil          | Flux d'outil Streaming      |
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
| `anthropic.claude-3-5-haiku-20241022-v1:0`  | <Croix size={18} /> | <Check size={18} /> | <Check size={18} /> | <Croix size={18} /> |
| `anthropic.claude-3-opus-20240229-v1:0`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-sonnet-20240229-v1:0`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `anthropic.claude-3-haiku-20240307-v1:0`    | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `anthropic.claude-v2:1`                     | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `cohere.command-r-v1:0`                     | <Cross size={18} /> | <Cross size={18} /> | <Vérifie size={18} /> | <Cross size={18} /> |
| `cohere.command-r-plus-v1:0`                | <Cross size={18} /> | <Cross size={18} /> | <Vérifie size={18} /> | <Cross size={18} /> |
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

| `meta.llama3-2-90b-instruct-v1:0`           | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `mistral.mistral-7b-instruct-v0:2`          | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `mistral.mixtral-8x7b-instruct-v0:1`        | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `mistral.mistral-large-2402-v1:0`           | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `mistral.mistral-small-2402-v1:0`           | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter les [docs Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-supported-models-features.html)
  pour une liste complète des modèles disponibles. La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID de modèle d'un fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

## Embedding de Modèles

Vous pouvez créer des modèles qui appellent l'API Bedrock [Bedrock API](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
à l'aide de la méthode de fabrication `.embedding()`.

```ts
const model = bedrock.embedding('amazon.titan-embed-text-v1');
```

Le modèle d'embeddings Bedrock Titan amazon.titan-embed-text-v2:0 prend en charge plusieurs paramètres supplémentaires.
Vous pouvez les passer en tant qu'argument d'option :

```ts
const model = bedrock.embedding('amazon.titan-embed-text-v2:0', {
  dimensions: 512 // optionnel, nombre de dimensions pour l'embedding
  normalize: true // optionnel, normalise les embeddings de sortie
})
```

Les paramètres facultatifs suivants sont disponibles pour les modèles d'embeddings Bedrock Titan :

- **dimensions** _nombre_

  Le nombre de dimensions que les embeddings de sortie devraient avoir. Les valeurs suivantes sont acceptées : 1024 (par défaut), 512, 256.

- **normalize** _booléen_

  Drapeau indiquant si les embeddings de sortie doivent être normalisés ou non. Par défaut, c'est à `true`.

### Capacités du Modèle

| Modèle                          | Dimensions par Défaut | Dimensions personnalisées   |
| ------------------------------ | ------------------ | --------------------------- |
| `amazon.titan-embed-text-v1`   | 1536               | <Cross size={18} />        |
| `amazon.titan-embed-text-v2:0` | 1024               | <Check size={18} />         |

## Modèles d'images

Vous pouvez créer des modèles qui appellent l'API Bedrock [API Bedrock](https://docs.aws.amazon.com/nova/latest/userguide/image-generation.html)
en utilisant la méthode de fabrication `.image()`.

Pour plus d'informations sur le modèle d'image Amazon Nova Canvas, voir la [Vue d'ensemble de Nova Canvas](https://docs.aws.amazon.com/ai/responsible-ai/nova-canvas/overview.html).

<Note>
  Le modèle `amazon.nova-canvas-v1:0` est disponible dans la région `us-east-1`.
</Note>

```ts
const model = bedrock.image('amazon.nova-canvas-v1:0');
```

Vous pouvez ensuite générer des images avec la fonction `experimental_generateImage` :

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: bedrock.imageModel('amazon.nova-canvas-v1:0'),
  prompt: 'Un coucher de soleil magnifique sur une mer calme',
  size: '512x512',
  seed: 42,
});
```

Vous pouvez également passer l'objet `providerOptions` à la fonction `generateImage` pour personnaliser le comportement de génération :

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: bedrock.imageModel('amazon.nova-canvas-v1:0'),
  prompt: 'Un coucher de soleil magnifique sur une mer calme',
  size: '512x512',
  seed: 42,
  providerOptions: { bedrock: { quality: 'premium' } },
});
```

La documentation des paramètres supplémentaires peut être trouvée dans le [Guide de l'utilisateur Amazon Bedrock pour Amazon Nova
Documentation](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-req-resp-structure.html).

### Paramètres de Modèle d'Image

Lors de la création d'un modèle d'image, vous pouvez personnaliser le comportement de génération avec des paramètres facultatifs :

```ts
const model = bedrock.imageModel('amazon.nova-canvas-v1:0', {
  maxImagesPerCall: 1, // Nombre maximum d'images à générer par appel API
});
```

- **maxImagesPerCall** _nombre_

  Surcharger le nombre maximum d'images générées par appel API. La valeur par défaut peut varier
  en fonction du modèle, avec 5 comme valeur par défaut courante.

### Capacités du Modèle

Le modèle Amazon Nova Canvas prend en charge les tailles personnalisées avec des contraintes telles que :

- Chaque côté doit être compris entre 320 et 4096 pixels, inclus.
- Chaque côté doit être divisible par 16.
- Le rapport d'aspect doit être compris entre 1:4 et 4:1. C'est-à-dire qu'un côté ne peut pas être plus long que 4 fois l'autre côté.
- Le total des pixels doit être inférieur à 4 194 304.

Pour plus d'informations, voir [Accès et utilisation de la génération d'images](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-access.html).

| Modèle                     | Tailles                                                                                                 |
| ------------------------- | ----------------------------------------------------------------------------------------------------- |
| `amazon.nova-canvas-v1:0` | Tailles personnalisées : 320-4096px par côté (doivent être divisibles par 16), rapport d'aspect 1:4 à 4:1, max 4.2M pixels |

## En-têtes de réponse

Le fournisseur Amazon Bedrock retournera les en-têtes de réponse associés aux requêtes réseau effectuées sur les serveurs Bedrock.

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { generateText } from 'ai';

const { text } = await generateText({
  model: bedrock('meta.llama3-70b-instruct-v1:0'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});

console.log(result.response.headers);
```

Voici un exemple de sortie où vous pouvez voir l'en-tête `x-amzn-requestid`. Cela peut être utile pour corrélater les appels API Bedrock avec les requêtes effectuées par le SDK AI :

```js highlight="6"
{
  connection: 'keep-alive',
  'content-length': '2399',
  'content-type': 'application/json',
  date: 'Fri, 07 Feb 2025 04:28:30 GMT',
  'x-amzn-requestid': 'c9f3ace4-dd5d-49e5-9807-39aedfa47c8e'
}
```

Cette information est également disponible avec `streamText` :

```ts
import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamText } from 'ai';

const result = streamText({
  model: bedrock('meta.llama3-70b-instruct-v1:0'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
for await (const textPart of result.textStream) {
  process.stdout.write(textPart);
}
console.log('En-têtes de réponse :', (await result.response).headers);
```

Avec un exemple de sortie comme :

```js highlight="6"
{
  connection: 'keep-alive',
  'content-type': 'application/vnd.amazon.eventstream',
  date: 'Ven, 07 fév 2025 04:33:37 GMT',
  'transfer-encoding': 'chunked',
  '

## Migration vers `@ai-sdk/amazon-bedrock` 2.x

Le fournisseur Amazon Bedrock a été réécrit dans la version 2.x pour supprimer la dépendance envers le package `@aws-sdk/client-bedrock-runtime`.

L'option de fournisseur `bedrockOptions` disponible précédemment a été supprimée. Si vous utilisiez l'objet `bedrockOptions`, vous devriez maintenant utiliser les paramètres `region`, `accessKeyId`, `secretAccessKey` et `sessionToken` directement au lieu.

Notez que vous devriez peut-être définir tous ces paramètres explicitement, par exemple même si vous n'utilisez pas `sessionToken`, définissez-le sur `undefined`. Si vous exécutez dans un environnement serverless, il peut y avoir des variables d'environnement par défaut définies par votre environnement conteneur qui seront ensuite prises en charge par le fournisseur Amazon Bedrock et pourraient entrer en conflit avec les paramètres que vous souhaitez utiliser.

---
titre : Groq
description : Apprenez à utiliser Groq.
---

# Fournisseur Groq

Le [fournisseur Groq](https://groq.com/) contient un support pour les modèles de langage de l'API Groq.

## Configuration

Le fournisseur Groq est disponible via le module `@ai-sdk/groq`.
Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `groq` à partir de `@ai-sdk/groq` :

```ts
import { groq } from '@ai-sdk/groq';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createGroq` à partir de `@ai-sdk/groq`
et créer une instance de fournisseur avec vos paramètres :

```ts
import { createGroq } from '@ai-sdk/groq';

const groq = createGroq({
  // paramètres personnalisés
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Groq :

- **baseURL** _chaîne_

  Utilisez une adresse URL différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  La valeur par défaut est `https://api.groq.com/openai/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  La valeur par défaut est la variable d'environnement `GROQ_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  La valeur par défaut est la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests, par exemple.

## Modèles de langage

Vous pouvez créer des [modèles Groq](https://console.groq.com/docs/models) à l'aide d'une instance de fournisseur.
La première argument est l'ID du modèle, par exemple `gemma2-9b-it`.

```ts
const model = groq('gemma2-9b-it');
```

### Modèles de Raisonnement

Groq offre plusieurs modèles de raisonnement comme `qwen-qwq-32b` et `deepseek-r1-distill-llama-70b`.
Vous pouvez configurer la façon dont le raisonnement est exposé dans le texte généré en utilisant l'option `reasoningFormat`.
Il prend en charge les options `parsed`, `hidden` et `raw`.

```ts
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const result = await generateText({
  model: groq('qwen-qwq-32b'),
  providerOptions: {
    groq: { reasoningFormat: 'parsed' },
  },
  prompt: 'Combien de "r"s sont dans le mot "fraise"?',
});
```

<Remarque>Seuls les modèles de raisonnement Groq supportent l'option `reasoningFormat.`</Remarque>

### Exemple

Vous pouvez utiliser les modèles de langage Groq pour générer du texte avec la fonction `generateText` :

```ts
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const { text } = await generateText({
  model: groq('gemma2-9b-it'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

## Capacités du Modèle

| Modèle                                       | Entrée d'Image         | Génération d'Objet   | Utilisation d'Outils          | Flux d'Outils      |
| ------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `meta-llama/llama-4-scout-17b-16e-instruct` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemma2-9b-it`                              | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama-3.3-70b-versatile`                   | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama-3.1-8b-instant`                      | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama-guard-3-8b`                          | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `llama3-70b-8192`                           | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `llama3-8b-8192`                            | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `mixtral-8x7b-32768`                        | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `qwen-qwq-32b`                              | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `mistral-saba-24b`                          | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `qwen-2.5-32b`                              | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `deepseek-r1-distill-qwen-32b`              | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |

| `deepseek-r1-distill-llama-70b`             | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter les [docs de Groq](https://console.groq.com/docs/models) pour une liste complète des modèles disponibles. La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID de modèle de fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription de Groq](https://console.groq.com/docs/speech-to-text)
en utilisant la méthode de fabrication `.transcription()`.

La première argument est l'identifiant du modèle par exemple `whisper-large-v3`.

```ts
const model = groq.transcription('whisper-large-v3');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, en fournissant la langue d'entrée au format ISO-639-1 (par exemple `en`) améliorera la précision et la latence.

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

Les options de fournisseur suivantes sont disponibles :

- **timestampGranularités** _string[]_
  La granularité des horodatages dans la transcription.
  Défaut à `['segment']`.
  Les valeurs possibles sont `['word']`, `['segment']`, et `['word', 'segment']`.
  Remarque : Il n'y a pas de latence supplémentaire pour les horodatages de segment, mais la génération d'horodatages de mots entraîne une latence supplémentaire.

- **langue** _string_
  La langue de l'audio d'entrée. Fournir la langue d'entrée au format ISO-639-1 (par exemple 'en') améliorera la précision et la latence.
  Facultatif.

- **invite** _string_
  Un texte optionnel pour guider le style du modèle ou continuer un segment audio précédent. L'invite doit correspondre à la langue de l'audio.
  Facultatif.

- **température** _nombre_
  La température d'échantillonnage, comprise entre 0 et 1. Des valeurs plus élevées comme 0,8 feront sortir une sortie plus aléatoire, tandis que des valeurs plus basses comme 0,2 feront sortir une sortie plus ciblée et déterministe. Si elle est fixée à 0, le modèle utilisera la probabilité logarithmique pour augmenter automatiquement la température jusqu'à ce que certaines seuils soient atteints.
  Défaut à 0.
  Optionnel.

### Capacités du modèle

| Modèle                        | Transcription       | Durée            | Segments            | Langue            |
| ---------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper-large-v3`           | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `whisper-large-v3-turbo`     | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `distil-whisper-large-v3-en` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

---
Titre : Fal
Description : Apprenez à utiliser les modèles Fal AI avec le SDK AI.
---

# Fournisseur Fal

[Fal AI](https://fal.ai/) fournit une plateforme de médias génératifs pour les développeurs avec des capacités d'inference fulgurantes. Leur plateforme offre une performance optimisée pour exécuter les modèles de diffusion, avec des vitesses jusqu'à 4 fois plus rapides que les alternatives.

## Configuration

Le fournisseur Fal est disponible via le module `@ai-sdk/fal`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `fal` à partir de `@ai-sdk/fal` :

```ts
import { fal } from '@ai-sdk/fal';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createFal` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createFal } from '@ai-sdk/fal';

const fal = createFal({
  apiKey: 'votre-clé-api', // facultatif, par défaut à l'environnement FAL_API_KEY, tombant en panne sur FAL_KEY
  baseURL: 'URL-personnalisée', // facultatif
  headers: {
    /* en-têtes personnalisés */
  }, // facultatif
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Fal :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  Le prefixe par défaut est `https://fal.run`.

- **apiKey** _chaîne_

  Clé API qui est envoyée à l'aide de l'en-tête `Authorization`.
  Elle par défaut à l'environnement `FAL_API_KEY`, tombant en panne sur `FAL_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour des tests par exemple.

## Modèles d'image

Vous pouvez créer des modèles d'image Fal à l'aide de la méthode de fabrication `.image()`.
Pour plus d'informations sur la génération d'image avec le SDK AI, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

### Utilisation de base

```ts
import { fal } from '@ai-sdk/fal';
import { experimental_generateImage as generateImage } from 'ai';
import fs from 'fs';

const { image } = await generateImage({
  model: fal.image('fal-ai/fast-sdxl'),
  prompt: 'Un paysage montagneux calme au coucher du soleil',
});

const filename = `image-${Date.now()}.png`;
fs.writeFileSync(filename, image.uint8Array);
console.log(`L'image a été enregistrée dans ${filename}`);
```

### Capabilités du Modèle

Fal offre de nombreux modèles optimisés pour différents cas d'utilisation. Voici quelques exemples populaires. Pour une liste complète de modèles, voir la [documentation Fal AI](https://fal.ai/models).

| Modèle                               | Description                                                                                                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fal-ai/fast-sdxl`                  | Modèle SDXL haute vitesse optimisé pour une inférence rapide avec des vitesses jusqu'à 4 fois plus rapides                                                                               |
| `fal-ai/flux-pro/kontext`           | FLUX.1 Kontext [pro] gère à la fois les textes et les images de référence en entrée, permettant des éditions ciblées et des transformations complexes de scènes entières de manière fluide |
| `fal-ai/flux-pro/kontext/max`       | FLUX.1 Kontext [max] avec une adhérence aux prompts et une génération de typographie améliorées, répondant aux normes premium pour l'édition sans compromis sur la vitesse      |
| `fal-ai/flux-lora`                  | Point d'entrée rapide pour le modèle FLUX.1 [dev] avec support LoRA, permettant une génération d'image rapide et de haute qualité à l'aide de adaptations LoRA pré-entraînées.        |

| `fal-ai/flux-pro/v1.1-ultra`        | Génération d'image de qualité professionnelle avec une résolution allant jusqu'à 2K et une photoréalisme améliorée                                                                 |
| `fal-ai/ideogram/v2`                | Spécialisé pour des posters et logos de haute qualité avec un traitement exceptionnel de la typographie                                                                            |
| `fal-ai/recraft-v3`                 | SOTA en génération d'image avec des capacités d'art vectoriel et de style de marque                                                                                         |
| `fal-ai/stable-diffusion-3.5-large` | Modèle MMDiT avancé avec une amélioration de la typographie et une compréhension de prompts complexes                                                                                   |

| `fal-ai/hyper-sdxl`                 | Varianté de SDXL optimisé pour les performances avec des capacités créatives améliorées

Les modèles Fal supportent les ratios d'aspect suivants :

- 1:1 (HD carré)
- 16:9 (paysage)
- 9:16 (portrait)
- 4:3 (paysage)
- 3:4 (portrait)
- 16:10 (1280x800)
- 10:16 (800x1280)
- 21:9 (2560x1080)
- 9:21 (1080x2560)

Les caractéristiques clés des modèles Fal incluent :

- Des vitesses d'inference jusqu'à 4 fois plus rapides par rapport aux alternatives
- Optimisé par le Fal Inference Engine™
- Support pour une infrastructure temps réel
- Échelle rentable avec un prix payant d'utilisation
- Capacités de formation LoRA pour la personnalisation des modèles

#### Modifier une Image

Transformer des images existantes à l'aide de prompts de texte.

```ts
// Exemple : Modifier une image existante
await generateImage({
  model: fal.image('fal-ai/flux-pro/kontext'),
  prompt: 'Placez un beignet à côté de la farine.',
  providerOptions: {
    fal: {
      image_url:
        'https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png',
    },
  },
});
```

### Fonctionnalités Avancées

La plateforme Fal offre plusieurs capacités avancées :

- **Inférence de Modèle Privé** : Exécutez vos propres modèles de transformation de diffusion avec une inférence jusqu'à 50 % plus rapide
- **Formation de LoRA** : Formez et personnalisez les modèles en moins de 5 minutes
- **Infrastructure en Temps Réel** : Activez de nouvelles expériences utilisateur avec des temps d'inférence rapides
- **Architecture Échelle** : Échellez jusqu'à des milliers de GPU lorsque nécessaire

Pour plus de détails sur les capacités et les fonctionnalités de Fal, visitez la [documentation Fal AI](https://fal.ai/docs).

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription Fal](https://docs.fal.ai/guides/convert-speech-to-text)
en utilisant la méthode de fabrique `.transcription()`.

La première argument est l'ID du modèle sans le préfixe `fal-ai/` par exemple `wizper`.

```ts
const model = fal.transcription('wizper');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, en fournissant l'option `batchSize` augmentera le nombre de tranches audio traitées en parallèle.

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

Les options de fournisseur disponibles sont :

- **langue** _chaîne_
  Langue du fichier audio. Si défini sur null, la langue sera détectée automatiquement.
  Accepte les codes de langue ISO comme 'en', 'fr', 'zh', etc.
  Facultatif.

- **diariser** _booléen_
  Si diariser le fichier audio (identifier les différents locuteurs).
  Par défaut à true.
  Facultatif.

- **chunkLevel** _chaîne_
  Niveau des tranches à retourner. Soit 'segment' ou 'mot'.
  Valeur par défaut : "mot"
  Facultatif.

- **version** _chaîne_
  Version du modèle à utiliser. Tous les modèles sont des variants grand de Whisper.
  Valeur par défaut : "3"
  Facultatif.

- **batchSize** _nombre_
  Taille de la plage pour le traitement.
  Valeur par défaut : 64
  Facultatif.

- **numSpeakers** _nombre_
  Nombre de locuteurs dans le fichier audio. Si non fourni, le nombre de locuteurs sera détecté automatiquement.
  Facultatif.

### Capacités du Modèle

| Modèle     | Transcription       | Durée            | Segments            | Langue            |
| --------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `whisper` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `wizper`  | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titre : AssemblyAI
description : Apprenez à utiliser le fournisseur AssemblyAI pour le SDK AI.
---

# Fournisseur AssemblyAI

Le [fournisseur AssemblyAI](https://assemblyai.com/) contient un support pour les modèles de langage de l'API de transcription AssemblyAI.

## Configuration

Le fournisseur AssemblyAI est disponible dans le module `@ai-sdk/assemblyai`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `assemblyai` à partir de `@ai-sdk/assemblyai` :

```ts
import { assemblyai } from '@ai-sdk/assemblyai';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createAssemblyAI` à partir de `@ai-sdk/assemblyai` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createAssemblyAI } from '@ai-sdk/assemblyai';

const assemblyai = createAssemblyAI({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur AssemblyAI :

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Elle est par défaut définie sur la variable d'environnement `ASSEMBLYAI_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Elle est par défaut définie sur la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests par exemple.

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription d'AssemblyAI](https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file/typescript)
en utilisant la méthode de fabrication `.transcription()`.

La première argument est l'ID du modèle, par exemple `best`.

```ts
const model = assemblyai.transcription('best');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, en fournissant l'option `contentSafety` pour activer la filtration de sécurité du contenu.

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

Les options de fournisseur suivantes sont disponibles :

- **audioEndAt** _nombre_

  Temps de fin de l'audio en millisecondes.
  Optionnel.

- **audioStartFrom** _nombre_

  Temps de début de l'audio en millisecondes.
  Optionnel.

- **autoChapters** _boolean_

  Si les chapitres doivent être générés automatiquement pour la transcription.
  Optionnel.

- **autoHighlights** _boolean_

  Si les highlights doivent être générés automatiquement pour la transcription.
  Optionnel.

- **boostParam** _enum_

  Paramètre de boost pour la transcription.
  Valeurs autorisées : `'low'`, `'default'`, `'high'`.
  Optionnel.

- **contentSafety** _boolean_

  Si la filtration de sécurité du contenu doit être activée.
  Optionnel.

- **contentSafetyConfidence** _nombre_

  Seuil de confiance pour la filtration de sécurité du contenu (25-100).
  Optionnel.

- **customSpelling** _tableau d'objets_

  Règles de ponctuation personnalisées pour la transcription.
  Chaque objet a les propriétés `from` (tableau de chaînes) et `to` (chaîne).
  Optionnel.

- **disfluencies** _boolean_

**Inclure les dysfluences (um, uh, etc.) dans la transcription.**
  Optionnel.

- **entityDetection** _boolean_

  Déterminer si détecter les entités dans la transcription.
  Optionnel.

- **filterProfanity** _boolean_

  Déterminer si filtrer la profanité dans la transcription.
  Optionnel.

- **formatText** _boolean_

  Déterminer si formatter le texte dans la transcription.
  Optionnel.

- **iabCategories** _boolean_

  Déterminer si inclure les catégories IAB dans la transcription.
  Optionnel.

- **languageCode** _string_

  Code de langue pour l'audio.
  Supporte de nombreux codes de langue ISO-639-1 et ISO-639-3.
  Optionnel.

- **languageConfidenceThreshold** _number_

  Threshold de confiance pour la détection de langue.
  Optionnel.

- **languageDetection** _boolean_

  Déterminer si activer la détection de langue.
  Optionnel.

- **multichannel** _boolean_

  Déterminer si traiter les canaux audio séparément.
  Optionnel.

- **punctuate** _boolean_

  Déterminer si ajouter des signes de ponctuation à la transcription.
  Optionnel.

- **redactPii** _boolean_

  Déterminer si masquer les informations personnellement identifiables.
  Optionnel.

- **redactPiiAudio** _boolean_

  Déterminer si masquer les PII dans le fichier audio.
  Optionnel.

- **redactPiiAudioQuality** _enum_

  Qualité du fichier audio masqué.
  Valeurs autorisées : `'mp3'`, `'wav'`.
  Optionnel.

- **redactPiiPolicies** _array of enums_

  Politiques pour la suppression des PII, spécifiant les types d'informations à masquer.
  Supporte de nombreux types comme `'person_name'`, `'phone_number'`, etc.
  Optionnel.

- **redactPiiSub** _enum_

  Méthode de substitution pour les PII masqués.
  Valeurs autorisées : `'entity_name'`, `'hash'`.
  Optionnel.

- **sentimentAnalysis** _boolean_

  Déterminer si effectuer une analyse d'opinion sur la transcription.
  Optionnel.

- **speakerLabels** _boolean_

**Étiquetage des différents locuteurs dans la transcription**
  Optionnel.

- **speakersExpected** _nombre_

  Nombre attendu de locuteurs dans l'enregistrement audio.
  Optionnel.

- **speechThreshold** _nombre_

  Threshold pour la détection de la parole (0-1).
  Optionnel.

- **summarization** _booléen_

  Étiquette pour générer un résumé de la transcription.
  Optionnel.

- **summaryModel** _énumération_

  Modèle à utiliser pour la résumé.
  Valeurs autorisées : `'informative'`, `'conversational'`, `'catchy'`.
  Optionnel.

- **summaryType** _énumération_

  Type de résumé à générer.
  Valeurs autorisées : `'bullets'`, `'bullets_verbose'`, `'gist'`, `'headline'`, `'paragraph'`.
  Optionnel.

- **topics** _tableau de chaînes de caractères_

  Liste de sujets à détecter dans la transcription.
  Optionnel.

- **webhookAuthHeaderName** _chaîne de caractères_

  Nom de l'en-tête d'authentification pour les requêtes webhook.
  Optionnel.

- **webhookAuthHeaderValue** _chaîne de caractères_

  Valeur de l'en-tête d'authentification pour les requêtes webhook.
  Optionnel.

- **webhookUrl** _chaîne de caractères_

  URL à envoyer les notifications webhook.
  Optionnel.

- **wordBoost** _tableau de chaînes de caractères_

  Liste de mots à amplifier dans la transcription.
  Optionnel.

### Capacités du modèle

| Modèle  | Transcription       | Durée            | Segment            | Langue            |
| ------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `best` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `nano` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titre : DeepInfra
description : Apprenez à utiliser les modèles de DeepInfra avec l'API du SDK AI.
---

# Fournisseur DeepInfra

Le [fournisseur DeepInfra](https://deepinfra.com) contient des fonctionnalités pour les modèles de pointe de la technologie grâce à l'API DeepInfra, y compris Llama 3, Mixtral, Qwen et de nombreux autres modèles open-source populaires.

## Configuration

Le fournisseur DeepInfra est disponible via le module `@ai-sdk/deepinfra`. Vous pouvez l'installer avec :

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `deepinfra` à partir de `@ai-sdk/deepinfra` :

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createDeepInfra` à partir de `@ai-sdk/deepinfra` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createDeepInfra } from '@ai-sdk/deepinfra';

const deepinfra = createDeepInfra({
  apiKey: process.env.DEEPINFRA_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur DeepInfra :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser les serveurs proxy.
  Le prefixe par défaut est `https://api.deepinfra.com/v1/openai`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. Il prend par défaut la valeur de la variable d'environnement `DEEPINFRA_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de la fonction [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Par défaut, la fonction `fetch` globale est utilisée.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour les tests, par exemple.

## Modèles de Langue

Vous pouvez créer des modèles de langue à l'aide d'une instance de fournisseur. La première argument est l'ID du modèle, par exemple :

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
import { generateText } from 'ai';

const { text } = await generateText({
  model: deepinfra('meta-llama/Meta-Llama-3.1-70B-Instruct'),
  prompt: 'Écrivez une recette de lasagnes végétariennes pour 4 personnes.',
});
```

Les modèles de DeepInfra peuvent également être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

## Capabilités du Modèle

| Modèle                                             | Entrée d'Image         | Génération d'Objet   | Utilisation d'Outil          | Flux d'Outil Streaming      |
| --------------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct`         | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo`           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Llama-3.3-70B-Instruct`                 | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Meta-Llama-3.1-405B-Instruct`           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`      | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `meta-llama/Meta-Llama-3.1-70B-Instruct`            | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`       | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Croix size={18} /> |
| `meta-llama/Meta-Llama-3.1-8B-Instruct`             | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> |
| `meta-llama/Llama-3.2-11B-Vision-Instruct`          | <Vérifié size={18} /> | <Vérifié size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `meta-llama/Llama-3.2-90B-Vision-Instruct`          | <Vérifié size={18} /> | <Vérifié size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `mistralai/Mixtral-8x7B-Instruct-v0.1`              | <Croix size={18} /> | <Vérifié size={18} /> | <Vérifié size={18} /> | <Croix size={18} /> |
| `deepseek-ai/DeepSeek-V3`                           | <Croix size={18} /> | <Croix size={18} /> | <

| `deepseek-ai/DeepSeek-R1`                           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`         | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `deepseek-ai/DeepSeek-R1-Turbo`                     | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `nvidia/Llama-3.1-Nemotron-70B-Instruct`            | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `Qwen/Qwen2-7B-Instruct`                            | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `Qwen/Qwen2.5-72B-Instruct`                         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `Qwen/Qwen2.5-Coder-32B-Instruct`                   | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `Qwen/QwQ-32B-Preview`                              | <Croix size={18} /> | <Vérifié size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `google/codegemma-7b-it`                            | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `google/gemma-2-9b-it`                              | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `microsoft/WizardLM-2-8x22B`                        | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter les [docs DeepInfra](https://deepinfra.com) pour une liste complète des modèles disponibles. Vous pouvez également passer l'ID du modèle de fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

## Modèles d'Images

Vous pouvez créer des modèles d'images DeepInfra à l'aide de la méthode de fabrication `.image()`.
Pour plus d'informations sur la génération d'images avec le SDK AI, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: deepinfra.image('stabilityai/sd3.5'),
  prompt: 'Une ville futuriste à l'occident',
  aspectRatio: '16:9',
});
```

<Note>
  Le support des modèles pour les paramètres `size` et `aspectRatio` varie par modèle. Veuillez
  consulter la documentation individuelle du modèle sur [la page des modèles de DeepInfra](https://deepinfra.com/models/text-to-image) pour les options supportées et les paramètres supplémentaires.
</Note>

### Options spécifiques au modèle

Vous pouvez passer des paramètres spécifiques au modèle à l'aide du champ `providerOptions.deepinfra` :

```ts
import { deepinfra } from '@ai-sdk/deepinfra';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: deepinfra.image('stabilityai/sd3.5'),
  prompt: 'Une ville futuriste à l'occident',
  aspectRatio: '16:9',
  providerOptions: {
    deepinfra: {
      num_inference_steps: 30, // Contrôle le nombre d'étapes de débruitage (1-50)
    },
  },
});
```

### Capabilités du Modèle

Pour les modèles supportant les rapports d'aspect, les rapports suivants sont généralement supportés :
`1:1 (par défaut), 16:9, 1:9, 3:2, 2:3, 4:5, 5:4, 9:16, 9:21`

Pour les modèles supportant des paramètres de taille, les dimensions doivent généralement être :

- Multiples de 32
- Largeur et hauteur comprises entre 256 et 1440 pixels
- Taille par défaut est de 1024x1024

| Modèle                              | Spécification des dimensions | Notes                                                    |
| ---------------------------------- | ------------------------ | -------------------------------------------------------- |
| `stabilityai/sd3.5`                | Rapport d'aspect             | Modèle de base premium de haute qualité, 8 milliards de paramètres                |
| `black-forest-labs/FLUX-1.1-pro`   | Taille                     | Modèle d'état de l'art le plus récent avec une suivie de prompt supérieure |
| `black-forest-labs/FLUX-1-schnell` | Taille                     | Génération rapide en 1-4 étapes                             |
| `black-forest-labs/FLUX-1-dev`     | Taille                     | Optimisé pour une précision anatomique                        |
| `black-forest-labs/FLUX-pro`       | Taille                     | Modèle Flux de référence                                      |

| `stabilityai/sd3.5-medium`         | Rapport d'aspect          | Modèle de 2,5 milliards de paramètres équilibré          |
| `stabilityai/sdxl-turbo`           | Rapport d'aspect          | Optimisé pour une génération

Pour plus de détails et d'informations sur les tarifs, voir la [page des modèles text-to-image DeepInfra](https://deepinfra.com/models/text-to-image).

---
titre : Deepgram
description : Découvrez comment utiliser le fournisseur Deepgram pour le SDK AI.
---

---

### Prerequisites

*   Comprendre les concepts de base de l'IA et du

# Fournisseur Deepgram

Le [fournisseur Deepgram](https://deepgram.com/) contient un support de modèle de langage pour l'API de transcription Deepgram.

## Configuration

Le fournisseur Deepgram est disponible dans le module `@ai-sdk/deepgram`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `deepgram` à partir de `@ai-sdk/deepgram` :

```ts
import { deepgram } from '@ai-sdk/deepgram';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createDeepgram` à partir de `@ai-sdk/deepgram` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createDeepgram } from '@ai-sdk/deepgram';

const deepgram = createDeepgram({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Deepgram :

- **apiKey** _chaîne de caractères_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Elle prend par défaut la valeur de la variable d'environnement `DEEPGRAM_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  Elle prend par défaut la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests par exemple.

## Modèles de transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription Deepgram](https://developers.deepgram.com/docs/pre-recorded-audio)
à l'aide de la méthode de fabrication `.transcription()`.

Le premier argument est l'ID du modèle, par exemple `nova-3`.

```ts
const model = deepgram.transcription('nova-3');
```

Vous pouvez également passer des options spécifiques au fournisseur à l'aide de l'argument `providerOptions`. Par exemple, en fournissant l'option `summarize`, vous activez les résumés pour les sections de contenu.

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

Les options de fournisseur suivantes sont disponibles :

- **langue** _chaîne_

  Code de langue pour l'audio.
  Supporte de nombreux codes de langue ISO-639-1 et ISO-639-3.
  Facultatif.

- **smartFormat** _booléen_

  Appliquer la mise en forme intelligente à la transcription.
  Facultatif.

- **punctuate** _booléen_

  Ajouter des signes de ponctuation à la transcription.
  Facultatif.

- **paragraphs** _booléen_

  Formater la transcription en paragraphes.
  Facultatif.

- **summarize** _enum | booléen_

  Générer un résumé de la transcription.
  Valeurs autorisées : `'v2'`, `false`.
  Facultatif.

- **thèmes** _booléen_

  Détection de thèmes dans la transcription.
  Facultatif.

- **intentions** _booléen_

  Détection d'intentions dans la transcription.
  Facultatif.

- **sentiment** _booléen_

  Analyse d'opinion sur la transcription.
  Facultatif.

- **détecterEntités** _booléen_

  Détection d'entités dans la transcription.
  Facultatif.

- **redact** _chaîne de caractères | tableau de chaînes de caractères_

  Spécifie le contenu à supprimer de la transcription.
  Optionnel.

- **replace** _chaîne de caractères_

  Chaîne de remplacement pour le contenu supprimé.
  Optionnel.

- **search** _chaîne de caractères_

  Termes de recherche à trouver dans la transcription.
  Optionnel.

- **keyterm** _chaîne de caractères_

  Termes clés à identifier dans la transcription.
  Optionnel.

- **diarize** _booléen_

  Détermine si les différents locuteurs doivent être identifiés dans la transcription.
  Défaut à `true`.
  Optionnel.

- **utterances** _booléen_

  Détermine si la transcription doit être segmentée en énoncés.
  Optionnel.

- **uttSplit** _nombre_

  Seuil pour la segmentation des énoncés.
  Optionnel.

- **fillerWords** _booléen_

  Détermine si les mots de remplissage (um, uh, etc.) doivent être inclus dans la transcription.
  Optionnel.

### Capabilités du Modèle

| Modèle                                                                                              | Transcription       | Durée            | Segmentations            | Langue            |
| -------------------------------------------------------------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `nova-3` (+ [variantes](https://developers.deepgram.com/docs/models-languages-overview#nova-3))     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `nova-2` (+ [variantes](https://developers.deepgram.com/docs/models-languages-overview#nova-2))     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `nova` (+ [variantes](https://developers.deepgram.com/docs/models-languages-overview#nova))         | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `amélioré` (+ [variantes](https://developers.deepgram.com/docs/models-languages-overview#amélioré)) | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `base` (+ [variantes](https://developers.deepgram.com/docs/models-languages-overview

# base))         | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

---
titre : Gladia
description : Apprenez à utiliser le fournisseur Gladia pour le SDK IA.
---

# Fournisseur Gladia

Le [Gladia](https://gladia.io/) fournit un support pour les modèles de langage de l'API de transcription Gladia.

## Configuration

Le fournisseur Gladia est disponible dans le module `@ai-sdk/gladia`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `gladia` à partir de `@ai-sdk/gladia` :

```ts
import { gladia } from '@ai-sdk/gladia';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createGladia` à partir de `@ai-sdk/gladia` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createGladia } from '@ai-sdk/gladia';

const gladia = createGladia({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Gladia :

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Elle prend par défaut la variable d'environnement `DEEPGRAM_API_KEY`.

- **en-têtes** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  Elle prend par défaut la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour les tests, par exemple.

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription Gladia](https://docs.gladia.io/chapters/pre-recorded-stt/getting-started)
à l'aide de la méthode de fabrication `.transcription()`.

```ts
const model = gladia.transcription();
```

Vous pouvez également passer des options spécifiques au fournisseur à l'aide de l'argument `providerOptions`. Par exemple, en fournissant l'option `summarize`, vous activerez les résumés pour les sections de contenu.

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

<Note>
  Gladia n'a pas de modèles variés, vous pouvez donc omettre le paramètre d'identifiant de modèle standard.
</Note>

Les options de fournisseur suivantes sont disponibles :

- **contextPrompt** _chaîne de caractères_

  Contexte à fournir au modèle de transcription pour une meilleure précision.
  Facultatif.

- **customVocabulary** _booléen | any[]_

  Vocabulaire personnalisé pour améliorer l'exactitude de la transcription.
  Facultatif.

- **customVocabularyConfig** _objet_

  Configuration pour le vocabulaire personnalisé.
  Facultatif.

  - **vocabulary** _Tableau&lt;chaîne de caractères | { value: chaîne de caractères, intensity?: nombre, pronunciations?: chaîne de caractères[], language?: chaîne de caractères }&gt;_
  - **defaultIntensity** _nombre_

- **detectLanguage** _booléen_

  Déterminer automatiquement la langue.
  Facultatif.

- **enableCodeSwitching** _booléen_

  Activer la commutation de code pour les audio multilingues.
  Facultatif.

- **codeSwitchingConfig** _objet_

  Configuration pour la commutation de code.
  Facultatif.

  - **languages** _Tableau de chaînes de caractères_

- **language** _chaîne de caractères_

  Spécifier la langue de l'audio.
  Facultatif.

- **callback** _booléen_

Activer la callback lorsque la transcription est terminée.
  Optionnel.

- **callbackConfig** _objet_

  Configuration pour la callback.
  Optionnel.

  - **url** _chaîne_
  - **method** _'POST' | 'PUT'_

- **sous-titres** _booléen_

  Générer des sous-titres à partir de la transcription.
  Optionnel.

- **sous-titresConfig** _objet_

  Configuration pour les sous-titres.
  Optionnel.

  - **formats** _Tableau&lt;'srt' | 'vtt'&gt;_
  - **minimumDuration** _nombre_
  - **maximumDuration** _nombre_
  - **maximumCharactersPerRow** _nombre_
  - **maximumRowsPerCaption** _nombre_
  - **style** _'default' | 'compliance'_

- **diarisation** _booléen_

  Activer la diarisation des locuteurs.
  Par défaut à `true`.
  Optionnel.

- **diarisationConfig** _objet_

  Configuration pour la diarisation.
  Optionnel.

  - **numberOfSpeakers** _nombre_
  - **minSpeakers** _nombre_
  - **maxSpeakers** _nombre_
  - **enhanced** _booléen_

- **traduction** _booléen_

  Activer la traduction de la transcription.
  Optionnel.

- **traductionConfig** _objet_

  Configuration pour la traduction.
  Optionnel.

  - **targetLanguages** _chaîne[]_
  - **model** _'base' | 'enhanced'_
  - **matchOriginalUtterances** _booléen_

- **résumé** _booléen_

  Activer le résumé de la transcription.
  Optionnel.

- **résuméConfig** _objet_

  Configuration pour le résumé.
  Optionnel.

  - **type** _'general' | 'bullet_points' | 'concise'_

- **modération** _booléen_

  Activer la modération du contenu.
  Optionnel.

- **reconnaissanceDEntitéNommée** _booléen_

  Activer la reconnaissance d'

- **nameConsistency** _boolean_

  Activer la cohérence des noms dans la transcription.
  Facultatif.

- **customSpelling** _boolean_

  Activer la ponctuation personnalisée.
  Facultatif.

- **customSpellingConfig** _object_

  Configuration pour la ponctuation personnalisée.
  Facultatif.

  - **spellingDictionary** _Record&lt;string, string[]&gt;_

- **structuredDataExtraction** _boolean_

  Activer l'extraction de données structurées.
  Facultatif.

- **structuredDataExtractionConfig** _object_

  Configuration pour l'extraction de données structurées.
  Facultatif.

  - **classes** _string[]_

- **sentimentAnalysis** _boolean_

  Activer l'analyse d'opinion.
  Facultatif.

- **audioToLlm** _boolean_

  Activer le traitement audio vers LLM.
  Facultatif.

- **audioToLlmConfig** _object_

  Configuration pour le traitement audio vers LLM.
  Facultatif.

  - **prompts** _string[]_

- **customMetadata** _Record&lt;string, any&gt;_

  Métadonnées personnalisées à inclure avec la requête.
  Facultatif.

- **sentences** _boolean_

  Activer la détection de phrases.
  Facultatif.

- **displayMode** _boolean_

  Activer le mode affichage.
  Facultatif.

- **

### Capacités du Modèle

| Modèle     | Transcription       | Durée            | Segments            | Langue            |
| --------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `Default` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
titre : LMNT
description : Apprenez à utiliser le fournisseur LMNT pour le SDK AI.
---

# Fournisseur LMNT

Le [LMNT](https://lmnt.com/) fournit le support des modèles de langage pour l'API de transcription LMNT.

## Configuration

Le fournisseur LMNT est disponible dans le module `@ai-sdk/lmnt`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `lmnt` à partir de `@ai-sdk/lmnt` :

```ts
import { lmnt } from '@ai-sdk/lmnt';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createLMNT` à partir de `@ai-sdk/lmnt` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createLMNT } from '@ai-sdk/lmnt';

const lmnt = createLMNT({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur LMNT :

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Cela prend par défaut la variable d'environnement `LMNT_API_KEY`.

- **headers** _Record&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de la fonction [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  Cela prend par défaut la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de la fonction fetch pour des tests par exemple.

## Modèles de parole

Vous pouvez créer des modèles qui appellent l'[API de parole LMNT](https://docs.lmnt.com/api-reference/speech/synthesize-speech-bytes)
en utilisant la méthode de fabrication `.speech()`.

La première argument est l'identifiant du modèle par exemple `aurora`.

```ts
const model = lmnt.speech('aurora');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, fournir une voix à utiliser pour l'audio généré.

```ts highlight="6"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { lmnt } from '@ai-sdk/lmnt';

const result = await generateSpeech({
  model: lmnt.speech('aurora'),
  text: 'Bonjour, monde!',
  providerOptions: { lmnt: { language: 'fr' } },
});
```

### Options du fournisseur

Le fournisseur LMNT accepte les options suivantes :

- **model** _'aurora' | 'blizzard'_

  Le modèle LMNT à utiliser. Par défaut, il s'agit de `'aurora'`.

- **language** _'auto' | 'en' | 'es' | 'pt' | 'fr' | 'de' | 'zh' | 'ko' | 'hi' | 'ja' | 'ru' | 'it' | 'tr'_

  La langue à utiliser pour la synthèse vocale. Par défaut, il s'agit de `'auto'`.

- **format** _'aac' | 'mp3' | 'mulaw' | 'raw' | 'wav'_

  Le format audio à retourner. Par défaut, il s'agit de `'mp3'`.

- **sampleRate** _nombre_

  Le taux d'échantillonnage de l'audio en Hz. Par défaut, il s'agit de `24000`.

- **speed** _nombre_

  La vitesse de la parole. Doit être comprise entre 0,25 et 2. Par défaut, il s'agit de `1`.

- **seed** _nombre_

  Un seed optionnel pour une génération déterministe.

- **conversational** _boolean_

  Si utiliser un style de conversation. Par défaut, il s'agit de `false`.

- **length** _nombre_

  La longueur maximale de l'audio en secondes. La valeur maximale est de 300.

- **topP** _nombre_

  Le paramètre de sampling top-p. Doit être compris entre 0 et 1. Par défaut, il s'agit de `1`.

- **temperature** _nombre_

  Le paramètre de température pour le sampling. Doit être au moins de 0. Par défaut, il s'agit de `1`.

### Capabilités du modèle

| Modèle      | Instructions        |
| ---------- | ------------------- |
| `aurora`   | <Check size={18} /> |
| `blizzard` | <Check size={18} /> |

---
titre : Google Generative AI
description : Apprenez à utiliser le fournisseur Google Generative AI.
---

# Fournisseur Google AI Génératif

Le [fournisseur Google AI Génératif](https://ai.google/discover/generativeai/) contient le support de modèle de langage et d'embedding pour les API [Google AI Génératif](https://ai.google.dev/api/rest).

## Configuration

Le fournisseur Google est disponible dans le module `@ai-sdk/google`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance par défaut du fournisseur `google` à partir de `@ai-sdk/google` :

```ts
import { google } from '@ai-sdk/google';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createGoogleGenerativeAI` à partir de `@ai-sdk/google` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createGoogleGenerativeAI } from '@ai-sdk/google';

const google = createGoogleGenerativeAI({
  // paramètres personnalisés
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Google Generative AI :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  Le prefixe par défaut est `https://generativelanguage.googleapis.com/v1beta`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `x-goog-api-key`.
  Elle prend par défaut la valeur de la variable d'environnement `GOOGLE_GENERATIVE_AI_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Les valeurs par défaut sont la fonction de `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de `fetch` personnalisée pour des tests par exemple.

## Modèles de Langage

Vous pouvez créer des modèles qui appellent l'[API de l'intelligence artificielle générative de Google](https://ai.google.dev/api/rest) à l'aide de l'instance du fournisseur.
La première argument est l'ID du modèle, par exemple `gemini-1.5-pro-latest`.
Les modèles supportent les appels d'outils et certains ont des capacités multi-modales.

```ts
const model = google('gemini-1.5-pro-latest');
```

<Note>
  Vous pouvez utiliser des modèles affinés en les précédant de `tunedModels/`,
  par exemple `tunedModels/my-model`.
</Note>

L'intelligence artificielle générative de Google prend également en charge certaines paramètres spécifiques au modèle qui ne font pas partie des [paramètres de l'appel standard](/docs/ai-sdk-core/settings).
Vous pouvez les passer en tant qu'argument d'option :

```ts
const model = google('gemini-1.5-pro-latest', {
  safetySettings: [
    { category: 'HARM_CATEGORY_UNSPECIFIED', threshold: 'BLOCK_LOW_AND_ABOVE' },
  ],
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles de l'intelligence artificielle générative de Google :

- **cachedContent** _chaîne_

  Facultatif. Le nom du contenu stocké utilisé en tant que contexte pour servir la prévision.
  Format : cachedContents/\{cachedContent\}

- **structuredOutputs** _booléen_

  Facultatif. Activer les sorties structurées. Par défaut, c'est vrai.

  Cela est utile lorsque le schéma JSON contient des éléments qui ne sont pas pris en charge par la version de schéma OpenAPI utilisée par
  l'intelligence artificielle générative de Google. Vous pouvez utiliser cela pour désactiver les sorties structurées si vous en avez besoin.

  Voir [Résolution de problèmes : Limites de schéma](

# Limitations du schéma) pour plus de détails.

- **safetySettings** _Array\<\{ category: chaîne de caractères; threshold: chaîne de caractères \}\>_

  Optionnel. Paramètres de sécurité pour le modèle.

  - **category** _chaîne de caractères_

    La catégorie du paramètre de sécurité. Peut être l'une des suivantes :

    - `HARM_CATEGORY_HATE_SPEECH`
    - `HARM_CATEGORY_DANGEREUX_CONTENU`
    - `HARM_CATEGORY_HARCELEMENT`
    - `HARM_CATEGORY_SEXEULEMENT_EXPLICITE`

  - **threshold** _chaîne de caractères_

    Le seuil du paramètre de sécurité. Peut être l'une des suivantes :

    - `HARM_BLOCK_THRESHOLD_UNSPECIFIED`
    - `BLOCK_LOW_AND_ABOVE`
    - `BLOCK_MEDIUM_AND_ABOVE`
    - `BLOCK_ONLY_HIGH`
    - `BLOCK_NONE`

Une configuration supplémentaire peut être effectuée à l'aide des options du fournisseur Google Generative AI. Vous pouvez valider les options du fournisseur à l'aide du type `GoogleGenerativeAIProviderOptions`.

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

Un autre exemple montrant l'utilisation des options du fournisseur pour spécifier le budget de réflexion pour un modèle de réflexion Google Generative AI :

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

Les options de fournisseur suivantes sont disponibles :

- **responseModalities** _string[]_
  Les modalités à utiliser pour la réponse. Les modalités suivantes sont prises en charge : `TEXT`, `IMAGE`. Lorsqu'elles ne sont pas définies ou vides, le modèle par défaut retourne uniquement du texte.

- **thinkingConfig** _\{ thinkingBudget: number; \}_

  Optionnel. Configuration pour le processus de réflexion du modèle. Seuls les modèles de Google Generative AI spécifiques le supportent.

  - **thinkingBudget** _number_

    Optionnel. fournit au modèle des directives sur le nombre de jetons de réflexion qu'il peut utiliser lors de la génération d'une réponse. Doit être un entier compris entre 0 et 24576. Définir cela sur 0 désactive la réflexion. Les budgets compris entre 1 et 1024 jetons seront fixés à 1024.
    Pour plus d'informations, voir la [documentation de Google Generative AI](https://ai.google.dev/gemini-api/docs/thinking).

Vous pouvez utiliser les modèles de langage de Google Generative AI pour générer du texte avec la fonction `generateText` :

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text } = await generateText({
  model: google('gemini-1.5-pro-latest'),
  prompt: 'Écrivez une recette de lasagnes végétariennes pour 4 personnes.',
});
```

Les modèles de langage de Google Generative AI peuvent également être utilisés dans les fonctions `streamText`, `generateObject`, et `streamObject` (voir [AI SDK Core](/docs/ai-sdk-core)).

### Entrées de Fichier

Le fournisseur de l'IA générative de Google prend en charge les entrées de fichier, par exemple des fichiers PDF.

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
          text: 'Quel est un modèle d\'embedding selon ce document ?',
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

<Note>
  Le SDK de l'IA téléchargera automatiquement les URL si vous les passez comme données, sauf
  pour `https://generativelanguage.googleapis.com/v1beta/files/`. Vous pouvez utiliser
  l'API de fichiers de l'IA générative de Google pour télécharger des fichiers plus importants à cet emplacement.
</Note>

Voir [Parties de fichiers](/docs/foundations/prompts#file-parts) pour plus de détails sur la manière d'utiliser les fichiers dans les incitations.

### Contenu Caché

Vous pouvez utiliser les modèles de langage génératifs de Google pour stocker du contenu :

```ts
import { google } from '@ai-sdk/google';
import { GoogleAICacheManager } from '@google/generative-ai/server';
import { generateText } from 'ai';

const cacheManager = new GoogleAICacheManager(
  process.env.GOOGLE_GENERATIVE_AI_API_KEY,
);

// Au 23 août 2024, seuls ces modèles supportent la mise en cache
type GoogleModelCacheableId =
  | 'models/gemini-1.5-flash-001'
  | 'models/gemini-1.5-pro-001';

const model: GoogleModelCacheableId = 'models/gemini-1.5-pro-001';

const { name: contenuCaché } = await cacheManager.create({
  model,
  contents: [
    {
      role: 'user',
      parts: [{ text: '1000 Recettes de Lasagnes...' }],
    },
  ],
  ttlSeconds: 60 * 5,
});

const { text: recetteVégétarienneDeLasagne } = await generateText({
  model: google(model, { contenuCaché }),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});

const { text: recetteDeLasagneAuViande } = await generateText({
  model: google(model, { contenuCaché }),
  prompt: 'Écrivez une recette de lasagne au viande pour 12 personnes.',
});
```

### Recherche de fondement

Avec [la recherche de fondement](https://ai.google.dev/gemini-api/docs/grounding),
le modèle a accès à l'information la plus récente en utilisant Google recherche.
La recherche de fondement peut être utilisée pour fournir des réponses autour d'événements actuels :

```ts highlight="7,14-20"
import { google } from '@ai-sdk/google';
import { GoogleGenerativeAIProviderMetadata } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text, providerMetadata } = await generateText({
  model: google('gemini-1.5-pro', {
    useSearchGrounding: true,
  }),
  prompt:
    'Listez les 5 premiers news de San Francisco de la semaine passée.' +
    'Vous devez inclure la date de chaque article.',
});

// accédez aux métadonnées de fondement. Le casting vers le type de métadonnées de fournisseur
// est facultatif mais fournit l'autocomplétion et la sécurité de type.
const metadata = providerMetadata?.google as
  | GoogleGenerativeAIProviderMetadata
  | undefined;
const groundingMetadata = metadata?.groundingMetadata;
const safetyRatings = metadata?.safetyRatings;
```

Les métadonnées de fondement incluent des informations détaillées sur la manière dont les résultats de recherche ont été utilisés pour fonder la réponse du modèle. Voici les champs disponibles :

- **`webSearchQueries`** (`string[] | null`)

  - Tableau des requêtes de recherche utilisées pour récupérer des informations
  - Exemple : `["Quel est le temps à Chicago ce week-end ?"]`

- **`searchEntryPoint`** (`{ renderedContent: string } | null`)

  - Contient le contenu principal du résultat de recherche utilisé comme point d'entrée
  - Le champ `renderedContent` contient le contenu formatté

- **`groundingSupports`** (Tableau d'objets de support | null)
  - Contient des détails sur la manière dont certaines parties de réponse sont prises en charge par les résultats de recherche
  - Chaque objet de support inclut :
    - **`segment`** : Informations sur le segment de texte ancré
      - `text` : Le segment de texte réel
      - `startIndex` : Position de début dans la réponse
      - `endIndex` : Position de fin dans la réponse
    - **`groundingChunkIndices`** : Références aux tronçons de recherche de support
    - **`confidenceScores`** : Scores de confiance (0-1) pour chaque tronçon de support

Exemple de réponse :

```json
{
  "groundingMetadata": {
    "webSearchQueries": ["Quel est le temps à Chicago ce week-end?"],
    "searchEntryPoint": {
      "renderedContent": "..."
    },
    "groundingSupports": [
      {
        "segment": {
          "startIndex": 0,
          "endIndex": 65,
          "text": "Le temps à Chicago change rapidement, vous pouvez donc ajuster facilement."
        },
        "groundingChunkIndices": [0],
        "confidenceScores": [0.99]
      }
    ]
  }
}
```

#### Récupération Dynamique

Avec [la récupération dynamique](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-with-google-search#dynamic-retrieval), vous pouvez configurer comment le modèle décide de lancer Grounding avec Google Search. Cela vous donne plus de contrôle sur quand et comment le modèle ancre ses réponses.

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
  prompt: 'Qui a gagné le dernier grand prix de Formule 1 ?',
});
```

La configuration `dynamicRetrieval` décrit les options pour personnaliser la récupération dynamique :

- `mode`: Le mode du prédicteur à utiliser pour la récupération dynamique. Les modes suivants sont pris en charge :

  - `MODE_DYNAMIC`: Effectuer la récupération uniquement lorsque le système décide qu'il est nécessaire
  - `MODE_UNSPECIFIED`: Déclencher toujours la récupération

- `dynamicThreshold`: Le seuil à utiliser pour la récupération dynamique (si non défini, une valeur par défaut système est utilisée).

<Note>
  La récupération dynamique n'est disponible que avec les modèles Gemini 1.5 Flash et n'est pas prise en charge avec les variantes 8B.
</Note>

### Sources

Lorsque vous utilisez [Grounding de recherche](

# Recherche de sources
Le modèle inclura les sources dans la réponse.
Vous pouvez y accéder à l'aide de la propriété `sources` du résultat :

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const { sources } = await generateText({
  model: google('gemini-2.0-flash-exp', { useSearchGrounding: true }),
  prompt: 'Listez les 5 premières actualités de San Francisco de la semaine passée.',
});
```

### Sorties d'images

Le modèle `gemini-2.0-flash-exp` prend en charge la génération d'images. Les images sont exposées sous forme de fichiers dans la réponse.
Vous devez activer la sortie d'image dans les options du fournisseur à l'aide de l'option `responseModalities`.

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const result = await generateText({
  model: google('gemini-2.0-flash-exp'),
  providerOptions: {
    google: { responseModalities: ['TEXT', 'IMAGE'] },
  },
  prompt: 'Générez une image d\'un chat comique',
});

for (const file of result.files) {
  if (file.mimeType.startsWith('image/')) {
    // affichez l\'image
  }
}
```

### Évaluation de la Sécurité

Les évaluations de la sécurité fournissent des informations sur la sécurité de la réponse du modèle.
Voir [la documentation Google AI sur les paramètres de sécurité](https://ai.google.dev/gemini-api/docs/safety-settings).

Extrait d'exemple de réponse :

```json
{
  "notesDeSécurité" : [
    {
      "catégorie" : "HARM_CATEGORY_HATE_SPEECH",
      "probabilité" : "NEGLIGIBLE",
      "scoreDeProbabilité" : 0,11027937,
      "gravité" : "HARM_SEVERITY_LOW",
      "scoreDeGravité" : 0,28487435
    },
    {
      "catégorie" : "HARM_CATEGORY_DANGEROUS_CONTENT",
      "probabilité" : "HIGH",
      "bloqué" : true,
      "scoreDeProbabilité" : 0,95422274,
      "gravité" : "HARM_SEVERITY_MEDIUM",
      "scoreDeGravité" : 0,43398145


### Dépannage

#### Limites du schéma

L'API de l'intelligence artificielle générative de Google utilise un sous-ensemble du schéma OpenAPI 3.0,
qui ne prend pas en charge des fonctionnalités telles que les unions.
Les erreurs que vous obtenez dans ce cas ressemblent à ceci :

`GenerateContentRequest.generation_config.response_schema.properties[occupation].type: must be specified`

Par défaut, les sorties structurées sont activées (et pour les appels de fonction elles sont requises).
Vous pouvez désactiver les sorties structurées pour la génération d'objets comme un travailaround :

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
  prompt: 'Générez un exemple de personne pour la test.',
});
```

Les fonctionnalités suivantes de Zod sont connues pour ne pas fonctionner avec Google Generative AI :

- `z.union`
- `z.record`

### Capacités du Modèle

### Description

| Modèle                            | Entrée d'image         | Génération d'objet   | Utilisation de l'outil          | Flux d'outil Streaming      |
| -------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `gemini-2.5-pro-preview-05-06`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.5-flash-preview-04-17` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.5-pro-exp-03-25`       | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-2.0-flash`               | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-pro`                 | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-pro-latest`          | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `gemini-1.5-flash`               | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

| `gemini-1.5-flash-latest`        | <Vérifie size={18} /> | <Vérifie size={18} /> | <Vérifie size={18} /> | <Vérifie size={18} /> |
| `gemini-1.5-flash-8b`            | <Vérifie size={18} /> | <Vérifie size={18} /> | <Vérifie size={18} /> | <Vérifie size={18} /> |
| `gemini-1.5-flash-8b-latest`     | <Vérifie size={18} /> | <Vérifie size={18} /> | <Vérifie size={18} /> | <Vérifie size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter les [docs de l'IA
  générative de Google](https://ai.google.dev/gemini-api/docs/models/gemini) pour
  une liste complète des modèles disponibles. La table ci-dessus liste les modèles
  populaires. Vous pouvez également passer l'ID du modèle d'un fournisseur disponible
  sous forme de chaîne si nécessaire.
</Note>

## Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'[API d'embeddings de l'intelligence artificielle générative de Google](https://ai.google.dev/api/embeddings)
en utilisant la méthode de fabrication `.textEmbeddingModel()`.

```ts
const model = google.textEmbeddingModel('text-embedding-004');
```

Les modèles d'embeddings de l'intelligence artificielle générative de Google supportent des paramètres supplémentaires. Vous pouvez les passer en tant qu'argument d'option :

```ts
const model = google.textEmbeddingModel('text-embedding-004', {
  outputDimensionality: 512, // optionnel, nombre de dimensions pour l'embedding
  taskType: 'SIMILARITE_SEMANTIQUE', // optionnel, spécifie le type de tâche pour générer les embeddings
});
```

Les paramètres optionnels suivants sont disponibles pour les modèles d'embeddings de l'intelligence artificielle générative de Google :

- **outputDimensionality**: _nombre_

  Dimensionnalité réduite facultative pour l'embedding de sortie. Si défini, les valeurs excessives de l'embedding de sortie sont tronquées de la fin.

- **taskType**: _chaîne_

  Optionnel. Spécifie le type de tâche pour générer les embeddings. Les types de tâche pris en charge incluent :

  - `SIMILARITE_SEMANTIQUE` : Optimisé pour la similarité de texte.
  - `CLASSIFICATION` : Optimisé pour la classification de texte.
  - `AGRUPPEMENT` : Optimisé pour grouper les textes en fonction de la similarité.
  - `RETRIEVAL_DOCUMENT` : Optimisé pour la récupération de documents.
  - `RETRIEVAL_QUERY` : Optimisé pour la récupération basée sur des requêtes.
  - `REPONSE_QUESTION` : Optimisé pour répondre aux questions.
  - `VERIFICATION_FAIT` : Optimisé pour vérifier des informations factuelles.
  - `RETRIEVAL_QUERY_CODE` : Optimisé pour récupérer des blocs de code en fonction de requêtes naturelles.

### Capacités du Modèle

| Modèle                | Dimensions par Défaut | Dimensions personnalisées   |
| -------------------- | ------------------ | --------------------------- |
| `text-embedding-004` | 768                | <Check size={18} /> |

---
titre : Hume
description : Apprenez à utiliser le fournisseur Hume pour le SDK AI.
---

# Fournisseur Hume

Le [Hume](https://hume.ai/) fournit le support des modèles de langage pour l'API de transcription Hume.

## Configuration

Le fournisseur Hume est disponible dans le module `@ai-sdk/hume`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `hume` à partir de `@ai-sdk/hume` :

```ts
import { hume } from '@ai-sdk/hume';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createHume` à partir de `@ai-sdk/hume` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createHume } from '@ai-sdk/hume';

const hume = createHume({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Hume :

- **apiKey** _chaîne_

  Clé API qui est envoyée à l'aide de l'en-tête `Authorization`.
  Elle prend par défaut la valeur de la variable d'environnement `HUME_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input : RequestInfo, init ?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Elle prend par défaut la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests par exemple.

## Modèles de parole

Vous pouvez créer des modèles qui appellent l'[API de parole Hume](https://dev.hume.ai/docs/text-to-speech-tts/overview)
en utilisant la méthode de fabrication `.speech()`.

```ts
const model = hume.speech();
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, en fournissant une voix à utiliser pour l'audio généré.

```ts highlight="6"
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { hume } from '@ai-sdk/hume';

const result = await generateSpeech({
  model: hume.speech(),
  text: 'Bonjour, monde!',
  voice: 'd8ab67c6-953d-4bd8-9370-8fa53a0f1453',
  providerOptions: { hume: {} },
});
```

Les options de fournisseur suivantes sont disponibles :

- **context** _objet_

  Soit :

  - `{ generationId: string }` - Un ID de génération à utiliser pour le contexte.
  - `{ utterances: HumeUtterance[] }` - Un tableau d'objets d'expression pour le contexte.

### Capacités du modèle

| Modèle     | Instructions        |
| --------- | ------------------- |
| `default` | <Check size={18} /> |

---
titre : Google Vertex AI
description : Apprenez à utiliser le fournisseur Google Vertex AI.
---

# Fournisseur Google Vertex

Le fournisseur Google Vertex pour le [SDK AI](/docs) contient le support des modèles de langage pour les API [Google Vertex AI](https://cloud.google.com/vertex-ai). Cela inclut le support pour les [modèles Gemini de Google](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models) et les [modèles partenaires Anthropic Claude](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).

<Note>
  Le fournisseur Google Vertex est compatible avec les deux environnements Node.js et Edge.
  L'environnement Edge est pris en charge grâce à la sous-module `@ai-sdk/google-vertex/edge`.
  Plus de détails peuvent être trouvés dans la section [Google Vertex Edge Runtime](#google-vertex-edge-runtime) et [Google Vertex Anthropic Edge Runtime](#google-vertex-anthropic-edge-runtime) ci-dessous.
</Note>

## Installation

Le fournisseur Google Vertex et le fournisseur Google Vertex Anthropic sont tous deux disponibles dans la module `@ai-sdk/google-vertex`. Vous pouvez l'installer avec

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

## Utilisation du fournisseur Google Vertex

L'instance du fournisseur Google Vertex est utilisée pour créer des instances de modèle qui appellent l'API Vertex AI. Les modèles disponibles avec ce fournisseur incluent [les modèles Gemini de Google](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models). Si vous cherchez à utiliser [les modèles Claude d'Anthropic](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude), voir la section [Utilisation du fournisseur Google Vertex Anthropic](#utilisation-du-fournisseur-google-vertex-anthropic) ci-dessous.

### Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `vertex` à partir de `@ai-sdk/google-vertex` :

```ts
import { vertex } from '@ai-sdk/google-vertex';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createVertex` à partir de `@ai-sdk/google-vertex` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createVertex } from '@ai-sdk/google-vertex';

const vertex = createVertex({
  projet : 'mon-projet', // facultatif
  emplacement : 'us-central1', // facultatif
});
```

Google Vertex prend en charge deux implémentations d'authentification différentes en fonction de votre environnement de runtime.

#### Environnement de runtime Node.js

L'environnement de runtime Node.js est le runtime par défaut pris en charge par le SDK AI. Il prend en charge toutes les options d'authentification Google Cloud standard à travers la bibliothèque `google-auth-library` : <https://github.com/googleapis/google-auth-library-nodejs?tab=readme-ov-file

# Façons d'authentifier

La mise en œuvre typique consiste à définir un chemin vers un fichier de fichiers de fichiers json de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fichiers de fich

# L87C18-L87C35) interface.

  - **authClient** _objet_
    Un `AuthClient` à utiliser.

  - **keyFilename** _chaîne_
    Chemin vers un fichier de clé .json, .pem ou .p12.

  - **keyFile** _chaîne_
    Chemin vers un fichier de clé .json, .pem ou .p12.

  - **credentials** _objet_
    Objet contenant les propriétés client_email et private_key, ou les options de compte externe.

  - **clientOptions** _objet_
    Options objet passé au constructeur du client.

  - **scopes** _chaîne | chaîne[]_
    Étendues requises pour la demande API souhaitée.

  - **projectId** _chaîne_
    Votre ID de projet.

  - **universeDomain** _chaîne_
    Le domaine de service par défaut pour un univers Cloud donné.

- **en-têtes** _Resolvable&lt;Record&lt;chaîne, chaîne | indéfini&gt;&gt;_

  En-têtes à inclure dans les requêtes. Ils peuvent être fournis sous plusieurs formats :

  - Un enregistrement de paires clé-valeur d'en-tête : `Record<string, string | undefined>`
  - Une fonction qui retourne les en-têtes : `() => Record<string, string | undefined>`
  - Une fonction asynchrone qui retourne les en-têtes : `async () => Record<string, string | undefined>`
  - Une promesse qui se résout en en-têtes : `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Par défaut, elle utilise la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour la mise au point.

- **baseURL** _chaîne_

Optionnel. URL de base pour les appels de l'API Google Vertex, par exemple pour utiliser des serveurs proxy. Par défaut, elle est construite à partir de la localisation et du projet :
  `https://${location}-aiplatform.googleapis.com/v1/projects/${project}/locations/${location}/publishers/google`

<a id="google-vertex-edge-runtime"></a>

#### Edge Runtime

Les runtimes Edge (comme Vercel Edge Functions et Cloudflare Workers) sont des environnements JavaScript légers qui s'exécutent plus près des utilisateurs au niveau de l'edge du réseau.
Ils ne fournissent qu'un sous-ensemble des API Node.js standard.
Par exemple, l'accès direct au système de fichiers n'est pas disponible, et de nombreuses bibliothèques Node.js spécifiques
(inclus la bibliothèque d'authentification Google standard) ne sont pas compatibles.

La version du runtime Edge du fournisseur Google Vertex prend en charge les [Credentials par défaut d'Application](https://github.com/googleapis/google-auth-library-nodejs?tab=readme-ov-file) de Google.

# application-default-credentials) à travers les variables d'environnement. Les valeurs peuvent être obtenues à partir d'un fichier JSON de fichiers de connexion de `Google Cloud Console` <https://console.cloud.google.com/apis/credentials>.

Vous pouvez importer l'instance de fournisseur par défaut `vertex` de `@ai-sdk/google-vertex/edge` :

```ts
import { vertex } from '@ai-sdk/google-vertex/edge';
```

<Note>
  Le sous-module `/edge` est inclus dans le package `@ai-sdk/google-vertex`, vous n'avez donc pas besoin de l'installer séparément. Vous devez importer à partir de `@ai-sdk/google-vertex/edge` pour le différencier du fournisseur Node.js.
</Note>

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createVertex` de `@ai-sdk/google-vertex/edge` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createVertex } from '@ai-sdk/google-vertex/edge';

const vertex = createVertex({
  projet : 'mon-projet', // facultatif
  emplacement : 'us-central1', // facultatif
});
```

Pour l'authentification de la runtime Edge, vous aurez besoin de définir ces variables d'environnement à partir du fichier JSON de fichiers de connexion de l'application Google par défaut :

- `GOOGLE_CLIENT_EMAIL`
- `GOOGLE_PRIVATE_KEY`
- `GOOGLE_PRIVATE_KEY_ID` (facultatif)

Ces valeurs peuvent être obtenues à partir d'un fichier JSON de compte de service de `Google Cloud Console` <https://console.cloud.google.com/apis/credentials>.

#### Paramètres de fournisseur optionnels

Vous pouvez utiliser les paramètres suivants pour personnaliser l'instance du fournisseur :

- **projet** _chaîne_

  L'ID du projet Google Cloud que vous souhaitez utiliser pour les appels API.
  Il utilise par défaut la variable d'environnement `GOOGLE_VERTEX_PROJECT`.

- **emplacement** _chaîne_

  L'emplacement Google Cloud que vous souhaitez utiliser pour les appels API, par exemple `us-central1`.
  Il utilise par défaut la variable d'environnement `GOOGLE_VERTEX_LOCATION`.

- **googleCredentials** _objet_

  Facultatif. Les informations d'identification utilisées par le fournisseur Edge pour l'authentification. Ces informations d'identification sont généralement définies à l'aide de variables d'environnement et sont dérivées d'un fichier JSON de compte de service.

  - **clientEmail** _chaîne_
    L'adresse e-mail du client du fichier JSON de compte de service. Par défaut, il utilise la valeur de la variable d'environnement `GOOGLE_CLIENT_EMAIL`.

  - **privateKey** _chaîne_
    La clé privée du fichier JSON de compte de service. Par défaut, il utilise la valeur de la variable d'environnement `GOOGLE_PRIVATE_KEY`.

  - **privateKeyId** _chaîne_
    L'ID de la clé privée du fichier JSON de compte de service (facultatif). Par défaut, il utilise la valeur de la variable d'environnement `GOOGLE_PRIVATE_KEY_ID`.

- **en-têtes** _Resolvable&lt;Record&lt;chaîne, chaîne | indefini&gt;&gt;_

  Les en-têtes à inclure dans les requêtes. Ils peuvent être fournis sous différentes formes :

  - Un enregistrement de paires clé-valeur d'en-tête : `Record<string, string | undefined>`
  - Une fonction qui retourne les en-têtes : `() => Record<string, string | undefined>`
  - Une fonction asynchrone qui retourne les en-têtes : `async () => Record<string, string | undefined>`
  - Une promesse qui se résout en en-têtes : `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

Implémentation personnalisée de [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  Par défaut, elle utilise la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de `fetch` pour les tests par exemple.

### Modèles de Langue

Vous pouvez créer des modèles qui appellent l'API Vertex à l'aide de l'instance du fournisseur.
La première argument est l'identifiant du modèle, par exemple `gemini-1.5-pro`.

```ts
const model = vertex('gemini-1.5-pro');
```

<Note>
  Si vous utilisez des [modèles personnalisés](https://cloud.google.com/vertex-ai/docs/training-overview), le nom de votre modèle doit commencer par `projects/`.
</Note>

Les modèles de Vertex Google prennent également en charge certaines paramètres spécifiques au modèle qui ne font pas partie des [paramètres de configuration standard](/docs/ai-sdk-core/settings). Vous pouvez les passer en tant qu'argument d'option :

```ts
const model = vertex('gemini-1.5-pro', {
  safetySettings: [
    { category: 'HARM_CATEGORY_UNSPECIFIED', threshold: 'BLOCK_LOW_AND_ABOVE' },
  ],
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles de Vertex Google :

- **structuredOutputs** _boolean_

  Facultatif. Activer les sorties structurées. La valeur par défaut est true.

  Cela est utile lorsque le schéma JSON contient des éléments qui ne sont pas pris en charge par la version du schéma OpenAPI utilisée par Vertex Google. Vous pouvez utiliser cela pour désactiver les sorties structurées si vous en avez besoin.

  Voir [Résolution des problèmes : Limitations de schéma](

# Limitations du schéma) pour plus de détails.

- **safetySettings** _Array\<\{ category: string; threshold: string \}\>_

  Optionnel. Paramètres de sécurité pour le modèle.

  - **category** _string_

    La catégorie du paramètre de sécurité. Peut être l'une des suivantes :

    - `HARM_CATEGORY_UNSPECIFIED`
    - `HARM_CATEGORY_HATE_SPEECH`
    - `HARM_CATEGORY_DANGEREUX_CONTENU`
    - `HARM_CATEGORY_HARCELEMENT`
    - `HARM_CATEGORY_EXPLICITE_SEXE`
    - `HARM_CATEGORY_CIVIQUE_INTEGRITE`

  - **threshold** _string_

    Le seuil du paramètre de sécurité. Peut être l'une des suivantes :

    - `HARM_BLOCK_THRESHOLD_UNSPECIFIED`
    - `BLOCK_LOW_AND_ABOVE`
    - `BLOCK_MEDIUM_AND_ABOVE`
    - `BLOCK_ONLY_HIGH`
    - `BLOCK_NONE`

- **useSearchGrounding** _boolean_

  Optionnel. Lorsque cette option est activée, le modèle utilisera [Google recherche pour ancrer la réponse](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview).

- **audioTimestamp** _boolean_

  Optionnel. Active la compréhension des horodatages pour les fichiers audio. Par défaut, il est défini sur false.

  Cela est utile pour générer des transcriptions avec des horodatages précis.
  Consultez [la documentation de Google](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/audio-understanding) pour plus de détails.

Vous pouvez utiliser les modèles de langage Google Vertex pour générer du texte avec la fonction `generateText` :

```ts highlight="1,4"
import { vertex } from '@ai-sdk/google-vertex';
import { generateText } from 'ai';


```markdown
const { text } = await generateText({
  model: vertex('gemini-1.5-pro'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage Google Vertex peuvent également être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

#### Raisonnement (Jetons de Pensée)

Google Vertex AI, grâce à son support pour les modèles Gemini, peut également émettre des "jetons de pensée", représentant le processus de raisonnement du modèle. La bibliothèque SDK de l'IA expose ces informations sous forme de raisonnement.

Pour activer les jetons de pensée pour les modèles Gemini compatibles via Vertex, définissez `includeThoughts: true` dans l'option de configuration `thinkingConfig` du fournisseur. Puisque le fournisseur Vertex utilise le modèle de langage sous-jacent du fournisseur Google, ces options sont transmises via `providerOptions.google` :

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { GoogleGenerativeAIProviderOptions } from '@ai-sdk/google'; // Note : importer depuis @ai-sdk/google
import { generateText, streamText } from 'ai';

// Pour generateText :
const { text, raisonnement, detailsDeRaisonnement } = await generateText({
  model: vertex('gemini-2.5-flash-preview-04-17'), // Ou autre modèle pris en charge via Vertex
  providerOptions: {
    google: {
      // Les options sont imbriquées sous 'google' pour le fournisseur Vertex
      thinkingConfig: {
        includeThoughts: true,
        // thinkingBudget: 2048, // Optionnel
      },
    } satisfies GoogleGenerativeAIProviderOptions,
  },
  prompt: 'Expliquez le calcul quantique en termes simples.',
});

console.log('Raisonnement :', raisonnement);
console.log('Détails de raisonnement :', detailsDeRaisonnement);
console.log('Texte final :', text);
```

// Pour streamText :
const result = streamText({
  model: vertex('gemini-2.5-flash-preview-04-17'), // Ou autre modèle pris en charge via Vertex
  providerOptions: {
    google: {
      // Les options sont imbriquées sous 'google' pour le fournisseur Vertex
      thinkingConfig: {
        includeThoughts: true,
        // thinkingBudget: 2048, // Optionnel
      },
    } satisfies GoogleGenerativeAIProviderOptions,
  },
  prompt: 'Expliquez le calcul quantique en termes simples.',
});

for await (const part of result.fullStream) {
  if (part.type === 'reasoning') {
    process.stdout.write(`PENSÉE : ${part.textDelta}\n`);
  } else if (part.type === 'text-delta') {
    process.stdout.write(part.textDelta);
  }
}

<Remarque>
  Référez-vous à la [documentation de Google Vertex AI sur "thinking"](https://cloud.google.com/vertex-ai/generative-ai/docs/thinking)
  pour la compatibilité des modèles et plus de détails.
</Remarque>

#### Entrées de Fichier

Le fournisseur Google Vertex prend en charge les entrées de fichier, par exemple des fichiers PDF.

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
          text: 'Quel est un modèle d\'embedding selon ce document ?',
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

<Note>
  Le SDK IA téléchargera automatiquement les URL si vous les passez comme données, excepté les URL `gs://`. Vous pouvez utiliser l'API Google Cloud Storage pour télécharger des fichiers plus volumineux à cette emplacement.
</Note>

Voir [Parties de Fichier](/docs/foundations/prompts#file-parts) pour plus de détails sur la manière d'utiliser les fichiers dans les incitations.

#### Recherche de Rattachement

Avec [la recherche de rattachement](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview),
le modèle a accès à l'information la plus récente en utilisant Google recherche.
La recherche de rattachement peut être utilisée pour fournir des réponses autour d'événements actuels :

```ts highlight="7,14-20"
import { vertex } from '@ai-sdk/google-vertex';
import { GoogleGenerativeAIProviderMetadata } from '@ai-sdk/google';
import { generateText } from 'ai';

const { text, providerMetadata } = await generateText({
  model: vertex('gemini-1.5-pro', {
    useSearchGrounding: true,
  }),
  prompt:
    'Listez les 5 premiers actualités de San Francisco de la semaine dernière.' +
    'Vous devez inclure la date de chaque article.',
});

// accéder aux métadonnées de rattachement. Le casting vers le type de métadonnées du fournisseur
// est facultatif mais fournit l'autocomplétion et la sécurité de type.
const metadata = providerMetadata?.google as
  | GoogleGenerativeAIProviderMetadata
  | undefined;
const groundingMetadata = metadata?.groundingMetadata;
const safetyRatings = metadata?.safetyRatings;
```

Les métadonnées de rattachement incluent des informations détaillées sur la manière dont les résultats de recherche ont été utilisés pour rattacher la réponse du modèle. Voici les champs disponibles :

- **`webSearchQueries`** (`string[] | null`)

  - Tableau d'opérations de recherche utilisées pour récupérer des informations
  - Exemple : `["Quel est le temps à Chicago ce week-end?"]`

- **`searchEntryPoint`** (`{ renderedContent: string } | null`)

  - Contient le contenu principal du résultat de recherche utilisé comme point d'entrée
  - Le champ `renderedContent` contient le contenu formatté

- **`groundingSupports`** (Tableau d'objets de support | null)
  - Contient des détails sur la manière dont certaines parties de réponse sont prises en charge par les résultats de recherche
  - Chaque objet de support comprend :
    - **`segment`** : Informations sur le segment de texte ancré
      - `text` : Le segment de texte réel
      - `startIndex` : Position de début dans la réponse
      - `endIndex` : Position de fin dans la réponse
    - **`groundingChunkIndices`** : Références aux tronçons de recherche de support
    - **`confidenceScores`** : Scores de confiance (0-1) pour chaque tronçon de support

Extrait de réponse d'exemple :

```json
{
  "groundingMetadata": {
    "retrievalQueries": ["Quel est le temps à Chicago ce week-end?"],
    "searchEntryPoint": {
      "renderedContent": "..."
    },
    "groundingSupports": [
      {
        "segment": {
          "startIndex": 0,
          "endIndex": 65,
          "text": "Le temps à Chicago change rapidement, il est donc facile de s'adapter en portant des couches."
        },
        "groundingChunkIndices": [0],
        "confidenceScores": [0,99]
      }
    ]
  }
}
```

<Note>
  Le fournisseur Google Vertex ne prend pas encore en charge le mode de récupération dynamique et le seuil.

# Récupération Dynamique).
</Note>

### Sources

Lorsque vous utilisez [Search Grounding](#search-grounding), le modèle inclura les sources dans la réponse.
Vous pouvez y accéder en utilisant la propriété `sources` du résultat :

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { generateText } from 'ai';

const { sources } = await generateText({
  model: vertex('gemini-1.5-pro', { useSearchGrounding: true }),
  prompt: 'Listez les 5 premiers articles de San Francisco des dernières semaines.',
});
```

### Évaluations de Sécurité

Les évaluations de sécurité fournissent des informations sur la sécurité de la réponse du modèle.
Voir la [documentation de Google Vertex AI sur la configuration des filtres de sécurité](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters).

Extrait d'exemple de réponse :

```json
{
  "notesDeSécurité" : [
    {
      "catégorie" : "HARM_CATEGORY_HATE_SPEECH",
      "probabilité" : "NEGLIGIBLE",
      "scoreDeProbabilité" : 0,11027937,
      "gravité" : "HARM_SEVERITY_LOW",
      "scoreDeGravité" : 0,28487435
    },
    {
      "catégorie" : "HARM_CATEGORY_DANGEROUS_CONTENT",
      "probabilité" : "HIGH",
      "bloqué" : true,
      "scoreDeProbabilité" : 0,95422274,
      "gravité" : "HARM_SEVERITY_MEDIUM",
      "scoreDeGravité" : 0,43398145


Pour plus de détails, voir la [documentation de Google Vertex AI sur l'ancrage avec Google Search](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/

# Recherche à partir du sol).

### Dépannage

#### Limites du schéma

L'API Google Vertex utilise un sous-ensemble du schéma OpenAPI 3.0,
qui ne prend pas en charge des fonctionnalités telles que les unions.
Les erreurs que vous obtenez dans ce cas ressemblent à ceci :

`GenerateContentRequest.generation_config.response_schema.properties[occupation].type: must be specified`

Par défaut, les sorties structurées sont activées (et pour les appels de boutons, elles sont requises).
Vous pouvez désactiver les sorties structurées pour la génération d'objets en tant que workaround :

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
  prompt: 'Générer un exemple de personne pour les tests.',
});
```

Les fonctionnalités suivantes de Zod sont connues pour ne pas fonctionner avec Google Vertex :

- `z.union`
- `z.record`

### Capacités du Modèle

| Modèle                  | Entrée d'image         | Génération d'objets   | Utilisation d'outil          | Flux d'outil           |
| ---------------------- | ------------------- | ------------------- | --------------------------- | --------------------- |
| `gemini-2.0-flash-001` | <Check size={18} /> | <Check size={18} /> | <Check size={18} />          | <Check size={18} />   |
| `gemini-2.0-flash-exp` | <Check size={18} /> | <Check size={18} /> | <Check size={18} />          | <Check size={18} />   |
| `gemini-1.5-flash`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} />          | <Check size={18} />   |
| `gemini-1.5-pro`       | <Check size={18} /> | <Check size={18} /> | <Check size={18} />          | <Check size={18} />   |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter la [documentation
  Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#supported-models)
  pour une liste complète des modèles disponibles. La table ci-dessus liste les
  modèles populaires. Vous pouvez également passer l'ID du modèle de fournisseur
  disponible en tant que chaîne si nécessaire.
</Note>

### Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'API d'embeddings de Google Vertex AI à l'aide de la méthode de fabrication `.textEmbeddingModel()` :

```ts
const model = vertex.textEmbeddingModel('text-embedding-004');
```

Les modèles d'embeddings de Google Vertex AI prennent en charge des paramètres supplémentaires. Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = vertex.textEmbeddingModel('text-embedding-004', {
  outputDimensionality: 512, // optionnel, nombre de dimensions pour l'embedding
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles d'embeddings de Google Vertex AI :

- **outputDimensionality** : _nombre_

  Dimensionnalité réduite facultative pour l'embedding de sortie. Si défini, les valeurs excessives de l'embedding de sortie sont tronquées de la fin.

#### Capacités du Modèle

| Modèle                | Max Values Par Appel | Appels Parallèles      |
| -------------------- | ------------------- | ------------------- |
| `text-embedding-004` | 2048                | <Check size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID de n'importe quel modèle de fournisseur disponible en tant que chaîne si nécessaire.
</Note>

### Modèles d'images

Vous pouvez créer des modèles [Imagen](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview) qui appellent l'[API Imagen sur Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images)
en utilisant la méthode de fabrication `.image()`. Pour plus d'informations sur la génération d'images avec le SDK AI, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: vertex.image('imagen-3.0-generate-002'),
  prompt: 'Une ville futuriste au coucher du soleil',
  aspectRatio: '16:9',
});
```

Une configuration supplémentaire peut être effectuée en utilisant les options du fournisseur Google Vertex. Vous pouvez valider les options du fournisseur en utilisant le type `GoogleVertexImageProviderOptions`.

```ts
import { vertex } from '@ai-sdk/google-vertex';
import { GoogleVertexImageProviderOptions } from '@ai-sdk/google-vertex';
import { generateImage } from 'ai';

const { image } = await generateImage({
  model: vertex.image('imagen-3.0-generate-002'),
  providerOptions: {
    vertex: {
      negativePrompt: 'pixelé, flou, de mauvaise qualité',
    } satisfies GoogleVertexImageProviderOptions,
  },
  // ...
});
```

Les options de fournisseur suivantes sont disponibles :

- **negativePrompt** _chaîne_
  Une description de ce que l'on doit dissuader dans les images générées.

- **personGeneration** `allow_adult` | `allow_all` | `dont_allow`
  Si on doit autoriser la génération de personnes. Par défaut, `allow_adult`.

- **safetySetting** `block_low_and_above` | `block_medium_and_above` | `block_only_high` | `block_none`
  Déterminer si le contenu non sécurisé doit être bloqué. Par défaut, il est bloqué à partir de `block_medium_and_above`.

- **addWatermark** _boolean_
  Déterminer si ajouter une eau-forte invisible aux images générées. Par défaut, il est défini sur `true`.

- **storageUri** _string_
  URI de stockage Cloud pour stocker les images générées.

<Note>
  Les modèles d'images ne supportent pas le paramètre `size`. Utilisez le paramètre `aspectRatio` à la place.
</Note>

#### Capacités du Modèle

| Modèle                          | Rapports d'Aspect             |
| ------------------------------ | ------------------------- |
| `imagen-3.0-generate-002`      | 1:1, 3:4, 4:3, 9:16, 16:9 |
| `imagen-3.0-fast-generate-001` | 1:1, 3:4, 4:3, 9:16, 16:9 |

## Utilisation du Fournisseur Google Vertex Anthropic

Le fournisseur Google Vertex Anthropic pour le [SDK AI](/docs) offre une prise en charge des modèles Claude d'Anthropic à travers les API Google Vertex AI. Cette section fournit des détails sur la mise en place et l'utilisation du fournisseur Google Vertex Anthropic.

### Instance du Fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `vertexAnthropic` à partir de `@ai-sdk/google-vertex/anthropic` :

```typescript
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
```

Si vous avez besoin d'une mise en place personnalisée, vous pouvez importer `createVertexAnthropic` à partir de `@ai-sdk/google-vertex/anthropic` et créer une instance de fournisseur avec vos paramètres :

```typescript
import { createVertexAnthropic } from '@ai-sdk/google-vertex/anthropic';

const vertexAnthropic = createVertexAnthropic({
  projet : 'mon-projet', // facultatif
  emplacement : 'us-central1', // facultatif
});
```

#### Exécution Node.js

Pour les environnements Node.js, le fournisseur Google Vertex Anthropic prend en charge toutes les options d'authentification standard de Google Cloud à travers la bibliothèque `google-auth-library`. Vous pouvez personnaliser les options d'authentification en les passant à la fonction `createVertexAnthropic` :

```typescript
import { createVertexAnthropic } from '@ai-sdk/google-vertex/anthropic';

const vertexAnthropic = createVertexAnthropic({
  googleAuthOptions: {
    credentials: {
      client_email: 'mon-email',
      private_key: 'ma-clé-privee',
    },
  },
});
```

##### Paramètres du fournisseur facultatifs

Vous pouvez utiliser les paramètres suivants facultatifs pour personnaliser l'instance du fournisseur Google Vertex Anthropic :

- **projet** _chaîne_

  L'ID du projet Google Cloud que vous souhaitez utiliser pour les appels API.
  Il utilise par défaut la variable d'environnement `GOOGLE_VERTEX_PROJECT`.

- **emplacement** _chaîne_

  L'emplacement Google Cloud que vous souhaitez utiliser pour les appels API, par exemple `us-central1`.
  Il utilise par défaut la variable d'environnement `GOOGLE_VERTEX_LOCATION`.

- **googleAuthOptions** _objet_

  Facultatif. Les options d'authentification utilisées par la [Bibliothèque d'authentification Google](https://github.com/googleapis/google-auth-library-nodejs/). Voir également les [GoogleAuthOptions](https://github.com/googleapis/google-auth-library-nodejs/blob/08978822e1b7b5961f0e355df51d738e012be392/src/auth/googleauth.ts)

# L87C18-L87C35) interface.

  - **authClient** _objet_
    Un `AuthClient` à utiliser.

  - **keyFilename** _chaîne_
    Chemin vers un fichier de clé .json, .pem ou .p12.

  - **keyFile** _chaîne_
    Chemin vers un fichier de clé .json, .pem ou .p12.

  - **credentials** _objet_
    Objet contenant les propriétés client_email et private_key, ou les options de compte externe client.

  - **clientOptions** _objet_
    Options objet passé au constructeur du client.

  - **scopes** _chaîne | chaîne[]_
    Étendues requises pour la demande API souhaitée.

  - **projectId** _chaîne_
    Votre ID de projet.

  - **universeDomain** _chaîne_
    Le domaine de service par défaut pour un univers Cloud donné.

- **en-têtes** _Resolvable&lt;Record&lt;chaîne, chaîne | indéfini&gt;&gt;_

  Les en-têtes à inclure dans les requêtes. Ils peuvent être fournis sous plusieurs formats :

  - Un enregistrement de paires clé-valeur d'en-tête : `Record<string, string | undefined>`
  - Une fonction qui retourne des en-têtes : `() => Record<string, string | undefined>`
  - Une fonction asynchrone qui retourne des en-têtes : `async () => Record<string, string | undefined>`
  - Une promesse qui se résout en en-têtes : `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Par défaut, elle utilise la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests, par exemple.

<a id="google-vertex-anthropic-edge-runtime"></a>

#### Edge Runtime

Les environnements Edge (comme Vercel Edge Functions et Cloudflare Workers) sont des environnements JavaScript légers qui s'exécutent plus près des utilisateurs à l'extrémité du réseau.
Ils ne fournissent qu'un sous-ensemble des API Node.js standard.
Par exemple, l'accès direct au système de fichiers n'est pas disponible, et de nombreuses bibliothèques Node.js spécifiques (y compris la bibliothèque d'authentification Google standard) ne sont pas compatibles.

La version Edge du fournisseur Google Vertex Anthropic prend en charge les [Credentials par défaut d'Application Google](https://github.com/googleapis/google-auth-library-nodejs?tab=readme-ov-file#application-default-credentials) à travers les variables d'environnement. Les valeurs peuvent être obtenues à partir d'un fichier JSON de credentials depuis le [Console Google Cloud](https://console.cloud.google.com/apis/credentials).

Pour les environnements Edge, vous pouvez importer l'instance du fournisseur à partir de `@ai-sdk/google-vertex/anthropic/edge` :

```typescript
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic/edge';
```

Pour personnaliser la configuration, utilisez `createVertexAnthropic` du même module :

```typescript
import { createVertexAnthropic } from '@ai-sdk/google-vertex/anthropic/edge';

const vertexAnthropic = createVertexAnthropic({
  projet : 'mon-projet', // optionnel
  emplacement : 'us-central1', // optionnel
});
```

Pour l'authentification Edge runtime, définissez ces variables d'environnement à partir de votre fichier JSON de Credentials d'Application Google par défaut :

- `GOOGLE_CLIENT_EMAIL`
- `GOOGLE_PRIVATE_KEY`
- `GOOGLE_PRIVATE_KEY_ID` (facultatif)

#### Paramètres de configuration facultatifs du fournisseur

Vous pouvez utiliser les paramètres de configuration suivants pour personnaliser l'instance du fournisseur :

- **projet** _chaîne_

  L'ID du projet Google Cloud que vous souhaitez utiliser pour les appels API.
  Il utilise par défaut la variable d'environnement `GOOGLE_VERTEX_PROJECT`.

- **emplacement** _chaîne_

  L'emplacement Google Cloud que vous souhaitez utiliser pour les appels API, par exemple `us-central1`.
  Il utilise par défaut la variable d'environnement `GOOGLE_VERTEX_LOCATION`.

- **googleCredentials** _objet_

  Facultatif. Les informations d'identification utilisées par le fournisseur Edge pour l'authentification. Ces informations d'identification sont généralement définies à travers des variables d'environnement et sont dérivées d'un fichier JSON de compte de service.

  - **clientEmail** _chaîne_
    L'adresse e-mail du client du fichier JSON de compte de service. Par défaut, il utilise la valeur de la variable d'environnement `GOOGLE_CLIENT_EMAIL`.

  - **privateKey** _chaîne_
    La clé privée du fichier JSON de compte de service. Par défaut, il utilise la valeur de la variable d'environnement `GOOGLE_PRIVATE_KEY`.

  - **privateKeyId** _chaîne_
    L'ID de la clé privée du fichier JSON de compte de service (facultatif). Par défaut, il utilise la valeur de la variable d'environnement `GOOGLE_PRIVATE_KEY_ID`.

- **en-têtes** _Resolvable&lt;Record&lt;chaîne, chaîne | indéfini&gt;&gt;_

  Les en-têtes à inclure dans les requêtes. Ils peuvent être fournis sous différentes formes :

  - Un enregistrement de paires clé-valeur d'en-tête : `Record<string, string | undefined>`
  - Une fonction qui retourne les en-têtes : `() => Record<string, string | undefined>`
  - Une fonction asynchrone qui retourne les en-têtes : `async () => Record<string, string | undefined>`
  - Une promesse qui se résout en en-têtes : `Promise<Record<string, string | undefined>>`

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

Implémentation personnalisée de [fetch](https://developer.mozilla.org/fr/docs/Web/API/fetch).
  Par défaut, elle utilise la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour des tests par exemple.

### Modèles de Langue

Vous pouvez créer des modèles qui appellent l'[API de Messages d'Anthropic](https://docs.anthropic.com/claude/reference/messages_post) à l'aide de l'instance du fournisseur.
La première argument est l'ID du modèle, par exemple `claude-3-haiku-20240307`.
Certains modèles disposent de capacités multi-modales.

```ts
const model = anthropic('claude-3-haiku-20240307');
```

Vous pouvez utiliser les modèles de langues d'Anthropic pour générer du texte avec la fonction `generateText` :

```ts
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
import { generateText } from 'ai';

const { text } = await generateText({
  model: vertexAnthropic('claude-3-haiku-20240307'),
  prompt: 'Écrivez une recette de lasagnes végétariennes pour 4 personnes.',
});
```

Les modèles de langues d'Anthropic peuvent également être utilisés dans les fonctions `streamText`, `generateObject`, et `streamObject` (voir [Core de l'API SDK](/docs/ai-sdk-core)).

<Note>
  L'API d'Anthropic retourne des appels de l'outil de streaming tous à la fois après un délai. Cela
  cause la fonction `streamObject` à générer l'objet entièrement après un délai
  au lieu de le streaming de manière incrémentale.
</Note>

Les paramètres facultatifs suivants sont disponibles pour les modèles d'Anthropic :

- `sendReasoning` _boolean_

  Facultatif. Inclure le contenu de raisonnement dans les requêtes envoyées au modèle. Par défaut à `true`.

  Si vous rencontrez des problèmes avec le modèle qui gère les requêtes impliquant du contenu de raisonnement, vous pouvez définir cela sur `false` pour les omettre de la requête.

### Raisonnement

Anthropic offre un support de raisonnement pour le modèle `claude-3-7-sonnet@20250219`.

Vous pouvez l'activer en utilisant l'option `thinking` du fournisseur et en spécifiant un budget de tokens pour le raisonnement.

```ts
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
import { generateText } from 'ai';

const { text, raisonnement, detailsRaisonnement } = await generateText({
  model: vertexAnthropic('claude-3-7-sonnet@20250219'),
  prompt: 'Combien de personnes vivront dans le monde en 2040 ?',
  providerOptions: {
    anthropic: {
      thinking: { type: 'enabled', budgetTokens: 12000 },
    },
  },
});

console.log(raisonnement); // texte de raisonnement
console.log(detailsRaisonnement); // détails du raisonnement y compris le raisonnement masqué
console.log(text); // réponse textuelle
```

Consultez [UI SDK AI : Chatbot](/docs/ai-sdk-ui/chatbot#raisonnement) pour plus de détails
sur la manière d'intégrer le raisonnement dans votre chatbot.

#### Contrôle de Cache

<Note>
  Le contrôle de cache anthropique est dans un état Pré-Généralement Disponible (GA) sur Google Vertex. Pour plus d'informations, voir [la documentation du contrôle de cache anthropique de Google Vertex](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude-prompt-caching).
</Note>

Dans les messages et les parties de message, vous pouvez utiliser la propriété `providerOptions` pour définir les points de rupture de contrôle de cache.
Vous devez définir la propriété `anthropic` dans l'objet `providerOptions` sur `{ cacheControl: { type: 'ephemeral' } }` pour définir un point de rupture de contrôle de cache.

Les jetons d'entrée de création de cache sont ensuite retournés dans l'objet `providerMetadata` pour `generateText` et `generateObject`, à nouveau sous la propriété `anthropic`.
Lorsque vous utilisez `streamText` ou `streamObject`, la réponse contient une promesse qui se résout en métadonnées. Alternativement, vous pouvez les recevoir dans le callback `onFinish`.

```ts highlight="8,18-20,29-30"
import { vertexAnthropic } from '@ai-sdk/google-vertex/anthropic';
import { generateText } from 'ai';

const errorMessage = '... longue erreur de message ...';
```

```javascript
const result = await generateText({
  model: vertexAnthropic('claude-3-5-sonnet-20240620'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Vous êtes un expert en JavaScript.' },
        {
          type: 'text',
          text: `Message d'erreur : ${errorMessage}`,
          providerOptions: {
            anthropic: { cacheControl: { type: 'ephemeral' } },
          },
        },
        { type: 'text', text: 'Expliquez le message d\'erreur.' },
      ],
    },
  ],
});

console.log(result.text);
console.log(result.providerMetadata?.anthropic);
// par exemple : { cacheCreationInputTokens: 2118, cacheReadInputTokens: 0 }
```

Vous pouvez également utiliser le contrôle de cache sur les messages du système en fournissant plusieurs messages du système en tête de votre tableau de messages :

```ts highlight="3,9-11"
const result = await generateText({
  model: vertexAnthropic('claude-3-5-sonnet-20240620'),
  messages: [
    {
      role: 'system',
      content: 'Partie du message système en cache',
      providerOptions: {
        anthropic: { cacheControl: { type: 'éphémère' } },
      },
    },
    {
      role: 'system',
      content: 'Partie du message système non en cache',
    },
    {
      role: 'user',
      content: 'Prompt de l'utilisateur',
    },
  ],
});
```

Pour en savoir plus sur la mise en cache des prompts avec Anthropic, voir la [documentation de mise en cache des prompts de Google Vertex AI pour Claude](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude-prompt-caching) et la [documentation de contrôle de cache d'Anthropic](https

### Utilisation du Ordinateur

Anthropic fournit trois outils intégrés pouvant être utilisés pour interagir avec des systèmes externes :

1. **Outil Bash** : Permet d'exécuter des commandes bash.
2. **Outil de l'Éditeur de Texte** : fournit des fonctionnalités pour afficher et modifier des fichiers texte.
3. **Outil Ordinateur** : permet le contrôle des actions de la souris et de la touche sur un ordinateur.

Ils sont disponibles via la propriété `tools` de l'instance du fournisseur.

Pour plus d'informations voir [la documentation d'Anthropic sur l'utilisation du Ordinateur](https://docs.anthropic.com/en/docs/build-with-claude/computer-use).

#### Outil Bash

L'Outil Bash permet d'exécuter des commandes bash. Voici comment le créer et l'utiliser :

```ts
const bashTool = vertexAnthropic.tools.bash_20241022({
  execute: async ({ command, restart }) => {
    // Implémentez votre logique d'exécution de la commande bash ici
    // Retournez le résultat de l'exécution de la commande
  },
});
```

Paramètres :

- `command` (chaîne de caractères) : La commande bash à exécuter. Obligatoire à moins que l'outil ne soit redémarré.
- `restart` (booléen, facultatif) : Spécifier `true` redémarrera cet outil.

#### Outil d'Éditeur de Texte

L'outil d'éditeur de texte fournit une fonctionnalité pour afficher et éditer des fichiers de texte :

```ts
const outilEditeurTexte = vertexAnthropic.tools.textEditor_20241022({
  execute: async ({
    command,
    path,
    file_text,
    insert_line,
    new_str,
    old_str,
    view_range,
  }) => {
    // Implémentez votre logique d'édition de texte ici
    // Retournez le résultat de l'opération d'édition de texte
  },
});
```

Paramètres :

- `command` ('view' | 'create' | 'str_replace' | 'insert' | 'undo_edit'): La commande à exécuter.
- `path` (chaîne de caractères): Chemin absolu vers le fichier ou le répertoire, par exemple `/repo/file.py` ou `/repo`.
- `file_text` (chaîne de caractères, facultatif): Obligatoire pour la commande `create`, avec le contenu du fichier à créer.
- `insert_line` (nombre, facultatif): Obligatoire pour la commande `insert`. Le numéro de ligne après lequel insérer la nouvelle chaîne.
- `new_str` (chaîne de caractères, facultatif): Nouvelle chaîne pour les commandes `str_replace` ou `insert`.
- `old_str` (chaîne de caractères, facultatif): Obligatoire pour la commande `str_replace`, contenant la chaîne à remplacer.
- `view_range` (tableau de nombres, facultatif): Facultatif pour la commande `view` pour spécifier la plage de lignes à afficher.

#### Outil Informatique

L'Outil Informatique permet le contrôle des actions de clavier et de souris sur un ordinateur :

```ts
const computerTool = vertexAnthropic.tools.computer_20241022({
  largeurEcranPx: 1920,
  hauteurEcranPx: 1080,
  numeroEcran: 0, // Optionnel, pour les environnements X11

  execute: async ({ action, coordinate, text }) => {
    // Implémentez votre logique de contrôle de l'ordinateur ici
    // Retournez le résultat de l'action

    // Exemple de code :
    switch (action) {
      case 'screenshot': {
        // résultat multipart :
        return {
          type: 'image',
          data: fs
            .readFileSync('./data/screenshot-editor.png')
            .toString('base64'),
        };
      }
      default: {
        console.log('Action:', action);
        console.log('Coordonnées:', coordinate);
        console.log('Texte:', text);
        return `exécuté ${action}`;
      }
    }
  },

  // Cartographie vers le contenu de la résultat de l'outil pour la consommation par LLM :
  experimental_toToolResultContent(result) {
    return typeof result === 'string'
      ? [{ type: 'text', text: result }]
      : [{ type: 'image', data: result.data, mimeType: 'image/png' }];
  },
});
```

Paramètres :

- `action` ('clé' | 'type' | 'déplacement_souris' | 'clique_gauche' | 'clique_gauche_glissé' | 'clique_droit' | 'clique_milieu' | 'double_clique' | 'capture_ecran' | 'position_souris'): L'action à effectuer.
- `coordinate` (tableau de nombres, facultatif): Obligatoire pour les actions `déplacement_souris` et `clique_gauche_glissé`. Spécifie les coordonnées (x, y).
- `text` (chaîne de caractères, facultatif): Obligatoire pour les actions `type` et `clé`.

Ces outils peuvent être utilisés conjointement avec le modèle `claude-3-5-sonnet-v2@20241022` pour permettre des interactions et des tâches plus complexes.

### Capacités du Modèle

La liste la plus récente des modèles Anthropic sur Vertex AI est disponible [ici](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude#model-list).
Voir également [Compar

# Comparaison de Modèles).

| Modèle                            | Entrée Image          | Génération d'Objets    | Utilisation de l'Outil | Flux d'Utilisation de l'Outil | Utilisation de l'Ordinateur    |
| ----------------------------------- | -------------------- | --------------------- | --------------------- | ----------------------------- | ------------------------------ |
| `claude-3-7-sonnet@20250219`          | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} />          | <Vérifier size={18} />          |
| `claude-3-5-sonnet-v2@20241022`        | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} />          | <Vérifier size={18} />          |
| `claude-3-5-sonnet@20240620`           | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} />          | <Croix size={18} />             |
| `claude-3-5-haiku@20241022`            | <Croix size={18} />    | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} />          | <Croix size={18} />             |
| `claude-3-sonnet@20240229`             | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} />          | <Croix size={18} />             |
| `claude-3-haiku@20240307`              | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} /> | <Vérifier size={18} />          | <Croix size={18} />             |

| `claude-3-opus@20240229`        | <Vérifieur size={18} /> | <Vérifieur size={18} /> | <Vérifieur size={18} /> | <Vérifieur size={18} /> | <Croix size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID de modèle d'un fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

---
title: Rev.ai
description: Apprenez à utiliser le fournisseur Rev.ai pour le SDK AI.
---

# Fournisseur Rev.ai

Le [fournisseur Rev.ai](https://www.rev.ai/) contient un support de modèle de langue pour l'API de transcription Rev.ai.

## Configuration

Le fournisseur Rev.ai est disponible dans le module `@ai-sdk/revai`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `revai` à partir de `@ai-sdk/revai` :

```ts
import { revai } from '@ai-sdk/revai';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createRevai` à partir de `@ai-sdk/revai` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createRevai } from '@ai-sdk/revai';

const revai = createRevai({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Rev.ai :

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Elle prend par défaut la variable d'environnement `REVAI_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Elle prend par défaut la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour les tests, par exemple.

## Modèles de Transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription Rev.ai](https://www.rev.ai/docs/api/transcription)
en utilisant la méthode de fabrication `.transcription()`.

La première argument est l'identifiant du modèle par exemple `machine`.

```ts
const model = revai.transcription('machine');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, la fourniture de la langue d'entrée sous la forme ISO-639-1 (par exemple `en`) peut améliorer les performances de transcription si elle est connue à l'avance.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { revai } from '@ai-sdk/revai';
import { readFile } from 'fs/promises';

const result = await transcribe({
  model: revai.transcription('machine'),
  audio: await readFile('audio.mp3'),
  providerOptions: { revai: { language: 'en' } },
});
```

Les options de fournisseur suivantes sont disponibles :

- **metadata** _chaîne_

  Les métadonnées optionnelles qui ont été fournies lors de la soumission de la tâche.

- **notification_config** _objet_

  La configuration optionnelle pour une URL de rappel à invoquer lors de la fin du traitement.

  - **url** _chaîne_ - L'URL de rappel à invoquer lors de la fin du traitement.
  - **auth_headers** _objet_ - Les en-têtes d'autorisation optionnels, si nécessaire pour invoquer le rappel.

- **delete_after_seconds** _entier_

  La durée après la fin de la tâche pendant laquelle la tâche est supprimée automatiquement.

- **verbatim** _booléen_

  Configure le transcriber pour transcrire chaque syllabe, y compris toutes les débuts faux et les disfluences.

- **rush** _booléen_

  [Non pris en charge HIPAA] Disponible uniquement pour l'option de transcriber humain. Lorsque défini sur vrai, votre tâche est donnée une priorité élevée.

- **skip_diarization** _booléen_

  Spécifie si la diarisation des locuteurs sera ignorée par l'engin de parole.

- **skip_postprocessing** _booléen_

  Disponible uniquement pour les langues anglaise et espagnole. Préférence fournie par l'utilisateur sur la possibilité de sauter les opérations de post-traitement.

- **skip_punctuation** _boolean_

  Spécifiez si les éléments de type "punct" seront ignorés par le moteur de parole.

- **remove_disfluencies** _boolean_

  Lorsque défini sur true, les disfluences (comme 'ums' et 'uhs') ne seront pas présentes dans le transcript.

- **remove_atmospherics** _boolean_

  Lorsque défini sur true, les atmosphériques (comme `<laugh>`, `<affirmative>`) ne seront pas présentes dans le transcript.

- **filter_profanity** _boolean_

  Lorsque activé, les profanités seront filtrées en remplaçant les caractères par des astérisques sauf les premiers et les derniers.

- **speaker_channels_count** _integer_

  Seulement disponible pour les langues anglaise, espagnole et française. Spécifiez le nombre total de canaux de locuteurs uniques dans l'audio.

- **speakers_count** _integer_

  Seulement disponible pour les langues anglaise, espagnole et française. Spécifiez le nombre total de locuteurs uniques dans l'audio.

- **diarization_type** _string_

  Spécifiez le type de diarisation. Possibles valeurs : "standard" (par défaut), "premium".

- **custom_vocabulary_id** _string_

  Fournissez l'ID d'un vocabulaire personnalisé pré-rempli soumis à travers l'API des Vocabulaires Personnalisés.

- **custom_vocabularies** _Array_

  Spécifiez une collection de vocabulaires personnalisés à utiliser pour ce travail.

- **strict_custom_vocabulary** _boolean_

  Si true, seuls les phrases exactes seront utilisées comme vocabulaire personnalisé.

- **summarization_config** _object_

  Spécifiez les options de résumé.

  - **model** _string_ - Type de modèle pour la résumé. Possibles valeurs : "standard" (par défaut), "premium".
  - **type** _string_ - Type de mise en forme de la résumé. Possibles valeurs : "paragraph" (par défaut), "bullets".
  - **prompt** _string_ - Invitation personnalisée pour des résumés flexibles (mutuellement exclusif avec type).

- **translation_config** _object_

  Spécifiez les options de traduction.

- **target_languages** _Tableau_ - Tableau des langues cibles pour la traduction.
  - **model** _chaîne_ - Type de modèle pour la traduction. Les valeurs possibles sont : "standard" (par défaut), "premium".

- **language** _chaîne_

  La langue est fournie sous la forme d'un code de langue ISO 639-1. La valeur par défaut est "en".

- **forced_alignment** _booléen_

  Lorsqu'il est activé, il fournit une précision améliorée pour les timestamps par mot pour un transcript.
  La valeur par défaut est `false`.

  Langues prises en charge actuellement :

  - Anglais (en, en-us, en-gb)
  - Français (fr)
  - Italien (it)
  - Allemand (de)
  - Espagnol (es)

  Remarque : Cette option n'est pas disponible dans l'environnement de faible coût.

### Capacités du Modèle

| Modèle      | Transcription       | Durée            | Segments            | Langue            |
| ---------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `machine`  | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `human`    | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `low_cost` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `fusion`   | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
Titre : Mistral AI
Description : Apprenez à utiliser Mistral.
---

# Fournisseur Mistral AI

Le [fournisseur Mistral AI](https://mistral.ai/) contient un support pour les modèles de langage pour l'API de conversation de Mistral.

## Configuration

Le fournisseur Mistral est disponible dans le module `@ai-sdk/mistral`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `mistral` à partir de `@ai-sdk/mistral` :

```ts
import { mistral } from '@ai-sdk/mistral';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createMistral` à partir de `@ai-sdk/mistral`
et créer une instance de fournisseur avec vos paramètres :

```ts
import { createMistral } from '@ai-sdk/mistral';

const mistral = createMistral({
  // paramètres personnalisés
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Mistral :

- **baseURL** _chaîne_

  Utilisez une URL de préfixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  Le préfixe par défaut est `https://api.mistral.ai/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée à l'aide de l'en-tête `Authorization`.
  Il prend par défaut la variable d'environnement `MISTRAL_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Par défaut, il utilise la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour les tests, par exemple.

## Modèles de langage

Vous pouvez créer des modèles qui appellent l'[API de discussion de Mistral](https://docs.mistral.ai/api/

# (opération/createChatCompletion) en utilisant une instance de fournisseur.
La première argument est l'identifiant du modèle, par exemple `mistral-large-latest`.
Certains modèles de discussion Mistral supportent les appels d'outil.

```ts
const model = mistral('mistral-large-latest');
```

Les modèles de discussion Mistral supportent également des paramètres de modèle supplémentaires qui ne font pas partie des [paramètres de l'appel standard](/docs/ai-sdk-core/settings).
Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = mistral('mistral-large-latest', {
  safePrompt: true, // injection de prompt de sécurité facultative
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles Mistral :

- **safePrompt** _boolean_

  Injecter un prompt de sécurité avant toutes les conversations.

  Par défaut, `false`.

### Document OCR

Les modèles de chat Mistral supportent l'OCR de documents pour les fichiers PDF.
Vous pouvez configurer de manière optionnelle les limites d'image et de page en utilisant les options du fournisseur.

```ts
const result = await generateText({
  model: mistral('mistral-small-latest'),
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: 'Qu\'est-ce qu\'un modèle d\'embedding selon ce document?',
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
  // paramètres optionnels :
  providerOptions: {
    mistral: {
      documentImageLimit: 8,
      documentPageLimit: 64,
    },
  },
});
```

### Exemple

Vous pouvez utiliser les modèles de langage Mistral pour générer du texte avec la fonction `generateText` :

```ts
import { mistral } from '@ai-sdk/mistral';
import { generateText } from 'ai';

const { text } = await generateText({
  model: mistral('mistral-large-latest'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage Mistral peuvent également être utilisés dans les fonctions `streamText`, `generateObject` et `streamObject` (voir [AI SDK Core](/docs/ai-sdk-core)).

### Capabilités du Modèle

| Modèle                  | Entrée d'image         | Génération d'objet   | Utilisation de l'outil          | Flux d'outil            |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `pixtral-large-latest` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistral-large-latest` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistral-small-latest` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `ministral-3b-latest`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `ministral-8b-latest`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `pixtral-12b-2409`     | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter la [documentation de Mistral](https://docs.mistral.ai/getting-started/models/models_overview/) pour une liste complète des modèles disponibles. La table ci-dessus liste les modèles populaires. Vous pouvez également passer l'ID du modèle d'un fournisseur disponible en tant que chaîne si nécessaire.
</Note>

## Modèles d'Embedding

Vous pouvez créer des modèles qui appellent l'[API d'embeddings de Mistral](https://docs.mistral.ai/api/#operation/createEmbedding) en utilisant la méthode de fabrication `.embedding()`.

```ts
const model = mistral.embedding('mistral-embed');
```

### Capacités du Modèle

| Modèle           | Dimensions par Défaut |
| --------------- | ------------------ |
| `mistral-embed` | 1024               |

---
titre: Together.ai
description: Découvrez comment utiliser les modèles de Together.ai avec le SDK AI.
---

# Fournisseur Together.ai

Le [fournisseur Together.ai](https://together.ai) contient un support pour 200+ modèles open-source grâce à l'[API Together.ai](https://docs.together.ai/reference).

## Configuration

Le fournisseur Together.ai est disponible via le module `@ai-sdk/togetherai`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `togetherai` à partir de `@ai-sdk/togetherai` :

```ts
import { togetherai } from '@ai-sdk/togetherai';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createTogetherAI` à partir de `@ai-sdk/togetherai`
et créer une instance de fournisseur avec vos paramètres :

```ts
import { createTogetherAI } from '@ai-sdk/togetherai';

const togetherai = createTogetherAI({
  apiKey: process.env.TOGETHER_AI_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Together.ai :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  Le prefixe par défaut est `https://api.together.xyz/v1`.

- **apiKey** _chaîne_

  Clé d'API qui est envoyée en utilisant l'en-tête `Authorization`. Il prend par défaut la valeur de la variable d'environnement `TOGETHER_AI_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). Les paramètres par défaut sont la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests par exemple.

## Modèles de langage

Vous pouvez créer des [modèles Together.ai](https://docs.together.ai/docs/serverless-models) à l'aide d'une instance de fournisseur. Le premier argument est l'ID du modèle, par exemple `google/gemma-2-9b-it`.

```ts
const model = togetherai('google/gemma-2-9b-it');
```

### Modèles de Raisonnement

Together.ai expose les pensées de `deepseek-ai/DeepSeek-R1` dans le texte généré à l'aide de la balise `<think>`.
Vous pouvez utiliser `extractReasoningMiddleware` pour extraire ce raisonnement et l'exposer sous la propriété `reasoning` du résultat :

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const enhancedModel = wrapLanguageModel({
  model: togetherai('deepseek-ai/DeepSeek-R1'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Vous pouvez ensuite utiliser ce modèle amélioré dans des fonctions comme `generateText` et `streamText`.

### Exemple

Vous pouvez utiliser les modèles de langage de Together.ai pour générer du texte avec la fonction `generateText` :

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { generateText } from 'ai';

const { text } = await generateText({
  model: togetherai('meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage de Together.ai peuvent également être utilisés dans la fonction `streamText` (voir [Core SDK AI](/docs/ai-sdk-core)).

Le fournisseur Together.ai prend également en charge les [modèles de complétion](https://docs.together.ai/docs/serverless-models#language-models) via (suivant le code d'exemple ci-dessus) `togetherai.completionModel()` et les [modèles d'embeddings](https://docs.together.ai/docs/serverless-models#embedding-models) via `togetherai.textEmbeddingModel()`.

## Capacités du Modèle

| Modèle                                          | Entrée d'Image         | Génération d'Objet   | Utilisation d'Outil        | Flux d'Outil Streaming      |
| ---------------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `meta-llama/Meta-Llama-3.3-70B-Instruct-Turbo` | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`  | <Cross size={18} /> | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistralai/Mixtral-8x22B-Instruct-v0.1`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `mistralai/Mistral-7B-Instruct-v0.3`           | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `deepseek-ai/DeepSeek-V3`                      | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `google/gemma-2b-it`                           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

| `Qwen/Qwen2.5-72B-Instruct-Turbo`              | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |
| `databricks/dbrx-instruct`                     | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> | <Croix size={18} /> |

<Note>
  La table ci-dessus liste des modèles populaires. Veuillez consulter la [documentation de Together.ai](https://docs.together.ai/docs/serverless-models) pour obtenir une liste complète des modèles disponibles. Vous pouvez également passer l'ID d'un modèle fourni par un fournisseur sous forme de chaîne si nécessaire.
</Note>

## Modèles d'images

Vous pouvez créer des modèles d'images Together.ai à l'aide de la méthode de fabrication `.image()`.
Pour plus d'informations sur la génération d'images avec l'API SDK, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { experimental_generateImage as generateImage } from 'ai';

const { images } = await generateImage({
  model: togetherai.image('black-forest-labs/FLUX.1-dev'),
  prompt: 'Un resplendissant quetzal délicieux en vol au milieu de gouttes de pluie',
});
```

Vous pouvez passer des paramètres de requête spécifiques au fournisseur facultatifs à l'aide de l'argument `providerOptions`.

```ts
import { togetherai } from '@ai-sdk/togetherai';
import { experimental_generateImage as generateImage } from 'ai';

const { images } = await generateImage({
  model: togetherai.image('black-forest-labs/FLUX.1-dev'),
  prompt: 'Un resplendissant quetzal délicieux en vol au milieu de gouttes de pluie',
  size: '512x512',
  // Paramètres de requête facultatifs spécifiques au fournisseur
  providerOptions: {
    togetherai: {
      steps: 40,
    },
  },
});
```

Pour une liste complète des options spécifiques au fournisseur disponibles, voir la [Référence de l'API de génération d'images Together.ai](https://docs.together.ai/reference/post_images-generations).

### Capacités du Modèle

Les modèles d'image Together.ai supportent diverses dimensions d'image qui varient en fonction du modèle. Les tailles courantes incluent 512x512, 768x768 et 1024x1024, certains modèles supportant jusqu'à 1792x1792. La taille par défaut est de 1024x1024.

| Modèles Disponibles                           |
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

<Remarque>
  Veuillez consulter la page [modèles Together.ai](https://docs.together.ai/docs/serverless-models#image-models) pour une liste complète des modèles d'image disponibles et de leurs capacités.
</Remarque>

---
Titre : Cohere
Description : Apprenez à utiliser le fournisseur Cohere pour le SDK AI.
---

# Fournisseur Cohere

Le [fournisseur Cohere](https://cohere.com

## Installation

Le fournisseur Cohere est disponible dans le module `@ai-sdk/cohere`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `cohere` à partir de `@ai-sdk/cohere` :

```ts
import { cohere } from '@ai-sdk/cohere';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createCohere` à partir de `@ai-sdk/cohere`
et créer une instance de fournisseur avec vos paramètres :

```ts
import { createCohere } from '@ai-sdk/cohere';

const cohere = createCohere({
  // paramètres personnalisés
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Cohere :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  La valeur par défaut est `https://api.cohere.com/v2`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  La valeur par défaut est la variable d'environnement `COHERE_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  La valeur par défaut est la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour les tests, par exemple.

## Modèles de langage

Vous pouvez créer des modèles qui appellent l'[API de chat Cohere](https://docs.cohere.com/v2/docs/chat-api) à l'aide d'une instance de fournisseur.
La première argument est l'ID du modèle, par exemple `command-r-plus`.
Certains modèles de chat Cohere supportent les appels de la commande.

```ts
const model = cohere('command-r-plus');
```

### Exemple

Vous pouvez utiliser les modèles de langage Cohere pour générer du texte avec la fonction `generateText` :

```ts
import { cohere } from '@ai-sdk/cohere';
import { generateText } from 'ai';

const { text } = await generateText({
  model: cohere('command-r-plus'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
});
```

Les modèles de langage Cohere peuvent également être utilisés dans les fonctions `streamText`, `generateObject`, et `streamObject` (voir [Core SDK AI](/docs/ai-sdk-core).)

### Capacités du Modèle

| Modèle                | Entrée d'image          | Génération d'objet      | Utilisation d'outil      | Flux d'outil           |
| -------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- |
| `command-a-03-2025`   | <Cross size={18} />    | <Check size={18} />    | <Check size={18} />    | <Check size={18} />    |
| `command-r-plus`      | <Cross size={18} />    | <Check size={18} />    | <Check size={18} />    | <Check size={18} />    |
| `command-r`           | <Cross size={18} />    | <Check size={18} />    | <Check size={18} />    | <Check size={18} />    |
| `command-a-03-2025`   | <Cross size={18} />    | <Check size={18} />    | <Check size={18} />    | <Check size={18} />    |
| `command`             | <Cross size={18} />    | <Cross size={18} />    | <Cross size={18} />    | <Cross size={18} />    |
| `command-light`       | <Cross size={18} />    | <Cross size={18} />    | <Cross size={18} />    | <Cross size={18} />    |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter les [docs Cohere](https://docs.cohere.com/v2/docs/models#command) pour une liste complète des modèles disponibles. Vous pouvez également passer l'ID d'un modèle de fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

## Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'[API de mise en forme de Cohere](https://docs.cohere.com/v2/reference/embed) en utilisant la méthode de fabrication `.embedding()`.

```ts
const model = cohere.embedding('embed-english-v3.0');
```

Les modèles de mise en forme de Cohere prennent en charge des paramètres supplémentaires. Vous pouvez les passer en tant qu'argument d'options :

```ts
const model = cohere.embedding('embed-english-v3.0', {
  inputType: 'search_document',
});
```

Les paramètres facultatifs suivants sont disponibles pour les modèles de mise en forme de Cohere :

- **inputType** _'search_document' | 'search_query' | 'classification' | 'clustering'_

  Spécifie le type d'entrée passée au modèle. La valeur par défaut est `search_query`.

  - `search_document` : Utilisé pour les embeddings stockés dans une base de données vectorielle pour les cas d'utilisation de recherche.
  - `search_query` : Utilisé pour les embeddings des requêtes de recherche exécutées contre une base de données vectorielle pour trouver des documents pertinents.
  - `classification` : Utilisé pour les embeddings passés par un classificateur de texte.
  - `clustering` : Utilisé pour les embeddings exécutés par un algorithme de regroupement.

- **truncate** _'NONE' | 'START' | 'END'_

  Spécifie comment l'API gérera les entrées plus longues que la longueur maximale de token.
  La valeur par défaut est `END`.

  - `NONE` : Si sélectionné, lorsqu'une entrée dépasse la longueur maximale de token, l'API retournera une erreur.
  - `START` : Éliminera le début de l'entrée jusqu'à ce que le reste de l'entrée soit exactement la longueur maximale de token pour le modèle.
  - `END` : Éliminera la fin de l'entrée jusqu'à ce que le reste de l'entrée soit exactement la longueur maximale de token pour le modèle.

### Capacités du Modèle

| Modèle                           | Dimensions des Éléments d'Embedding |
| ------------------------------- | -------------------- |
| `embed-english-v3.0`            | 1024                 |
| `embed-multilingual-v3.0`       | 1024                 |
| `embed-english-light-v3.0`      | 384                  |
| `embed-multilingual-light-v3.0` | 384                  |
| `embed-english-v2.0`            | 4096                 |
| `embed-english-light-v2.0`      | 1024                 |
| `embed-multilingual-v2.0`       | 768                  |

---
titre : Feux d'Artifice
description : Apprenez à utiliser les modèles Fireworks avec la SDK AI.
---

# Fournisseur Fireworks

[Feux d'Artifice](https://fireworks.ai/) est une plateforme pour exécuter et tester les LLMs à travers leur [API](https://readme.fireworks.ai/).

## Configuration

Le fournisseur Fireworks est disponible via le module `@ai-sdk/fireworks`. Vous pouvez l'installer avec

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `fireworks` de `@ai-sdk/fireworks` :

```ts
import { fireworks } from '@ai-sdk/fireworks';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createFireworks` de `@ai-sdk/fireworks`
et créer une instance de fournisseur avec vos paramètres :

```ts
import { createFireworks } from '@ai-sdk/fireworks';

const fireworks = createFireworks({
  apiKey: process.env.FIREWORKS_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Fireworks :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  La valeur par défaut est `https://api.fireworks.ai/inference/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. La valeur par défaut est la variable d'environnement `FIREWORKS_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input : RequestInfo, init ?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modèles de Langue

Vous pouvez créer des modèles [Fireworks](https://fireworks.ai/models) à l'aide d'une instance de fournisseur.
La première argument est l'ID du modèle, par exemple `accounts/fireworks/models/firefunction-v1`:

```ts
const model = fireworks('accounts/fireworks/models/firefunction-v1');
```

### Modèles de Raisonnement

Fireworks expose la pensée de `deepseek-r1` dans le texte généré à l'aide de la balise `<think>`.
Vous pouvez utiliser `extractReasoningMiddleware` pour extraire ce raisonnement et l'exposer comme une propriété `reasoning` sur le résultat :

```ts
import { fireworks } from '@ai-sdk/fireworks';
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const enhancedModel = wrapLanguageModel({
  model: fireworks('accounts/fireworks/models/deepseek-r1'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

Vous pouvez ensuite utiliser ce modèle amélioré dans les fonctions comme `generateText` et `streamText`.

### Exemple

Vous pouvez utiliser les modèles de langage Fireworks pour générer du texte à l'aide de la fonction `generateText` :

```ts
import { fireworks } from '@ai-sdk/fireworks';
import { generateText } from 'ai';

const { text } = await generateText({
  model: fireworks('accounts/fireworks/models/firefunction-v1'),
  prompt: 'Écrivez une recette de lasagna végétarienne pour 4 personnes.',
});
```

Les modèles de langage Fireworks peuvent également être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

### Modèles de Complétion

Vous pouvez créer des modèles qui appellent l'API de complétion Fireworks à l'aide de la méthode de fabrication `.completion()` :

```ts
const model = fireworks.completion('accounts/fireworks/models/firefunction-v1');
```

### Capacités du Modèle

### Pr

| Modèle                                                     | Entrée d'image          | Génération d'objets    | Utilisation de l'outil        | Flux d'outil             |
| ---------------------------------------------------------- | ----------------------- | ---------------------- | ----------------------------- | ------------------------- |
| `accounts/fireworks/models/deepseek-r1`                    | <Cross size={18} /> | <Check size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/deepseek-v3`                    | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p1-405b-instruct`       | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `accounts/fireworks/models/llama-v3p1-8b-instruct`         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p2-3b-instruct`         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `accounts/fireworks/models/llama-v3p3-70b-instruct`        | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

| `comptes/fireworks/models/mixtral-8x7b-instruct-hf`       | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `comptes/fireworks/models/mixtral-8x22b-instruct`         | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `comptes/fireworks/models/qwen2p5-coder-32b-instruct`     | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `comptes/fireworks/models/llama-v3p2-11b-vision-instruct` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |
| `comptes/fireworks/models/yi-large`                       | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Cross size={18} /> |

<Note>
  La table ci-dessus liste les modèles populaires. Veuillez consulter la [page des modèles Fireworks](https://fireworks.ai/models) pour une liste complète des modèles disponibles.
</Note>

## Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'API d'embeddings de Fireworks à l'aide de la méthode de fabrication `.textEmbeddingModel()` :

```ts
const model = fireworks.textEmbeddingModel(
  'accounts/fireworks/models/nomic-embed-text-v1',
);
```

## Modèles d'Images

Vous pouvez créer des modèles d'images Fireworks à l'aide de la méthode de fabrication `.image()`.
Pour plus d'informations sur la génération d'images avec le SDK AI, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

```ts
import { fireworks } from '@ai-sdk/fireworks';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: fireworks.image('accounts/fireworks/models/flux-1-dev-fp8'),
  prompt: 'Une ville futuriste à l'heure du coucher du soleil',
  aspectRatio: '16:9',
});
```

<Note>
  Le support des paramètres `size` et `aspectRatio` varie entre les modèles. Voir la section [Capacités des Modèles](#model-capabilities-1) ci-dessous pour les dimensions prises en charge, ou consultez la documentation du modèle sur la [page des modèles de Fireworks](https://fireworks.ai/models) pour plus de détails.
</Note>

### Capabilités du Modèle

Pour tous les modèles supportant les rapports d'aspects, les rapports d'aspects suivants sont pris en charge :

`1:1 (par défaut), 2:3, 3:2, 4:5, 5:4, 16:9, 9:16, 9:21, 21:9`

Pour tous les modèles supportant les tailles, les tailles suivantes sont prises en charge :

`640 x 1536, 768 x 1344, 832 x 1216, 896 x 1152, 1024x1024 (par défaut), 1152 x 896, 1216 x 832, 1344 x 768, 1536 x 640`

| Modèle                                                        | Spécification de dimensions |
| ------------------------------------------------------------ | ------------------------ |
| `accounts/fireworks/models/flux-1-dev-fp8`                   | Rapport d'aspect             |
| `accounts/fireworks/models/flux-1-schnell-fp8`               | Rapport d'aspect             |
| `accounts/fireworks/models/playground-v2-5-1024px-aesthetic` | Taille                     |
| `accounts/fireworks/models/japanese-stable-diffusion-xl`     | Taille                     |
| `accounts/fireworks/models/playground-v2-1024px-aesthetic`   | Taille                     |
| `accounts/fireworks/models/SSD-1B`                           | Taille                     |
| `accounts/fireworks/models/stable-diffusion-xl-102

#### Modèles Stability AI

Fireworks présente également plusieurs modèles Stability AI appuyés par des clés API et des points de terminaison de Stability AI. Le fournisseur de SDK AI Fireworks ne prend pas actuellement en charge ces modèles :

| ID du modèle                               |
| -------------------------------------- |
| `accounts/stability/models/sd3-turbo`  |
| `accounts/stability/models/sd3-medium` |
| `accounts/stability/models/sd3`        |

---
titre : DeepSeek
description : Apprenez à utiliser les modèles de DeepSeek avec le SDK AI.
---

# Fournisseur DeepSeek

Le [fournisseur DeepSeek](https://www.deepseek.com) offre accès à des modèles de langage puissants à travers l'API DeepSeek, y compris leur [modèle DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3).

Les clés API peuvent être obtenues à partir de la [plateforme DeepSeek](https://platform.deepseek.com/api_keys).

## Configuration

Le fournisseur DeepSeek est disponible via le module `@ai-sdk/deepseek`. Vous pouvez l'installer avec :

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `deepseek` depuis `@ai-sdk/deepseek` :

```ts
import { deepseek } from '@ai-sdk/deepseek';
```

Pour une configuration personnalisée, vous pouvez importer `createDeepSeek` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createDeepSeek } from '@ai-sdk/deepseek';

const deepseek = createDeepSeek({
  apiKey: process.env.DEEPSEEK_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur DeepSeek :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API.
  Le prefixe par défaut est `https://api.deepseek.com/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. Il prend par défaut la valeur de l'environnement variable `DEEPSEEK_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modèles de langage

Vous pouvez créer des modèles de langage à l'aide d'une instance de fournisseur :

```ts
import { deepseek } from '@ai-sdk/deepseek';
import { generateText } from 'ai';

const { text } = await generateText({
  model: deepseek('deepseek-chat'),
  prompt: 'Écrivez une recette de lasagnes végétariennes pour 4 personnes.',
});
```

Les modèles de langage DeepSeek peuvent être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

### Raisonnement

DeepSeek dispose d'une prise en charge de raisonnement pour le modèle `deepseek-reasoner` :

```ts
import { deepseek } from '@ai-sdk/deepseek';
import { generateText } from 'ai';

const { text, raisonnement } = await generateText({
  model: deepseek('deepseek-reasoner'),
  prompt: 'Combien de personnes vivront dans le monde en 2040 ?',
});

console.log(raisonnement);
console.log(text);
```

Voir [AI SDK UI : Chatbot](/docs/ai-sdk-ui/chatbot#raisonnement) pour plus de détails sur la manière d'intégrer le raisonnement dans votre chatbot.

### Utilisation des jetons de cache

DeepSeek fournit une technologie de cache de contexte sur disque qui peut réduire considérablement les coûts de jetons pour le contenu répété. Vous pouvez accéder aux métriques de cache hit/miss à travers la propriété `providerMetadata` dans la réponse :

```ts
import { deepseek } from '@ai-sdk/deepseek';
import { generateText } from 'ai';

const result = await generateText({
  model: deepseek('deepseek-chat'),
  prompt: 'Votre prompt ici',
});

console.log(result.providerMetadata);
// Exemple de sortie : { deepseek : { promptCacheHitTokens : 1856, promptCacheMissTokens : 5 } }
```

Les métriques incluent :

- `promptCacheHitTokens` : Nombre de jetons d'entrée qui ont été mis en cache
- `promptCacheMissTokens` : Nombre de jetons d'entrée qui n'ont pas été mis en cache

<Note>
  Pour plus de détails sur le système de cache de DeepSeek, voir la [documentation sur le cache de DeepSeek](https://api-docs.deepseek.com/guides/kv_cache#checking-cache-hit-status).
</Note>

## Capacités du Modèle

| Modèle                    | Génération de Texte     | Génération d'Objet   | Entrée Image         | Utilisation d'Outils          | Flux d'Outils      |
| ------------------------- | ----------------------- | ------------------- | ------------------- | --------------------------- | ------------------- |
| `deepseek-chat`           | <Check size={18} />    | <Check size={18} /> | <Cross size={18} /> | <Check size={18} />          | <Check size={18} /> |
| `deepseek-reasoner`       | <Check size={18} />    | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} />          | <Cross size={18} /> |

<Note>
  Veuillez consulter la documentation [DeepSeek](https://api-docs.deepseek.com) pour une liste complète
  des modèles disponibles. Vous pouvez également passer l'ID du modèle de fournisseur disponible sous forme de chaîne si nécessaire.
</Note>

---
title: Cerebras
description: Apprenez à utiliser les modèles de Cerebras avec le SDK AI.
---

# Fournisseur Cerebras

Le [fournisseur Cerebras](https://cerebras.ai) offre accès à des modèles de langage puissants grâce à l'API Cerebras, y compris leurs capacités d'inference à haute vitesse alimentées par les moteurs à échelle de plaque et les systèmes CS-3.

Les clés d'API peuvent être obtenues à partir de la [Plateforme Cerebras](https://cloud.cerebras.ai).

## Configuration

Le fournisseur Cerebras est disponible via le module `@ai-sdk/cerebras`. Vous pouvez l'installer avec :

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

## Instance du fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `cerebras` à partir de `@ai-sdk/cerebras` :

```ts
import { cerebras } from '@ai-sdk/cerebras';
```

Pour une configuration personnalisée, vous pouvez importer `createCerebras` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createCerebras } from '@ai-sdk/cerebras';

const cerebras = createCerebras({
  apiKey: process.env.CEREBRAS_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Cerebras :

- **baseURL** _chaîne_

  Utilisez un préfixe de URL différent pour les appels API.
  Le préfixe par défaut est `https://api.cerebras.ai/v1`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. Il prend par défaut la valeur de l'environnement variable `CEREBRAS_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modèles de langage

Vous pouvez créer des modèles de langage à l'aide d'une instance de fournisseur :

```ts
import { cerebras } from '@ai-sdk/cerebras';
import { generateText } from 'ai';

const { text } = await generateText({
  model: cerebras('llama3.1-8b'),
  prompt: 'Écrivez une recette de lasagna végétarienne pour 4 personnes.',
});
```

Les modèles de langage Cerebras peuvent être utilisés dans la fonction `streamText` (voir [AI SDK Core](/docs/ai-sdk-core)).

## Capacités du Modèle

| Modèle          | Entrée d'Image         | Génération d'Objet   | Utilisation d'Outil          | Flux d'Outil Streaming      |
| -------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `llama3.1-8b`  | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama3.1-70b` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `llama3.3-70b` | <Cross size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

<Note>
  Veuillez consulter les [docs Cerebras](https://inference-docs.cerebras.ai/introduction) pour plus de détails sur les modèles disponibles. Notez que les fenêtres de contexte sont temporairement limitées à 8192 jetons dans la version Gratuite.
</Note>

---
title: Replication
description: Apprenez à utiliser les modèles Replicate avec le SDK AI.
---

# Fournisseur Replicate

[Replicate](https://replicate.com/) est une plateforme pour exécuter des modèles d'IA open-source. Il s'agit d'une choix populaire pour exécuter des modèles de génération d'image.

## Configuration

Le fournisseur Replicate est disponible via le module `@ai-sdk/replicate`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `replicate` à partir de `@ai-sdk/replicate` :

```ts
import { replicate } from '@ai-sdk/replicate';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createReplicate` à partir de `@ai-sdk/replicate`
et créer une instance de fournisseur avec vos paramètres :

```ts
import { createReplicate } from '@ai-sdk/replicate';

const replicate = createReplicate({
  apiToken: process.env.REPLICATE_API_TOKEN ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Replicate :

- **baseURL** _chaîne_

  Utilisez une adresse URL différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  La valeur par défaut est `https://api.replicate.com/v1`.

- **apiToken** _chaîne_

  Jeton d'API qui est envoyé en utilisant l'en-tête `Authorization`. Il prend par défaut la valeur de la variable d'environnement `REPLICATE_API_TOKEN`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modèles d'image

Vous pouvez créer des modèles d'image Replicate à l'aide de la méthode de fabrication `.image()`.
Pour plus d'informations sur la génération d'image avec le kit SDK, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

<Remarque>
  Le support des modèles pour `size` et autres paramètres varie en fonction du modèle. Vérifiez la documentation du modèle sur [Replicate](https://replicate.com/explore) pour les options et les paramètres supplémentaires qui peuvent être passés via `providerOptions.replicate`.
</Remarque>

### Modèles d'Images Supportés

Les modèles d'images suivants sont actuellement pris en charge par le fournisseur Replicate :

- [black-forest-labs/flux-1.1-pro-ultra](https://replicate.com/black-forest-labs/flux-1.1-pro-ultra)
- [black-forest-labs/flux-1.1-pro](https://replicate.com/black-forest-labs/flux-1.1-pro)
- [black-forest-labs/

- [stability-ai

Vous pouvez également utiliser des [modèles versionnés](https://replicate.com/docs/topics/models/versions).
L'identifiant pour les modèles versionnés est l'identifiant du modèle Replicate suivi d'un point-virgule et de l'ID de version (`$modelId:$versionId`), par exemple :
`bytedance/sdxl-lightning-

### Utilisation de base

```ts
import { replicate } from '@ai-sdk/replicate';
import { experimental_generateImage as generateImage } from 'ai';
import { writeFile } from 'node:fs/promises';

const { image } = await generateImage({
  model: replicate.image('black-forest-labs/flux-schnell'),
  prompt: 'Le monstre du Loch Ness se fait une manucure',
  aspectRatio: '16:9',
});

await writeFile('image.webp', image.uint8Array);

console.log('L\'image a été enregistrée sous le nom image.webp');
```

### Options spécifiques aux modèles

```ts highlight="9-11"
import { replicate } from '@ai-sdk/replicate';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: replicate.image('recraft-ai/recraft-v3'),
  prompt: 'Le monstre du Loch Ness se fait une manucure',
  size: '1365x1024',
  providerOptions: {
    replicate: {
      style: 'image_realiste',
    },
  },
});
```

### Modèles versionnés

```ts
import { replicate } from '@ai-sdk/replicate';
import { experimental_generateImage as generateImage } from 'ai';

const { image } = await generateImage({
  model: replicate.image(
    'bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637',
  ),
  prompt: 'Le monstre du Loch Ness se fait une manucure',
});
```

Pour plus de détails, voir la [page des modèles Replicate](https://replicate.com/explore).

---
titre : Perplexité
description : Apprenez à utiliser l'API Sonar de Perplexité avec le SDK AI.
---

# Fournisseur de Perplexité

Le [fournisseur Perplexité](https://sonar.perplexity.ai) offre accès à l'API Sonar - un modèle de langage qui combine de manière unique la recherche en temps réel sur le Web avec le traitement automatique du langage naturel. Chaque réponse est ancrée dans les données Web actuelles et comprend des citations détaillées, ce qui en fait un choix idéal pour la recherche, la vérification des faits et l'obtention d'informations à jour.

Les clés API peuvent être obtenues à partir de la [plateforme Perplexité](https://docs.perplexity.ai).

## Configuration

Le fournisseur Perplexité est disponible via le module `@ai-sdk/perplexity`. Vous pouvez l'installer avec :

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

## Instance du fournisseur

Vous pouvez importer l'instance par défaut du fournisseur `perplexity` depuis `@ai-sdk/perplexity` :

```ts
import { perplexity } from '@ai-sdk/perplexity';
```

Pour une configuration personnalisée, vous pouvez importer `createPerplexity` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createPerplexity } from '@ai-sdk/perplexity';

const perplexity = createPerplexity({
  apiKey: process.env.PERPLEXITY_API_KEY ?? '',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur Perplexity :

- **baseURL** _chaîne_

  Utilisez une adresse URL différente pour les appels API.
  La préfixe par défaut est `https://api.perplexity.ai`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`. Il est défini par défaut sur la variable d'environnement `PERPLEXITY_API_KEY`.

- **headers** _Enregistrement&lt;chaîne,chaîne&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input : RequestInfo, init ?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).

## Modèles de langage

Vous pouvez créer des modèles Perplexity en utilisant une instance de fournisseur :

```ts
import { perplexity } from '@ai-sdk/perplexity';
import { generateText } from 'ai';

const { text } = await generateText({
  model: perplexity('sonar-pro'),
  prompt: 'Quels sont les derniers développements dans le calcul quantique ?',
});
```

### Sources

Les sites web qui ont été utilisés pour générer la réponse sont inclus dans la propriété `sources` du résultat :

```ts
import { perplexity } from '@ai-sdk/perplexity';
import { generateText } from 'ai';

const { text, sources } = await generateText({
  model: perplexity('sonar-pro'),
  prompt: 'Quels sont les développements récents dans l'informatique quantique ?',
});

console.log(sources);
```

### Options de fournisseur & métadonnées

Le fournisseur Perplexity inclut des métadonnées supplémentaires dans la réponse grâce à `providerMetadata`.
Des options de configuration supplémentaires sont disponibles grâce à `providerOptions`.

```ts
const result = await generateText({
  model: perplexity('sonar-pro'),
  prompt: 'Quels sont les derniers développements dans le calcul quantique ?',
  providerOptions: {
    perplexity: {
      return_images: true, // Activer les réponses en images (utilisateurs Perplexity niveau 2 uniquement)
    },
  },
});

console.log(result.providerMetadata);
// Exemple de sortie :
// {
//   perplexity: {
//     usage: { citationTokens: 5286, numSearchQueries: 1 },
//     images: [
//       { imageUrl: "https://example.com/image1.jpg", originUrl: "https://elsewhere.com/page1", height: 1280, width: 720 },
//       { imageUrl: "https://example.com/image2.jpg", originUrl: "https://elsewhere.com/page2", height: 1280, width: 720 }
//     ]
//   },
// }
```

Les métadonnées incluent :

- `usage` : Objet contenant les métriques `citationTokens` et `numSearchQueries`
- `images` : Tableau d'URL d'images lorsqu'il est activé `return_images` (utilisateurs Perplexity niveau 2 et au-dessus uniquement)

Vous pouvez activer les réponses en images en définissant `return_images: true` dans les options de fournisseur. Cette fonctionnalité n'est disponible que pour les utilisateurs Perplexity niveau 2 et au-dessus.

<Note>
  Pour plus de détails sur les capacités de Perplexity, voir les [docs de complétion de chat de Perplexity](https://docs.perplexity.ai/api-reference/chat-completions).
</Note>

## Capacités du Modèle

| Modèle                 | Entrée d'Image         | Génération d'Objet   | Utilisation de l'Outil          | Flux d'Outil Streaming      |
| --------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| `sonar-pro`           | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `sonar`               | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |
| `sonar-deep-research` | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> | <Cross size={18} /> |

<Note>
  Veuillez consulter la [documentation de Perplexity](https://docs.perplexity.ai) pour la documentation API détaillée et les dernières mises à jour.
</Note>

---
title: Luma
description: Apprenez à utiliser les modèles Luma AI avec le SDK AI.
---

# Fournisseur Luma

[Luma AI](https://lumalabs.ai/) fournit des modèles de génération d'image de haute qualité à l'aide de leur plateforme Dream Machine. Les modèles de Luma offrent une génération d'image ultra-haute qualité avec une compréhension supérieure des prompts et des capacités uniques comme la cohérence des personnages et le support de référence multi-image.

## Installation

Le fournisseur Luma est disponible via le module `@ai-sdk/luma`. Vous pouvez l'installer avec

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

## Instance de fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `luma` à partir de `@ai-sdk/luma` :

```ts
import { luma } from '@ai-sdk/luma';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createLuma` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createLuma } from '@ai-sdk/luma';

const luma = createLuma({
  apiKey: 'votre-api-key', // facultatif, utilise par défaut la variable d'environnement LUMA_API_KEY
  baseURL: 'url-personnalisée', // facultatif
  headers: {
    /* en-têtes personnalisés */
  }, // facultatif
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur Luma :

- **baseURL** _chaîne_

  Utilisez une URL de prefixe différente pour les appels API, par exemple pour utiliser des serveurs proxy.
  Le prefixe par défaut est `https://api.lumalabs.ai`.

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Elle utilise par défaut la variable d'environnement `LUMA_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Vous pouvez l'utiliser comme middleware pour intercepter les requêtes,
  ou pour fournir une implémentation personnalisée de fetch pour la mise en œuvre de tests.

## Modèles d'image

Vous pouvez créer des modèles d'image Luma à l'aide de la méthode de fabrication `.image()`.
Pour plus d'informations sur la génération d'image avec le SDK AI, voir [generateImage()](/docs/reference/ai-sdk-core/generate-image).

### Utilisation de base

```ts
import { luma } from '@ai-sdk/luma';
import { experimental_generateImage as generateImage } from 'ai';
import fs from 'fs';

const { image } = await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Un paysage de montagne calme au coucher du soleil',
  aspectRatio: '16:9',
});

const filename = `image-${Date.now()}.png`;
fs.writeFileSync(filename, image.uint8Array);
console.log(`L'image a été enregistrée dans ${filename}`);
```

### Paramètres de modèles d'image

Lors de la création d'un modèle d'image, vous pouvez personnaliser le comportement de génération avec des paramètres facultatifs :

```ts
const model = luma.image('photon-1', {
  maxImagesPerCall: 1, // Nombre maximum d'images à générer par appel API
  pollIntervalMillis: 5000, // Fréquence de vérification des images terminées (en ms)
  maxPollAttempts: 10, // Nombre maximum d'essais de vérification avant le temps limite
});
```

Puisque Luma traite les images à travers un système de file d'attente asynchrone, ces paramètres vous permettent de régler le comportement de vérification :

- **maxImagesPerCall** _nombre_

  Définissez le nombre maximum d'images générées par appel API. Valeur par défaut : 1.

- **pollIntervalMillis** _nombre_

  Contrôlez la fréquence à laquelle l'API est vérifiée pour des images terminées pendant leur traitement. Valeur par défaut : 500ms.

- **maxPollAttempts** _nombre_

  Limitez le temps d'attente pour les résultats avant le temps limite, puisque la génération d'image est traitée de manière asynchrone. Valeur par défaut : 120 essais.

### Capacités du Modèle

Luma offre deux principaux modèles :

| Modèle            | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `photon-1`       | Génération d'images de haute qualité avec une compréhension supérieure des commandes |
| `photon-flash-1` | Génération accélérée optimisée pour la vitesse tout en maintenant la qualité  |

Les deux modèles prennent en charge les ratios d'aspect suivants :

- 1:1
- 3:4
- 4:3
- 9:16
- 16:9 (par défaut)
- 9:21
- 21:9

Pour plus de détails sur les ratios d'aspect pris en charge, voir la [documentation de génération d'images de Luma](https://docs.lumalabs.ai/docs/image-generation).

Les caractéristiques clés des modèles Luma incluent :

- Génération d'images de haute qualité extrême
- Une efficacité de 10 fois supérieure au coût par rapport aux modèles similaires
- Une compréhension et une adhésion des commandes supérieures
- Des capacités uniques de cohérence de caractères à partir d'images de référence unique
- Support de plusieurs images de référence pour un ajustement de style précis

### Options Avancées

Les modèles Luma prennent en charge plusieurs fonctionnalités avancées à travers le paramètre `providerOptions.luma`.

#### Référence d'image

Utilisez jusqu'à 4 images de référence pour guider votre génération. Utile pour créer des variations ou visualiser des concepts complexes. Ajustez la `poids` (0-1) pour contrôler l'influence des images de référence.

```ts
// Exemple : Générer un triton avec référence
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Un triton à la tombée de la nuit dans un étang forestier, dans le style de l'ukiyo-e',
  providerOptions: {
    luma: {
      image_ref: [
        {
          url: 'https://example.com/referencem.jpg',
          weight: 0,85,
        },
      ],
    },
  },
});
```

#### Référence de style

Appliquez des styles visuels spécifiques à vos générations en utilisant des images de référence. Contrôlez l'influence du style en utilisant le paramètre `poids`.

```ts
// Exemple : Générer avec référence de style
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Un chat persan crème bleu en train de lancer son site web sur Vercel',
  providerOptions: {
    luma: {
      style_ref: [
        {
          url: 'https://example.com/style.jpg',
          weight: 0,8,
        },
      ],
    },
  },
});
```

#### Référence de Personnage

Créez des personnages cohérents et personnalisés en utilisant jusqu'à 4 images de référence du même sujet. Plus d'images de référence améliorent la représentation du personnage.

```ts
// Exemple : Générer une image basée sur le personnage
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'Une femme avec un chat monté sur une baguette à balai dans une forêt',
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

#### Modifier l'Image

Transformez les images existantes à l'aide de prompts de texte. Utilisez le paramètre `weight` pour contrôler à quelle mesure le résultat correspond à l'image d'entrée (poids plus élevé = plus proche de l'image d'entrée mais moins créatif).

<Remarque>
  Pour les changements de couleur, il est recommandé d'utiliser une valeur de poids plus basse (0.0-0.1).
</Remarque>

```ts
// Exemple : Modifier une image existante
await generateImage({
  model: luma.image('photon-1'),
  prompt: 'transformer la bicyclette en bateau',
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

Pour plus de détails sur les capacités et les fonctionnalités de Luma, visitez la [documentation de génération d'images de Luma](https://docs.lumalabs.ai/docs/image-generation).

---
titre : ElevenLabs
description : Apprenez à utiliser le fournisseur ElevenLabs pour le SDK AI.
---

# Fournisseur ElevenLabs

Le [fournisseur ElevenLabs](https://elevenlabs.io/) contient un support de modèle de langage pour l'API de transcription ElevenLabs.

## Configuration

Le fournisseur ElevenLabs est disponible dans le module `@ai-sdk/elevenlabs`. Vous pouvez l'installer avec

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

## Instance du Fournisseur

Vous pouvez importer l'instance de fournisseur par défaut `elevenlabs` à partir de `@ai-sdk/elevenlabs` :

```ts
import { elevenlabs } from '@ai-sdk/elevenlabs';
```

Si vous avez besoin d'une configuration personnalisée, vous pouvez importer `createElevenLabs` à partir de `@ai-sdk/elevenlabs` et créer une instance de fournisseur avec vos paramètres :

```ts
import { createElevenLabs } from '@ai-sdk/elevenlabs';

const elevenlabs = createElevenLabs({
  // paramètres personnalisés, par exemple
  fetch: customFetch,
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance du fournisseur ElevenLabs :

- **apiKey** _chaîne_

  Clé API qui est envoyée en utilisant l'en-tête `Authorization`.
  Cela prend par défaut la variable d'environnement `ELEVENLABS_API_KEY`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés à inclure dans les requêtes.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch).
  Cela prend par défaut la fonction globale `fetch`.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour la mise en œuvre de tests, par exemple.

## Modèles de transcription

Vous pouvez créer des modèles qui appellent l'[API de transcription d'ElevenLabs](https://elevenlabs.io/speech-to-text)
en utilisant la méthode de fabrication `.transcription()`.

La première argument est l'identifiant du modèle, par exemple `scribe_v1`.

```ts
const model = elevenlabs.transcription('scribe_v1');
```

Vous pouvez également passer des options spécifiques au fournisseur en utilisant l'argument `providerOptions`. Par exemple, en fournissant le code de langue en format ISO-639-1 (par exemple `en`) peut améliorer les performances de transcription si connu à l'avance.

```ts highlight="6"
import { experimental_transcribe as transcribe } from 'ai';
import { elevenlabs } from '@ai-sdk/elevenlabs';

const result = await transcribe({
  model: elevenlabs.transcription('scribe_v1'),
  audio: new Uint8Array([1, 2, 3, 4]),
  providerOptions: { elevenlabs: { languageCode: 'en' } },
});
```

Les options de fournisseur suivantes sont disponibles :

- **languageCode** _chaîne_

  Un code de langue ISO-639-1 ou ISO-639-3 correspondant au langage du fichier audio.
  Peut améliorer les performances de transcription si connu à l'avance.
  Par défaut à `null`, dans lequel le langage est prédit automatiquement.

- **tagAudioEvents** _booléen_

  Si marquer les événements audio comme (rire), (pas), etc. dans la transcription.
  Par défaut à `true`.

- **numSpeakers** _entier_

  La quantité maximale de locuteurs parlant dans le fichier téléchargé.
  Peut aider à prédire qui parle quand.
  La quantité maximale de locuteurs qui peut être prédite est de 32.
  Par défaut à `null`, dans lequel la quantité de locuteurs est définie sur la valeur maximale prise en charge par le modèle.

- **timestampsGranularity** _enum_

  La granularité des horodatages dans la transcription.
  Par défaut à `'word'`.
  Les valeurs autorisées : `'none'`, `'word'`, `'character'`.

- **diarize** _booléen_

**Annoter le locuteur actuel dans le fichier téléchargé**
  Défaut à `true`.

- **fileFormat** _enum_

  Le format de l'audio d'entrée.
  Défaut à `'other'`.
  Valeurs autorisées : `'pcm_s16le_16'`, `'other'`.
  Pour `'pcm_s16le_16'`, l'audio d'entrée doit être un PCM de 16 bits à une fréquence d'échantillonnage de 16 kHz, canal unique (mono) et ordre de bits petit (little-endian).
  La latence sera inférieure à celle obtenue en passant un ondelette codée.

### Capabilités du Modèle

| Modèle                    | Transcription       | Durée            | Segments            | Langue            |
| ------------------------ | ------------------- | ------------------- | ------------------- | ------------------- |
| `scribe_v1`              | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |
| `scribe_v1_experimental` | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> | <Check size={18} /> |

---
Titre : Studio LM
Description : Utilisez l'API compatible OpenAI avec le SDK AI.
---

# Fournisseur Studio LM

[Studio LM](https://lmstudio.ai/) est une interface utilisateur pour exécuter des modèles locaux.

Il contient un serveur d'API compatible OpenAI que vous pouvez utiliser avec le SDK AI.
Vous pouvez démarrer le serveur local sous l'onglet [Serveur local](https://lmstudio.ai/docs/basics/server) dans l'interface utilisateur de Studio LM ("Démarrer le serveur").

## Configuration

Le fournisseur Studio LM est disponible via le module `@ai-sdk/openai-compatible` car il est compatible avec l'API OpenAI.
Vous pouvez l'installer avec

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

## Instance de fournisseur

Pour utiliser LM Studio, vous pouvez créer une instance de fournisseur personnalisée avec la fonction `createOpenAICompatible` de `@ai-sdk/openai-compatible` :

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'http://localhost:1234/v1',
});
```

<Note>
  LM Studio utilise le port `1234` par défaut, mais vous pouvez le modifier dans la [rubrique Serveur local de l'application](https://lmstudio.ai/docs/basics/server).
</Note>

## Modèles de langage

Vous pouvez interagir avec des LLM locaux dans [LM Studio](https://lmstudio.ai/docs/basics/server#endpoints-overview) à l'aide d'une instance de fournisseur.
La première argument est l'ID du modèle, par exemple `llama-3.2-1b`.

```ts
const model = lmstudio('llama-3.2-1b');
```

###### Pour utiliser un modèle, vous devez le télécharger d'abord. [Téléchargez-le](https://lmstudio.ai/docs/basics/download-model).

### Exemple

Vous pouvez utiliser les modèles de langage de LM Studio pour générer du texte avec la fonction `generateText` :

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'https://localhost:1234/v1',
});

const { text } = await generateText({
  model: lmstudio('llama-3.2-1b'),
  prompt: 'Écrivez une recette de lasagne végétarienne pour 4 personnes.',
  maxRetries: 1, // erreur immédiate si le serveur n'est pas en cours d'exécution
});
```

Les modèles de langage de LM Studio peuvent également être utilisés avec `streamText`.

## Embedding des Modèles

Vous pouvez créer des modèles qui appellent l'[API d'embeddings de LM Studio](https://lmstudio.ai/docs/basics/server#endpoints-overview)
à l'aide de la méthode de fabrication `.embedding()`.

```ts
const model = lmstudio.embedding('text-embedding-nomic-embed-text-v1.5');
```

### Exemple - Embedding d'une Valeur Unique

```tsx
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { embed } from 'ai';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'https://localhost:1234/v1',
});

// 'embedding' est un objet d'embeddings unique (tableau de nombres)
const { embedding } = await embed({
  model: lmstudio.textEmbeddingModel('text-embedding-nomic-embed-text-v1.5'),
  value: 'jour ensoleillé à la plage',
});
```

### Exemple - Embedding de plusieurs valeurs

Lors du chargement de données, par exemple lors de la préparation d'un magasin de données pour la génération augmentée par la récupération (RAG),
il est souvent utile d'embed de nombreuses valeurs à la fois (embedding en batch).

Le SDK AI fournit la fonction `embedMany` (`/docs/reference/ai-sdk-core/embed-many`) à cet effet.
De même que `embed`, vous pouvez l'utiliser avec des modèles d'embeddings,
par exemple `lmstudio.textEmbeddingModel('text-embedding-nomic-embed-text-v1.5')` ou `lmstudio.textEmbeddingModel('text-embedding-bge-small-en-v1.5')`.

```tsx
import { createOpenAICompatible } from '@ai-sdk/openai';
import { embedMany } from 'ai';

const lmstudio = createOpenAICompatible({
  name: 'lmstudio',
  baseURL: 'https://localhost:1234/v1',
});

// 'embeddings' est un tableau d'objets d'embeddings (number[][]).
// Il est classé dans le même ordre que les valeurs d'entrée.
const { embeddings } = await embedMany({
  model: lmstudio.textEmbeddingModel('text-embedding-nomic-embed-text-v1.5'),
  values: [
    'jour ensoleillé à la plage',
    'après-midi pluvieux dans la ville',
    'nuit enneigée dans les montagnes',
  ],
});
```

---
titre : NVIDIA NIM
description : Utilisez l'API compatible OpenAI de NVIDIA NIM avec le SDK AI.
---

# Fournisseur NVIDIA NIM

[NVIDIA NIM](https://www.nvidia.com/en-us/ai/) fournit des microservices d'inference optimisés pour déployer des modèles de fondation. Il offre une API compatible OpenAI que vous pouvez utiliser avec le SDK AI.

## Configuration

Le fournisseur NVIDIA NIM est disponible via le module `@ai-sdk/openai-compatible` car il est compatible avec l'API OpenAI.
Vous pouvez l'installer avec :

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

## Instance du fournisseur

Pour utiliser NVIDIA NIM, vous pouvez créer une instance personnalisée du fournisseur avec la fonction `createOpenAICompatible` de `@ai-sdk/openai-compatible` :

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

<Note>
  Vous pouvez obtenir une clé API et des crédits gratuits en vous inscrivant sur [NVIDIA
  Build](https://build.nvidia.com/explore/discover). Les nouveaux utilisateurs reçoivent 1 000
  crédits d'inference pour commencer.
</Note>

## Modèles de langage

Vous pouvez interagir avec les modèles NIM à l'aide d'une instance de fournisseur. Par exemple, pour utiliser [DeepSeek-R1](https://build.nvidia.com/deepseek-ai/deepseek-r1), un puissant modèle de langage open-source :

```ts
const model = nim.chatModel('deepseek-ai/deepseek-r1');
```

### Exemple - Générer du Texte

Vous pouvez utiliser les modèles de langage NIM pour générer du texte avec la fonction `generateText` :

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

const { texte, usage, finishReason } = await generateText({
  model: nim.chatModel('deepseek-ai/deepseek-r1'),
  prompt: 'Dites-moi l\'histoire du burrito de style Mission de San Francisco.',
});

console.log(texte);
console.log('Utilisation des jetons :', usage);
console.log('Raison de terminaison :', finishReason);
```

### Exemple - Flux de Texte

Les modèles de langage NIM peuvent également générer du texte de manière en flux avec la fonction `streamText` :

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
  prompt: 'M'ecrivez-moi l'histoire du Rhinocéros Blanc du Nord.',
});

for await (const textPart of result.textStream) {
  process.stdout.write(textPart);
}

console.log();
console.log('Utilisation de jetons :', await result.usage);
console.log('Raison de fin :', await result.finishReason);
```

Les modèles de langage NIM peuvent également être utilisés avec d'autres fonctions du SDK AI comme `generateObject` et `streamObject`.

<Note>
  La prise en charge des modèles pour les appels d'outils et la génération d'objets structurés varie. Par exemple, le modèle
  [`meta/llama-3.3-70b-instruct`](https://build.nvidia.com/meta/llama-3_3-70b-instruct)
  prend en charge les capacités de génération d'objets. Vérifiez la documentation spécifique de chaque modèle sur NVIDIA Build pour les fonctionnalités prises en charge.
</Note>

---
titre : Fournisseurs OpenAI compatibles
description : Utilisez les fournisseurs OpenAI compatibles avec le SDK AI.
---

# Fournisseurs Compatible avec OpenAI

Vous pouvez utiliser le [package Fournisseur Compatible avec OpenAI](https://www.npmjs.com/package/@ai-sdk/openai-compatible) pour utiliser des fournisseurs de modèles de langage qui implémentent l'API OpenAI.

Nous nous concentrons ci-dessous sur la configuration générale et la création d'une instance de fournisseur. Vous pouvez également [écrire un package de fournisseur personnalisé en utilisant le package Compatible avec OpenAI](/providers/openai-compatible-providers/custom-providers).

Nous fournissons une documentation détaillée pour les fournisseurs OpenAI compatibles suivants :

- [LM Studio](/providers/openai-compatible-providers/lmstudio)
- [NIM](/providers/openai-compatible-providers/nim)
- [Baseten](/providers/openai-compatible-providers/baseten)

La configuration générale et la création d'une instance de fournisseur sont les mêmes pour tous ces fournisseurs.

## Configuration

Le fournisseur Compatible avec OpenAI est disponible via le module `@ai-sdk/openai-compatible`. Vous pouvez l'installer avec :

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

## Instance de fournisseur

Pour utiliser un fournisseur compatible avec OpenAI, vous pouvez créer une instance de fournisseur personnalisée avec la fonction `createOpenAICompatible` de `@ai-sdk/openai-compatible` :

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const provider = createOpenAICompatible({
  name: 'nom-du-fournisseur',
  apiKey: process.env.API_KEY_DU_FOURNISSEUR,
  baseURL: 'https://api.fournisseur.com/v1',
});
```

Vous pouvez utiliser les paramètres facultatifs suivants pour personnaliser l'instance de fournisseur :

- **baseURL** _chaîne_

  Définit l'URL de prefixe pour les appels API.

- **apiKey** _chaîne_

  Clé API pour authentifier les requêtes. Si spécifiée, ajoute un en-tête `Authorization`
  aux en-têtes de requête avec la valeur `Bearer <apiKey>`. Cela sera ajouté
  avant tout en-tête potentiellement spécifié dans l'option `headers`.

- **headers** _Record&lt;string,string&gt;_

  En-têtes personnalisés facultatifs à inclure dans les requêtes. Ces en-têtes seront ajoutés aux en-têtes de requête
  après tout en-tête potentiellement ajouté par l'utilisation de l'option `apiKey`.

- **queryParams** _Record&lt;string,string&gt;_

  Paramètres de requête URL facultatifs à inclure dans les URL de requête.

- **fetch** _(input: RequestInfo, init?: RequestInit) => Promise&lt;Response&gt;_

  Implémentation personnalisée de [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch). Par défaut, utilise la fonction `fetch` globale.
  Vous pouvez l'utiliser comme un middleware pour intercepter les requêtes,
  ou pour fournir une implémentation de fetch personnalisée pour des tests, par exemple.

## Modèles de langage

Vous pouvez créer des modèles de fournisseur à l'aide d'une instance de fournisseur.
La première argument est l'identifiant du modèle, par exemple `modele-id`.

```ts
const model = provider('modele-id');
```

### Exemple

Vous pouvez utiliser des modèles de langage de fournisseur pour générer du texte avec la fonction `generateText` :

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

const provider = createOpenAICompatible({
  name: 'nom-du-fournisseur',
  apiKey: process.env.API_KEY_DU_FOURNISSEUR,
  baseURL: 'https://api.fournisseur.com/v1',
});

const { text } = await generateText({
  model: provider('id-du-modele'),
  prompt: 'Écrivez une recette de lasagnes végétariennes pour 4 personnes.',
});
```

### Inclure les identifiants de modèle pour la complétion automatique

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { generateText } from 'ai';

type ExemplesDIdentifiantsDeModèlesDeConversation =
  | 'meta-llama/Llama-3-70b-chat-hf'
  | 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
  | (string & {});

type ExemplesDIdentifiantsDeModèlesDeComplétion =
  | 'codellama/CodeLlama-34b-Instruct-hf'
  | 'Qwen/Qwen2.5-Coder-32B-Instruct'
  | (string & {});

type ExemplesDIdentifiantsDeModèlesDEmbedding =
  | 'BAAI/bge-large-en-v1.5'
  | 'bert-base-uncased'
  | (string & {});

const modèle = createOpenAICompatible<
  ExemplesDIdentifiantsDeModèlesDeConversation,
  ExemplesDIdentifiantsDeModèlesDeComplétion,
  ExemplesDIdentifiantsDeModèlesDEmbedding
>({
  nom : 'exemple',
  apiKey : process.env.PROVIDER_API_KEY,
  baseURL : 'https://api.example.com/v1',
});

// Les appels ultérieurs à e.g. `modèle.modèleDeConversation` compléteront automatiquement
// l'identifiant de modèle à partir de la liste de

### Paramètres de requête personnalisés

Certains fournisseurs peuvent nécessiter des paramètres de requête personnalisés. Un exemple est l'[API d'inférence de modèle Azure AI](https://learn.microsoft.com/fr-fr/azure/machine-learning/reference-model-inference-chat-completions?view=azureml-api-2)
qui nécessite un paramètre de requête `api-version`.

Vous pouvez définir ces paramètres via la configuration facultative `queryParams` du fournisseur. Ces paramètres seront ajoutés à toutes les requêtes effectuées par le fournisseur.

```ts highlight="7-9"
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const provider = createOpenAICompatible({
  name: 'nom-du-fournisseur',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.fournisseur.com/v1',
  queryParams: {
    'api-version': '1.0.0',
  },
});
```

Par exemple, avec la configuration ci-dessus, les requêtes API incluront le paramètre de requête dans l'URL comme suit :
`https://api.fournisseur.com/v1/chat/completions?api-version=1.0.0`.

## Options spécifiques au fournisseur

Le fournisseur compatible OpenAI prend en charge l'ajout d'options spécifiques au fournisseur au corps de la requête. Ces options sont spécifiées avec le champ `providerOptions` dans le corps de la requête.

Par exemple, si vous créez une instance de fournisseur avec le nom `provider-name`, vous pouvez ajouter un champ `custom-option` au corps de la requête comme suit :

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

Le corps de la requête envoyé au fournisseur inclura le champ `customOption` avec la valeur `magic-value`. Cela vous permet d'ajouter facilement des options spécifiques au fournisseur aux requêtes sans avoir à modifier le code du fournisseur ou du SDK AI.

## Extraction de Métadonnées personnalisées

Le fournisseur compatible avec OpenAI prend en charge l'extraction de métadonnées fournisseur spécifiques à partir des réponses API à l'aide d'extracteurs de métadonnées.
Ces extracteurs vous permettent de capturer des informations supplémentaires renvoyées par le fournisseur au-delà du format de réponse standard.

Les extracteurs de métadonnées reçoivent les données de réponse brutes et non traitées du fournisseur, vous offrant ainsi une flexibilité complète
pour extraire n'importe quels champs personnalisés ou fonctionnalités expérimentales que le fournisseur peut inclure.
Cela est particulièrement utile dans les cas suivants :

- Travail avec des fournisseurs qui incluent des champs de réponse non standard
- Expérimentation avec des fonctionnalités bêta ou de prévisualisation
- Captage de métriques ou d'informations de débogage fournisseur spécifiques
- Support de l'évolution rapide de l'API fournisseur sans changement des SDK

Les extracteurs de métadonnées fonctionnent avec les complétions de chat à flux et non à flux, et se composent de deux composants principaux :

1. Une fonction pour extraire les métadonnées à partir de réponses complètes
2. Un extracteur à flux qui peut accumuler les métadonnées à travers des tranches dans une réponse à flux

Voici un exemple d'extracteur de métadonnées qui capture à la fois les données standard et personnalisées du fournisseur :

```typescript
const monExtracteurDeMétadonnées: MetadataExtractor = {
  // Traitement des réponses complètes, non à flux
  extractMetadata: ({ parsedBody }) => {
    // Vous avez accès à la réponse brute complète
    // Extraire n'importe quels champs que le fournisseur inclut
    return {
      monFournisseur: {
        utilisationStandard: parsedBody.usage,
        fonctionnalitésExpérimentales: parsedBody.beta_features,
        métriquesPersonnalisées: {
          tempsDeTraitement: parsedBody.server_timing?.total_ms,
          versionDuModèle: parsedBody.model_version,
          // ... n'importe quelles autres données fournisseur spécifiques
        },
      },
    };
  },

  // Traitement des réponses à flux
  createStreamExtractor: () => {
    let donnéesAccumulées = {
      timing: [],
      champsPersonnalisés: {},
    };
```

```markdown
retour {
  // Traitez chaque morceau de données brute
  processChunk: parsedChunk => {
    if (parsedChunk.server_timing) {
      accumulatedData.timing.push(parsedChunk.server_timing);
    }
    if (parsedChunk.custom_data) {
      Object.assign(accumulatedData.customFields, parsedChunk.custom_data);
    }
  },
  // Construit les métadonnées finales à partir des données accumulées
  buildMetadata: () => ({
    monFournisseur: {
      streamTiming: accumulatedData.timing,
      customData: accumulatedData.customFields,
    },
  }),
};

},
```

Vous pouvez fournir un extrayeur de métadonnées lors de la création de votre instance de fournisseur :

```typescript
const fournisseur = createOpenAICompatible({
  nom: 'mon-fournisseur',
  apiKey: process.env.PROVIDER_API_KEY,
  baseURL: 'https://api.fournisseur.com/v1',
  metadataExtractor: monMetadataExtractor,
});
```

Les métadonnées extraites seront incluses dans la réponse sous le champ `providerMetadata` :

```typescript
const { texte, providerMetadata } = await generateText({
  modèle: fournisseur('modele-id'),
  prompt: 'Bonjour',
});

console.log(providerMetadata.monFournisseur.customMetric);
```

Cela vous permet d'accéder à des informations spécifiques au fournisseur tout en maintenant une interface cohérente à travers différents fournisseurs.