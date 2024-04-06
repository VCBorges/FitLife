import React from "react";
import { BaseInput } from "../../inputs/BaseInput";
import { BaseButton } from "../../buttons/BaseButton";
import { makeRequest } from "../../../utils/requests";
import { useAtom } from "jotai";
import { BaseTextArea } from "../../inputs/BaseTextArea/BaseTextArea";
import { atom } from "jotai";
import { CreateWorkoutExerciseFormSection } from "../CreateWorkoutExerciseFormSection/CreateWorkoutExerciseFormSection";
import { 
    createFormStateAtom, 
    createFormStateKey,
    handleFormErrors, 
    handleFormInputChange 
} from "../../../utils/atoms";

import "./CreateWorkoutForm.css";


const createWorkoutFormAtom = atom({
    name: createFormStateKey(),
    description: createFormStateKey(),
    __all__: createFormStateKey(),
    exercises: [],
});

export function CreateWorkoutForm({ createWorkoutEndpoint }) {
    const [createWorkoutState, setCreateWorkoutState] = useAtom(createWorkoutFormAtom);

    const handleChange = (e) => {
        handleFormInputChange({
            event: e,
            setStateAction: setCreateWorkoutState,
        });
    };

    const addExercise = () => {
        setCreateWorkoutState((prevState) => ({
            ...prevState,
            exercises: [
                ...prevState.exercises,
                { 
                    id: Date.now(), 
                    exercise_id: '', 
                    sets: 0,
                    repetitions: 0
                },
            ],
        }));
    };

    const handleExerciseChange = (id, e) => {
        const { name, value } = e.target;
        setCreateWorkoutState((prevState) => ({
          ...prevState,
          exercises: prevState.exercises.map((exercise) =>
            exercise.id === id ? { ...exercise, [name]: value } : exercise
          ),
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();

        await makeRequest({
            url: createWorkoutEndpoint,
            method: 'POST',
            body: {
                name: createWorkoutState.name.value,
                description: createWorkoutState.description.value,
                exercises: createWorkoutState.exercises,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            onSuccess: (data) => {
                // window.location.href = data.redirect_url;
            },
            onError: (data) => {
                const errors = data.errors;
                handleFormErrors({
                    errors: errors,
                    setStateAction: setCreateWorkoutState,
                });
            },
        });
    };

    return (
        <form className="create-workout-form" onSubmit={handleSubmit}>
            <BaseInput
                label="Nome"
                name="name"
                type="text"
                value={createWorkoutState.name.value}
                onChange={handleChange}
                placeholder="Nome"
                errorMessage={createWorkoutState.name.error}
                required={true}
            />
            <BaseTextArea
                label="Descrição"
                name="description"
                type="text"
                value={createWorkoutState.description.value}
                onChange={handleChange}
                placeholder="Descrição"
                errorMessage={createWorkoutState.description.error}
            />
            <BaseButton
                type="button"
                classes={['btn-secondary']}
                text="+ Exercicio"
                onClick={addExercise}
            />
            {createWorkoutState.exercises.map((exercise, index) => (
                <CreateWorkoutExerciseFormSection
                    key={exercise.id}
                    exercise={exercise}
                    index={index}
                    onExerciseChange={handleExerciseChange}
                />
            ))}
            <BaseButton
                type="submit"
                classes={['btn-primary', 'btn-blue']}
                text="Criar Treino"
            />
        </form>
    );
}