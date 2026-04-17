# iOS Platform Guide

Specifics that matter when shipping to the App Store. Not exhaustive -- a
working reference for the Squad.

---

## 1. Modern iOS Stack (2024-2025)

- **UI**: SwiftUI for greenfield; UIKit for fine-grained control or legacy screens
- **State**: `@Observable` macro (iOS 17+), or `ObservableObject` for older
- **Concurrency**: async/await + structured concurrency + actors
- **Data**: SwiftData (iOS 17+) for new, Core Data for legacy, GRDB for raw SQL
- **Networking**: URLSession with async; Alamofire if advanced features needed
- **DI**: composition root pattern; Resolver or Factory for larger apps
- **Testing**: XCTest + Swift Testing framework (Swift 6)

---

## 2. Minimum OS Support

Apple typically expects app devs to support current-1 or current-2. As of
early 2026, target iOS 17+ unless product calls for iOS 16.

Check market share per region before choosing minimum -- emerging markets often
hold older versions longer.

---

## 3. Info.plist Essentials

Every permission you request needs a usage description. App will CRASH at runtime
if the string is missing.

```xml
<key>NSCameraUsageDescription</key>
<string>We use the camera to let you upload photos to your profile.</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>We need access to attach photos to your posts.</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>We use your location to show nearby venues.</string>

<key>NSFaceIDUsageDescription</key>
<string>Face ID protects your account without needing a password.</string>

<key>NSMicrophoneUsageDescription</key>
<string>Recording voice notes requires microphone access.</string>
```

**Rule**: Be specific. "We need this for app functionality" gets rejected.

---

## 4. Privacy Manifest (PrivacyInfo.xcprivacy)

Required since iOS 17 for apps + SDKs. Declare:

- API categories used (`FileTimestamp`, `UserDefaults`, `SystemBootTime`, `DiskSpace`)
- Tracking domains (if any)
- Data collection types (contact info, identifiers, usage data)
- Whether each is linked to user identity
- Whether each is used for tracking

Tool: Xcode scanner + manual review. Missing manifest = App Store rejection.

---

## 5. Signing & Provisioning

| Artifact | Purpose |
|---|---|
| Team ID | Identifies your Apple Developer org |
| App ID | `com.yourorg.yourapp` -- must match bundle ID |
| Provisioning Profile | Ties Team + App ID + signing cert + devices (dev) or distribution |
| Signing Certificate | Distribution for release, Development for local |

**Automatic signing** (Xcode managed) is fine for small teams; **manual + fastlane match** scales better.

---

## 6. TestFlight + App Store Release

1. Archive in Xcode (Product → Archive) or `xcodebuild archive`
2. Upload to App Store Connect
3. TestFlight: internal group (up to 100 testers, no review) → external (up to 10000, light review)
4. Submit for App Store review (1-3 days typical)
5. Release manually or auto after approval
6. Phased release: 7-day gradual rollout supported

Common rejection reasons:
- Missing permission usage strings
- Placeholder content / broken links
- Subscription without required legal text (Terms, auto-renew disclosure)
- Login required but no demo account provided
- Using private APIs

---

## 7. In-App Purchase (StoreKit 2)

- StoreKit 2 is async/await native, much cleaner than StoreKit 1
- Server-side receipt validation via App Store Server API (JWS signed)
- Handle refunds via `Transaction.updates` stream
- Offer codes + promotional offers supported

Legal requirements:
- Restore Purchases button
- Privacy + Terms accessible before purchase
- Auto-renew disclosures visible near the CTA
- Subscription management links to App Store settings

---

## 8. Push Notifications (APNs)

- Use `.p8` auth key (new) instead of `.p12` certs -- doesn't expire, simpler
- `aps-environment` entitlement: development or production
- Rich notifications: Notification Service Extension
- Critical alerts: require special entitlement, Apple approval
- Background refresh for silent pushes: `content-available: 1`, `NSBackgroundModes: remote-notification`

Test with APNs tools like Houston, ApnsTool, or simple `apn` CLI.

---

## 9. Deep Links & Universal Links

- URL schemes (`myapp://`) are legacy; prefer Universal Links
- Universal Links: Associated Domain + `apple-app-site-association` JSON at root of your domain
- Test with `xcrun simctl openurl booted https://yourdomain.com/path`
- Deferred deep links via AppsFlyer / Branch / Adjust for install attribution

---

## 10. Background Execution

| Mode | Use |
|---|---|
| `fetch` | Periodic background refresh |
| `remote-notification` | Silent push to update |
| `audio` | Audio playback |
| `location` | Continuous location |
| `processing` | BGProcessingTask for heavy work |
| `bluetooth-central` | BLE while backgrounded |

iOS is aggressive about killing background apps. Don't rely on background work
for critical paths -- use push + server sync.

---

## 11. Security

### Keychain for secrets

```swift
let query: [String: Any] = [
  kSecClass as String: kSecClassGenericPassword,
  kSecAttrService as String: "com.yourorg.app",
  kSecAttrAccount as String: "refreshToken",
  kSecValueData as String: tokenData,
  kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
]
SecItemAdd(query as CFDictionary, nil)
```

### Biometric gate

```swift
let context = LAContext()
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics,
                      localizedReason: "Unlock your account") { success, error in
  // ...
}
```

### App Transport Security (ATS)

Default: TLS 1.2+, no arbitrary HTTP. Exceptions require justification in App
Review.

---

## 12. Performance Targets

- Cold launch < 2s to first meaningful content
- 60fps scrolling (ideally 120fps on ProMotion devices)
- < 50MB memory idle
- Battery: avoid continuous location, high-frequency timers, wake locks

Use Instruments profiler:
- Time Profiler for CPU
- Allocations for memory
- Energy Log for battery
- Network for bandwidth

---

## 13. Accessibility

- VoiceOver labels via `.accessibilityLabel`, hints via `.accessibilityHint`
- Dynamic Type: use `.font(.body)` instead of fixed sizes
- Color contrast 4.5:1 minimum for text
- Switch Control + Voice Control testing at least once

Apple's Accessibility Inspector (Xcode → Open Developer Tool) catches most issues.

---

## 14. Rejection Prevention

Before submitting:
- [ ] Every permission has a clear, specific usage string
- [ ] Privacy manifest present and accurate
- [ ] No private APIs (`_` prefix method calls)
- [ ] No placeholder text / lorem ipsum
- [ ] Demo account provided if login required
- [ ] Subscription disclosures present
- [ ] Privacy policy + Terms URLs valid
- [ ] All links in the app work (no 404)
- [ ] App doesn't crash on cold launch, dark mode, iPad (if supported)
