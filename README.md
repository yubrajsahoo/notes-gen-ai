# note-gen-ai

AI-powered lecture recording, transcription, note generation, note management, and practice platform.

## 1. Product Flow

The primary user journey is:

```text
User opens application
        |
        v
+-----------------------+
| Start Recording       |
+-----------------------+
        |
        v
Ask for:
- Microphone permission
- Screen/display permission
        |
        v
Capture:
- Microphone audio
- System/display audio when available
- Screen/video
        |
        v
+-----------------------+
| Transcription Service |
| Python + FastAPI      |
| Faster-Whisper        |
+-----------------------+
        |
        v
Live transcription
        |
        v
User clicks Stop Recording
        |
        v
Show Templates
        |
        v
User selects template
        |
        v
+-----------------------+
| Notes Gen Service     |
| Java + SpringBoot      |
| Gemini AI             |
+-----------------------+
        |
        v
Generated Note
        |
        v
+-----------------------+
| Notes Management      |
| Java + Spring Boot    |
+-----------------------+
        |
        v
Save note in selected folder
```

## 2. Main Modules

### Frontend - note-gen-ui
Technology:
- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Zustand
- WebSocket
- MediaRecorder API
- Screen Capture API
- Web Audio API

Main screens:
- Start Recording
- Recording
- Live Transcription
- Template Selection
- Generated Note
- My Notes
- Practice
- Credits
- Payment
- Profile

### 1. Transcription Service
Technology:
- Python
- FastAPI
- Faster-Whisper
- FFmpeg
- WebSocket
- RabbitMQ
- MongoDB/PostgreSQL as required

Responsibilities:
- Receive audio/video chunks
- Extract/process audio
- Transcribe speech
- Publish live transcript
- Publish `TranscriptionCompleted`

### 2. Notes Generation Service
Technology:
- Python
- FastAPI
- Gemini AI
- RabbitMQ
- Prompt/template engine

Responsibilities:
- Receive transcript
- Receive selected template
- Build Gemini prompt
- Generate structured notes
- Generate summaries, key points, questions, flashcards, etc.
- Return/publish generated note
- Publish `NoteGenerationCompleted`

### 3. Templates Service
Technology:
- Java
- Spring Boot
- Spring Data JPA
- PostgreSQL

Responsibilities:
- Create templates
- Update templates
- Delete templates
- List templates
- Store prompt definitions
- Store template metadata
- Support system and user templates

### 4. Notes Management Service - My Notes
Technology:
- Java
- Spring Boot
- Spring Data JPA
- PostgreSQL
- MongoDB if large document content is required
- Object storage for exports

Responsibilities:
- Store notes
- Create folders
- Move notes between folders
- Rename notes
- Modify notes
- Search notes
- Favorite/archive notes
- Download/export notes
- Delete notes
- Version notes
- Manage note ownership

### 5. Practice Service
Technology:
- Java
- Spring Boot
- PostgreSQL
- RabbitMQ
- Gemini integration for generate questions

Responsibilities:
- Read notes
- Generate practice questions
- Exams
- MCQ
- True/False
- Flashcards
- Scoring
- Practice history
- Progress tracking

### 6. Credit Management Service
Technology:
- Java
- Spring Boot
- PostgreSQL
- Redis
- RabbitMQ

Responsibilities:
- Maintain user credit balance
- Reserve credits
- Consume credits
- Release credits on failed AI generation
- Credit history
- Credit packages
- Usage limits

### 7. Payment Service
Technology:
- Java
- Spring Boot
- PostgreSQL
- Razorpay or another UPI-capable payment provider
- Webhooks

Responsibilities:
- Create payment orders
- Handle UPI payments
- Verify payment
- Process payment webhooks
- Maintain payment history
- Refund support
- Publish `PaymentCompleted`

Do not let the frontend directly mark a payment as successful.

