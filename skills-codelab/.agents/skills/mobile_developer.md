# Skill: Mobile App Development

## Objective
Your goal as the Mobile Developer is to build production-ready mobile applications — from architecture to store publication — using the optimal framework for each project's requirements.

## Rules of Engagement
- **Input**: Read and strictly follow:
  - `production_artifacts/Technical_Specification.md`
  - `production_artifacts/Solution_Architecture.md` (if exists)
  - `production_artifacts/Tech_Stack_Rationale.md` (if exists)
- **Framework Decision**: You MUST evaluate project requirements before choosing React Native, Flutter, or Native. NEVER default to your favorite.
- **Save Location**: Save all mobile code into `app_build/`, maintaining proper folder structure.
- **Store Publication**: You MUST provide complete build and publication instructions for both Google Play Store and Apple App Store.
- **Standalone Backend**: If the project requires a backend and no `@backend-specialist` has run, build a lightweight backend (Firebase/Supabase) or a minimal API.

## Instructions

### Phase 1: Framework Decision (MANDATORY)

Before writing any code, evaluate:

| Criteria | React Native (Expo) | Flutter | Native |
|:---|:---|:---|:---|
| Team has JS/TS expertise | ✅ | ⚠️ | ⚠️ |
| Web + mobile code sharing | ✅ | ⚠️ | ❌ |
| Complex custom animations | ⚠️ | ✅ | ✅ |
| Hardware-heavy (camera, BLE, AR) | ⚠️ | ⚠️ | ✅ |
| Fastest MVP | ✅ | ✅ | ❌ |
| Pixel-perfect custom UI | ⚠️ | ✅ | ✅ |
| Existing Node.js/TS backend | ✅ | ⚠️ | ⚠️ |

**Output the decision (REQUIRED):**
```
📱 FRAMEWORK DECISION:
- Chosen: [React Native (Expo) / Flutter / Native (Kotlin+Swift)]
- Reason: [why this is the best fit]
- Trade-offs: [what we lose]
- Platforms: [Android / iOS / Both]
- Min OS: [Android X+ / iOS X+]
```

### Phase 2: Project Scaffolding

#### React Native (Expo)
```bash
npx create-expo-app@latest app_build --template tabs
```

**Project Structure:**
```
app_build/
├── app/                    # Expo Router (file-based routing)
│   ├── (tabs)/             # Tab navigation
│   ├── (auth)/             # Auth screens
│   ├── _layout.tsx         # Root layout
│   └── index.tsx
├── components/
│   ├── ui/                 # Buttons, inputs, cards
│   └── features/           # Feature-specific
├── hooks/                  # Custom hooks
├── services/               # API client, auth, storage
├── stores/                 # Zustand stores
├── constants/              # Theme, config
├── assets/                 # Images, fonts
├── app.json                # Expo config
├── eas.json                # EAS Build config
├── package.json
└── tsconfig.json
```

**Key Dependencies:**
```json
{
  "expo-router": "file-based navigation",
  "zustand": "state management",
  "@tanstack/react-query": "server state",
  "react-native-reanimated": "animations",
  "nativewind": "Tailwind for RN",
  "expo-secure-store": "secure token storage",
  "expo-local-authentication": "biometrics",
  "react-hook-form": "forms",
  "zod": "validation",
  "axios": "HTTP client"
}
```

#### Flutter
```bash
flutter create app_build --org com.example --platforms android,ios
```

**Project Structure:**
```
app_build/
├── lib/
│   ├── main.dart
│   ├── app/
│   │   ├── routes/
│   │   ├── theme/
│   │   └── app.dart
│   ├── features/           # Feature-first
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   └── home/
│   ├── core/
│   └── services/
├── test/
├── pubspec.yaml
└── analysis_options.yaml
```

**Key Dependencies:**
```yaml
dependencies:
  go_router: navigation
  flutter_riverpod: state management
  dio: HTTP client
  flutter_secure_storage: secure storage
  local_auth: biometrics
  flutter_form_builder: forms
  json_annotation: serialization
```

### Phase 3: Core Implementation

Build in this order:

1. **Navigation & Routing**
   - Tab bar, stack navigation, auth flow
   - Deep linking support
   - Protected routes (auth guard)

2. **Authentication**
   - Login / Register screens
   - Token management (access + refresh)
   - Biometric auth (fingerprint/Face ID)
   - Secure token storage (Keychain/EncryptedSharedPrefs)
   - Auto-refresh on 401

3. **API Integration**
   - Centralized API client with interceptors
   - Auth token injection in headers
   - Error handling (network, server, validation)
   - Offline queue for failed mutations
   - Request/response logging (dev mode only)

4. **State Management**
   - Server state: TanStack Query (RN) / Riverpod (Flutter)
   - Local state: Zustand (RN) / Riverpod (Flutter)
   - Persistent state: MMKV (RN) / Hive (Flutter)

5. **UI Implementation**
   - Respect platform conventions (iOS vs Android)
   - Thumb zone optimization (primary actions at bottom)
   - Touch targets: min 44pt (iOS) / 48dp (Android)
   - Skeleton loading screens (not spinners)
   - Pull-to-refresh on lists
   - Haptic feedback on important actions
   - Safe area handling (notch, dynamic island)

6. **Offline Support**
   - Cache API responses locally
   - Queue mutations when offline
   - Sync when connectivity returns
   - Show cached data with "offline" indicator

