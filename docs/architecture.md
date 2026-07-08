# Hostel Meal Intelligence Platform (HMIP)

# Application Structure Specification v1.0

---

# 1. Architecture Principles

The project follows a Domain-Oriented Modular Monolith architecture.

Goals:

* High Cohesion
* Low Coupling
* Clear Business Boundaries
* Easily Extensible
* Framework Independent Business Logic

Business logic must not depend on Django.

---

# 2. High-Level Project Structure

```text
hmip/

│
├── config/                 # Django Project Configuration
│
├── apps/
│   │
│   ├── identity/
│   ├── hostel/
│   ├── meals/
│   ├── attendance/
│   ├── reporting/
│   ├── analytics/
│   ├── rewards/
│   ├── notifications/
│   └── common/
│
├── media/
├── static/
├── scripts/
└── requirements/
```

---

# 3. App Responsibilities

## identity

Responsible For

Authentication

Authorization

Users

Roles

Password Management

Login

Password Reset

Never Responsible For

Students

Hostels

Attendance

Meals

---

## hostel

Responsible For

Hostel

Hostel Settings

Student Management

Mess Staff Management

Meal Types

Hostel Configuration

Never Responsible For

Attendance

Prediction

Analytics

---

## meals

Responsible For

Menu

Meal Declaration

Meal Types Usage

Cutoff Validation

Skip Reasons

Never Responsible For

Attendance

Prediction

Rewards

---

## attendance

Responsible For

Attendance

Attendance Validation

Attendance Window

Attendance Sources

Duplicate Prevention

Never Responsible For

Meal Declaration

Rewards

Prediction

---

## reporting

Responsible For

Daily Reports

Historical Reports

Export

Snapshots

Never Responsible For

Prediction Algorithms

Attendance Entry

---

## analytics

Responsible For

Prediction Statistics

Cost Snapshots

Student Statistics

Prediction Service

Future ML Integration

Never Responsible For

Authentication

Attendance Recording

---

## rewards

Responsible For

Reward Rules

Reward Transactions

Reward Calculation

Leaderboard

---

## notifications

Responsible For

System Notifications

Meal Reminders

Password Notifications

Reward Notifications

---

## common

Responsible For

Shared Constants

Exceptions

Utilities

Base Classes

Shared Validators

No Business Logic

---

# 4. Internal App Structure

Every app follows the same structure.

Example:

```text
attendance/

├── admin.py

├── apps.py

├── urls.py

│
├── api/

│   ├── serializers/

│   ├── views/

│   └── permissions/

│
├── models/

│
├── services/

│
├── selectors/

│
├── validators/

│
├── tasks/

│
├── signals/

│
├── tests/

└── migrations/
```

---

# 5. Layer Responsibilities

## Models

Purpose

Persistence

Relationships

Database Constraints

Nothing Else

---

## Serializers

Purpose

Validate API Input

Convert Objects

No Business Rules

---

## Views

Purpose

Receive Request

Call Service

Return Response

No Business Logic

---

## Services

Purpose

Business Rules

Business Workflows

Transactions

Domain Logic

This is the heart of the application.

---

## Selectors

Purpose

Read Operations

Complex Queries

Dashboard Queries

Statistics Queries

Selectors never modify data.

---

## Validators

Purpose

Business Validation

Example

Attendance Window

Cutoff Time

Duplicate Attendance

---

## Tasks

Purpose

Background Jobs

Examples

Daily Report Generation

Prediction Calculation

Notification Sending

Reward Calculation

---

## Signals

Purpose

Very Small Side Effects

Avoid putting business logic inside signals.

---

# 6. Inter-App Dependency Rules

identity

↓

hostel

↓

meals

↓

attendance

↓

reporting

↓

analytics

↓

rewards

notifications

Common may be used by every app.

Reverse dependencies are prohibited.

Example

attendance must never import reporting.

---

# 7. Business Flow

Hostel Registration

↓

Student Creation

↓

Menu Publication

↓

Meal Declaration

↓

Cutoff

↓

Prediction Generation

↓

Daily Report

↓

Attendance Recording

↓

Analytics Update

↓

Reward Calculation

---

# 8. Domain Services

HostelService

StudentService

MenuService

MealDeclarationService

AttendanceService

ReportService

PredictionService

AnalyticsService

RewardService

NotificationService

---

# 9. Selector Classes

StudentSelector

AttendanceSelector

MealSelector

ReportSelector

AnalyticsSelector

RewardSelector

---

# 10. Validation Classes

AttendanceValidator

MealDeclarationValidator

MenuValidator

RewardValidator

---

# 11. Event Flow

StudentRegistered

↓

MenuPublished

↓

MealDeclarationSubmitted

↓

MealDeclarationUpdated

↓

CutoffReached

↓

PredictionGenerated

↓

DailyReportGenerated

↓

AttendanceMarked

↓

AnalyticsCalculated

↓

RewardCalculated

↓

RewardGranted

---

# 12. Coding Standards

Business logic belongs only in Services.

Queries belong only in Selectors.

Views coordinate.

Models persist.

Validators validate.

---

# 13. Design Rules

No business logic inside Views.

No business logic inside Serializers.

No business logic inside Models.

No direct model access from Views.

Always use Services.

Use Selectors for complex reads.

---

# 14. Scalability

The architecture should support:

1000+ Hostels

100,000+ Students

Future ML Prediction Engine

Future Mobile Applications

Future Public APIs

without restructuring the project.

---

# 15. Core Architecture Principle

Every module must answer one question:

"What business capability am I responsible for?"

If the answer is unclear, the code belongs somewhere else.