### 8. User Management Service
Technology:
- Java
- Spring Boot
- Spring Security
- JWT / OAuth2 / OpenID Connect
- PostgreSQL
- Redis

Responsibilities:
- Registration
- Login
- Refresh tokens
- User profile
- Roles
- Preferences
- Account management

## 3. API Gateway

Recommended:
- Java
- Spring Cloud Gateway

Responsibilities:
- Single entry point
- Routing
- Authentication checks
- CORS
- Rate limiting
- Request ID
- Security headers
- API versioning

Frontend should normally communicate with:

```text
React -> API Gateway -> Microservices
```

instead of directly calling every service.

## 4. Architecture

```text
                         +-----------------------+
                         | React + TypeScript UI |
                         +-----------+-----------+
                                     |
                                  HTTPS/WS
                                     |
                                     v
                         +-----------------------+
                         |    API Gateway        |
                         | Spring Cloud Gateway  |
                         +-----------+-----------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
              v                      v                      v
      +---------------+      +---------------+      +---------------+
      | User Service  |      | Notes Mgmt    |      | Templates     |
      | Java/Spring   |      | Java/Spring   |      | Java/Spring   |
      +-------+-------+      +-------+-------+      +-------+-------+
              |                      |                      |
              +----------------------+----------------------+
                                     |
                                  RabbitMQ
                                     |
              +----------------------+----------------------+
              |                                             |
              v                                             v
      +--------------------+                       +--------------------+
      | Transcription      |                       | Notes Generation   |
      | Python/FastAPI     |                       | Python/FastAPI     |
      | Faster-Whisper     |                       | Gemini AI          |
      +--------------------+                       +--------------------+
              |                                             |
              +----------------------+----------------------+
                                     |
                                     v
                            +------------------+
                            | Practice Service|
                            | Java/Spring     |
                            +------------------+

        +--------------------+       +----------------------+
        | Credit Management  |       | Payment Service      |
        | Java/Spring        |       | Java/Spring          |
        +--------------------+       +----------------------+

Infrastructure:
PostgreSQL | MongoDB | Redis | RabbitMQ | S3/MinIO
Prometheus | Grafana | OpenTelemetry | Tempo | Loki
Docker | Kubernetes | GitHub Actions
```

## 5. Full Recording Flow

### Step 1 - Start Recording

The UI displays:

```text
+------------------+
| Start Recording  |
+------------------+
```

### Step 2 - Permissions

Request:
1. Microphone access
2. Display/screen access

The browser's permission UI should be used. The application should explain why each permission is needed.

### Step 3 - Capture

Use:
- `navigator.mediaDevices.getUserMedia()` for microphone
- `navigator.mediaDevices.getDisplayMedia()` for screen/display
- `MediaRecorder` for recording
- Web Audio API for audio mixing when needed

Important browser limitation:

Display capture may provide system audio depending on browser, operating system, and user-selected sharing source. The application must handle cases where system audio is unavailable.

### Step 4 - Chunking

Do not wait until the entire lecture is finished.

Send small chunks:

```text
Browser
   |
   +-- chunk 1 --> Transcription Service
   +-- chunk 2 --> Transcription Service
   +-- chunk 3 --> Transcription Service
   +-- chunk 4 --> Transcription Service
```

This allows near-live transcription.

### Step 5 - Live Transcript

Use WebSocket:

```text
Browser <==== WebSocket ====> Transcription Service
```

UI:

```text
--------------------------------------
 Live Transcription
--------------------------------------
Today we are learning Spring Boot...

Spring Boot provides automatic
configuration...

The application context is responsible
for managing beans...
--------------------------------------
```

### Step 6 - Stop Recording

When the user clicks Stop:

```text
Recording stopped
       |
       v
Finalize transcript
       |
       v
Save recording/transcript
       |
       v
Show Templates
```

### Step 7 - Template Selection

Example:

```text
[ Lecture Notes ]
[ Cornell Notes ]
[ Summary ]
[ Detailed Study Notes ]
[ Interview Notes ]
[ Custom Template ]
```