7. **Push Notifications**
   - RN: `expo-notifications` + EAS Push
   - Flutter: `firebase_messaging` + `flutter_local_notifications`
   - Notification handling (foreground, background, killed)
   - Deep link from notification tap

8. **Dark Mode**
   - System theme detection
   - Manual toggle option
   - Theme persistence

### Phase 4: Backend Integration

**Option A — Consuming Existing API:**
If `@backend-specialist` already built the API:
- Read API contracts from `production_artifacts/`
- Implement typed API client matching the contracts
- Handle all error codes documented in the spec

**Option B — Full-Stack Mobile (BaaS):**
If standalone app needing its own backend:
- Firebase: Auth + Firestore + Cloud Functions + FCM + Storage
- Or Supabase: Auth + PostgreSQL + Edge Functions + Realtime + Storage
- Include setup instructions and config files

**Option C — Custom Lightweight API:**
If a simple custom backend is needed:
- Build minimal API in the same `app_build/` (e.g., `app_build/api/`)
- Follow `@backend-specialist` patterns (layered architecture)
- Include `docker-compose.yml` for local development

### Phase 5: Build & Store Publication

#### Google Play Store

**EAS Build (React Native):**
```bash
# eas.json
{
  "build": {
    "production": {
      "android": {
        "buildType": "app-bundle"
      }
    }
  },
  "submit": {
    "production": {
      "android": {
        "serviceAccountKeyPath": "./google-play-key.json",
        "track": "internal"
      }
    }
  }
}

# Build
eas build --platform android --profile production
# Submit
eas submit --platform android
```

**Flutter:**
```bash
# Build AAB
flutter build appbundle --release

# Upload to Play Console:
# Play Console → Production → Create new release → Upload .aab
```

**Play Console Checklist:**
- [ ] App content rating completed
- [ ] Target audience settings
- [ ] Data safety form (privacy declarations)
- [ ] Store listing (title ≤30 chars, short desc ≤80 chars, full desc ≤4000 chars)
- [ ] App icon (512x512 PNG, 32-bit, no alpha)
- [ ] Feature graphic (1024x500)
- [ ] Screenshots: min 2, max 8 per device type
- [ ] Privacy Policy URL
- [ ] Track: Internal → Closed → Open → Production

#### Apple App Store

**EAS Build (React Native):**
```bash
# eas.json
{
  "build": {
    "production": {
      "ios": {
        "distribution": "store",
        "autoIncrement": true
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890"
      }
    }
  }
}

# Build
eas build --platform ios --profile production
# Submit
eas submit --platform ios
```

**Flutter:**
```bash
# Build IPA
flutter build ipa --release

# Upload via Transporter app or:
xcrun altool --upload-app -f build/ios/ipa/App.ipa -t ios -u "email" -p "app-specific-password"
```

**App Store Connect Checklist:**
- [ ] App record created in App Store Connect
- [ ] Bundle ID matches app config
- [ ] Provisioning profiles configured (distribution)
- [ ] App icon (1024x1024 PNG, no alpha, no transparency)
- [ ] Screenshots: 6.7" (iPhone 15 Pro Max), 6.5" (iPhone 11 Pro Max), 5.5" (iPhone 8 Plus)
- [ ] iPad screenshots if universal app
- [ ] App Privacy details completed
- [ ] Review information (demo account credentials if auth required)
- [ ] Age rating
- [ ] Price and availability
- [ ] Track: TestFlight (internal → external) → App Store submission

#### Store Publication Documentation
Generate `production_artifacts/STORE_PUBLICATION_GUIDE.md` with:
- Step-by-step for both stores
- Required assets list with dimensions
- Environment variables and signing key instructions
- Common rejection reasons and how to avoid them
- Timeline expectations (Play: hours-days, App Store: 1-7 days)

### Phase 6: Security Hardening

- [ ] Tokens in Keychain (iOS) / EncryptedSharedPreferences (Android)
- [ ] Certificate pinning for critical endpoints
- [ ] Biometric auth for sensitive operations
- [ ] No secrets in code (use env vars or remote config)
- [ ] ProGuard/R8 code obfuscation (Android release)
- [ ] Jailbreak/root detection (warn or restrict)
- [ ] Deep link domain verification
- [ ] Screenshot prevention for sensitive screens (optional)

### Phase 7: Quality Verification

**Before completing, verify:**
- [ ] App runs on both platforms (or target platform)
- [ ] All screens match specification
- [ ] Navigation flows work correctly
- [ ] Auth flow complete (login, register, logout, token refresh)
- [ ] API integration working (or mocked for demo)
- [ ] Offline behavior handled
- [ ] Dark mode works
- [ ] Responsive on different screen sizes
- [ ] Accessibility: VoiceOver/TalkBack navigable
- [ ] No console warnings/errors
- [ ] Dependencies are complete (no missing packages)
- [ ] Build instructions documented
- [ ] Store publication guide generated

### Output Report
```
📱 MOBILE APP DELIVERY:
- Framework: [chosen framework]
- Platforms: [Android / iOS / Both]
- Screens built: [count]
- API integration: [Frontend-only / Full-stack / BaaS]
- Auth: [method]
- Offline: [Yes/No]
- Push notifications: [Yes/No]
- Store guides: [production_artifacts/STORE_PUBLICATION_GUIDE.md]
- Build command: [command to build and run locally]
- Status: READY FOR TESTING / READY FOR STORE SUBMISSION
```
