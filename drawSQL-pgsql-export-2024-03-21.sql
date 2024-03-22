CREATE TABLE "workouts"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "workouts" ADD PRIMARY KEY("id");
CREATE TABLE "workout_history"(
    "id" BIGINT NOT NULL,
    "workout_id" BIGINT NOT NULL
);
ALTER TABLE
    "workout_history" ADD PRIMARY KEY("id");
CREATE TABLE "users"(
    "id" BIGINT NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "birth_date" DATE NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "document" VARCHAR(255) NOT NULL,
    "date_joined" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "is_staff" BOOLEAN NOT NULL,
    "zip_code" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL,
    "state" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
CREATE TABLE "exercise_equipment"(
    "id" BIGINT NOT NULL,
    "exercise_id" BIGINT NOT NULL
);
ALTER TABLE
    "exercise_equipment" ADD PRIMARY KEY("id");
CREATE TABLE "exercises"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "equipment_id" BIGINT NOT NULL,
    "description" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "exercises" ADD PRIMARY KEY("id");
CREATE TABLE "muscle_group"(
    "id" BIGINT NOT NULL,
    "name" BIGINT NOT NULL
);
ALTER TABLE
    "muscle_group" ADD PRIMARY KEY("id");
CREATE TABLE "workout_history_exercise"(
    "id" BIGINT NOT NULL,
    "workout_history_id" BIGINT NOT NULL,
    "exercise_id" BIGINT NOT NULL,
    "repetitions" BIGINT NOT NULL,
    "sets" BIGINT NOT NULL,
    "rest_period_in_minutes" BIGINT NOT NULL
);
ALTER TABLE
    "workout_history_exercise" ADD PRIMARY KEY("id");
CREATE TABLE "equipment"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "description" BIGINT NOT NULL
);
ALTER TABLE
    "equipment" ADD PRIMARY KEY("id");
CREATE TABLE "exercise_muscle_group"(
    "id" BIGINT NOT NULL,
    "muscle_group_id" BIGINT NOT NULL,
    "exercise_id" BIGINT NOT NULL
);
ALTER TABLE
    "exercise_muscle_group" ADD PRIMARY KEY("id");
CREATE TABLE "workout_exercise"(
    "id" BIGINT NOT NULL,
    "workout_id" BIGINT NOT NULL,
    "exercise_id" BIGINT NOT NULL,
    "repetitions" BIGINT NOT NULL,
    "sets" BIGINT NOT NULL,
    "rest_period_in_minutes" BIGINT NOT NULL
);
ALTER TABLE
    "workout_exercise" ADD PRIMARY KEY("id");
ALTER TABLE
    "workout_exercise" ADD CONSTRAINT "workout_exercise_workout_id_foreign" FOREIGN KEY("workout_id") REFERENCES "workouts"("id");
ALTER TABLE
    "exercise_muscle_group" ADD CONSTRAINT "exercise_muscle_group_muscle_group_id_foreign" FOREIGN KEY("muscle_group_id") REFERENCES "muscle_group"("id");
ALTER TABLE
    "workout_history" ADD CONSTRAINT "workout_history_workout_id_foreign" FOREIGN KEY("workout_id") REFERENCES "workouts"("id");
ALTER TABLE
    "workouts" ADD CONSTRAINT "workouts_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "workout_exercise" ADD CONSTRAINT "workout_exercise_exercise_id_foreign" FOREIGN KEY("exercise_id") REFERENCES "exercises"("id");
ALTER TABLE
    "exercises" ADD CONSTRAINT "exercises_equipment_id_foreign" FOREIGN KEY("equipment_id") REFERENCES "equipment"("id");
ALTER TABLE
    "muscle_group" ADD CONSTRAINT "muscle_group_id_foreign" FOREIGN KEY("id") REFERENCES "exercises"("id");
ALTER TABLE
    "exercise_equipment" ADD CONSTRAINT "exercise_equipment_exercise_id_foreign" FOREIGN KEY("exercise_id") REFERENCES "exercises"("id");
ALTER TABLE
    "workout_history_exercise" ADD CONSTRAINT "workout_history_exercise_workout_history_id_foreign" FOREIGN KEY("workout_history_id") REFERENCES "workout_history"("id");
ALTER TABLE
    "exercise_muscle_group" ADD CONSTRAINT "exercise_muscle_group_exercise_id_foreign" FOREIGN KEY("exercise_id") REFERENCES "exercises"("id");
ALTER TABLE
    "workout_history_exercise" ADD CONSTRAINT "workout_history_exercise_exercise_id_foreign" FOREIGN KEY("exercise_id") REFERENCES "exercises"("id");