### Step 8 - Gemini AI

```text
Transcript
+
Selected Template
+
User preferences
+
Generation options
        |
        v
     Gemini AI
        |
        v
Structured Note
```

### Step 9 - Display Note

Show:
- Title
- Summary
- Key points
- Sections
- Important concepts
- Examples
- Questions
- Flashcards

### Step 10 - Save

User selects:

```text
My Notes
  |
  +-- Java
  +-- Spring Boot
  +-- College
  +-- Work
  +-- Personal
```

Then:

```text
Generated Note
      |
      v
Notes Management Service
      |
      v
Selected Folder
```

## 6. My Notes

My Notes is the central note-management area.

Features:
- Folder creation
- Note creation
- Rename
- Edit
- Move
- Copy
- Delete
- Favorite
- Archive
- Search
- Tags
- Version history
- Download/export
- Change template and regenerate
- Share later if required

Suggested export formats:
- PDF
- Markdown
- TXT
- DOCX

## 7. Practice

Practice is based on saved notes.

```text
My Note
   |
   v
Practice Service
   |
   +--> MCQ
   +--> True/False
   +--> Flashcards
   +--> Short Answer
   +--> Mock Exam
   |
   v
Score + Progress
```

## 8. Credits

Suggested flow:

```text
AI Request
    |
    v
Credit Management
    |
    +--> Check balance
    |
    +--> Reserve credits
             |
             v
        Gemini AI
             |
       +-----+-----+
       |           |
    Success      Failure
       |           |
       v           v
    Consume      Release
    credits      credits
```

This avoids charging users when an AI generation fails.

## 9. Payment

For UPI payments:

```text
User
 |
 v
Frontend
 |
 v
API Gateway
 |
 v
Payment Service
 |
 v
Payment Provider
 |
 v
UPI
 |
 v
Webhook
 |
 v
Payment Service
 |
 v
Credit Management
```

The payment service should verify provider webhooks server-side.

## 10. Suggested Data Ownership

Use logical database-per-service ownership.

```text
User Service
  -> user_db

Templates Service
  -> template_db

Notes Management
  -> notes_db

Practice Service
  -> practice_db

Payment Service
  -> payment_db

Credit Management
  -> credit_db

Transcription
  -> transcription data

Notes Generation
  -> generation/job data
```

Shared infrastructure can be:

```text
PostgreSQL
MongoDB
Redis
RabbitMQ
S3/MinIO
```

Avoid a shared schema where every service directly modifies another service's tables.

## 11. Event Model

Recommended RabbitMQ events:

```text
UserRegistered
RecordingStarted
AudioChunkUploaded
TranscriptionStarted
TranscriptionCompleted
TranscriptionFailed

NoteGenerationRequested
NoteGenerationStarted
NoteGenerationCompleted
NoteGenerationFailed

NoteCreated
NoteUpdated
NoteDeleted

CreditsReserved
CreditsConsumed
CreditsReleased
PaymentCreated
PaymentCompleted
PaymentFailed

PracticeStarted
PracticeCompleted
```

## 12. Technology Stack

### Frontend

```text
React
TypeScript
Vite
React Router
TanStack Query
Zustand
Axios
WebSocket
MediaRecorder API
Screen Capture API
Web Audio API
```

### Java

```text
Java 21+
Spring Boot
Spring Security
Spring Data JPA
Hibernate
Spring Cloud Gateway
RabbitMQ / Spring AMQP
Micrometer
OpenTelemetry
JUnit 5
Mockito
Testcontainers
```

### Python

```text
Python 3.12+
FastAPI
Uvicorn
Faster-Whisper
FFmpeg
Pydantic
Pika or aio-pika
httpx
pytest
```

### AI

```text
Google Gemini AI
Gemini API
Faster-Whisper
Optional local LLM through Ollama
```

### Storage

```text
PostgreSQL
MongoDB
Redis
S3 / MinIO
```

### Messaging

```text
RabbitMQ
```

### Observability

```text
Prometheus
Grafana
OpenTelemetry
Tempo
Loki
```

### Deployment

```text
Docker
Docker Compose
Kubernetes
GitHub Actions
Container Registry
```

## 13. Recommended Local Ports

| Component | Port |
|---|---:|
| React UI | 3000 |
| API Gateway | 8080 |
| User Service | 8081 |
| Transcription Service | 8082 |
| Notes Generation | 8083 |
| Templates Service | 8084 |
| Notes Management | 8085 |
| Practice Service | 8086 |
| Payment Service | 8087 |
| Credit Management | 8088 |
| PostgreSQL | 5432 |
| MongoDB | 27017 |
| Redis | 6379 |
| RabbitMQ | 5672 |
| RabbitMQ Management | 15672 |
| Prometheus | 9090 |
| Grafana | 3001 |

## 14. Recommended Repository

```text
note-gen-ai/
|
+-- frontend/
|   +-- note-gen-ui/
|
+-- services/
|   +-- api-gateway/
|   +-- user-service/
|   +-- transcription-service/
|   +-- notes-gen-service/
|   +-- templates-service/
|   +-- notes-management-service/
|   +-- practice-service/
|   +-- payment-service/
|   +-- credit-management-service/
|
+-- infrastructure/
|   +-- docker/
|   +-- postgres/
|   +-- mongodb/
|   +-- redis/
|   +-- rabbitmq/
|   +-- prometheus/
|   +-- grafana/
|   +-- tempo/
|   +-- loki/
|   +-- kubernetes/
|
+-- docs/
|   +-- architecture/
|   +-- api/
|   +-- events/
|   +-- database/
|
+-- .github/
|   +-- workflows/
|
+-- README.md
```

## 15. Development Order

### Phase 1 - Core product
- User Service
- API Gateway
- React UI
- Transcription Service
- Notes Generation Service
- Notes Management Service

### Phase 2 - Organization
- Templates Service
- Folders
- Search
- Export/download
- Note editing

### Phase 3 - Learning
- Practice Service
- Quiz
- Exam
- Flashcards
- Progress

### Phase 4 - Monetization
- Credit Management
- Payment Service
- UPI
- Credit packages
- Subscription

### Phase 5 - Production
- RabbitMQ
- Redis
- MinIO/S3
- Prometheus
- Grafana
- OpenTelemetry
- Tempo
- Loki
- Docker
- Kubernetes
- CI/CD

## 16. Architecture Principles

1. Each microservice owns its business domain.
2. Do not share database tables across services.
3. Use REST for immediate operations.
4. Use RabbitMQ for long-running/asynchronous workflows.
5. Keep AI workloads in Python.
6. Keep transactional/business workloads in Java.
7. Keep browser/media functionality in React/TypeScript.
8. Never trust payment or credit values from the frontend.
9. Reserve credits before expensive AI work and consume/release them after completion.
10. Add tracing, metrics, and structured logging from the beginning.
11. Keep the Gemini integration behind a service abstraction so another LLM can be added later.
12. Store audio/video in object storage instead of database blobs.

## 17. Target Production Flow

```text
React/TS
   |
   v
API Gateway
   |
   +--------------------------+
   |                          |
   v                          v
Java Services             Python Services
   |                          |
   |                          +--> Faster-Whisper
   |                          |
   |                          +--> Gemini AI
   |
   +--> PostgreSQL
   +--> Redis
   +--> RabbitMQ
   +--> MongoDB
   +--> S3/MinIO

Observability:
OpenTelemetry -> Tempo
Metrics       -> Prometheus -> Grafana
Logs          -> Loki
```

The first production milestone should be:

**Start Recording → Permissions → Audio/Video Capture → Live Transcription → Stop → Template Selection → Gemini Note Generation → Show Note → Save to My Notes/Folders.**
