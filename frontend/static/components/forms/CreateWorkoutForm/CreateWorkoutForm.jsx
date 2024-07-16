import React from "react";
import { BaseInput } from "../../inputs/BaseInput";
import { BaseButton } from "../../buttons/BaseButton";
import { makeRequest } from "../../../utils/requests";
import { BaseTextArea } from "../../inputs/BaseTextArea/BaseTextArea";
import { useForm, useFieldArray } from 'react-hook-form';

import "./CreateWorkoutForm.css";
import { TemplateContext } from "../../providers/TemplateContextProvider";
import { BaseSelectInput } from "../../selects/BaseSelectInput/BaseSelectInput";


export function CreateWorkoutForm({ createWorkoutEndpoint }) {
    const context = React.useContext(TemplateContext);
    const { 
        register, 
        control, 
        handleSubmit, 
        setError,
        clearErrors,
        formState: { errors } 
    } = useForm({
        defaultValues: {
            name: '',
            description: '',
            exercises: []
        }
    });

    const { 
        fields, 
        append, 
        remove,
    } = useFieldArray({
        control,
        name: "exercises",
        shouldUnregister: true, // Make sure to unregister fields on remove
        excludeKeys: ['id']
    });


    const addExercise = () => {
        append({
            // id: Date.now(),
            exercise_id: '',
            sets: 0,
            repetitions: 0
        });
    };

    const onSubmit = async (data) => {
        clearErrors();
        const { exercises, ...rest } = data;
        const sanitizedExercises = exercises.map(({ id, ...exercise }) => exercise);

        const sanitizedData = {
            ...rest,
            exercises: sanitizedExercises,
        };

        await makeRequest({
            url: createWorkoutEndpoint,
            method: 'POST',
            body: sanitizedData,
            onSuccess: (response) => {
            },
            onError: (response) => {
                Object.keys(response.errors).forEach(key => {
                    setError(key, {
                        type: "server",
                        message: response.errors[key][0]  // Assuming each field errors are in arrays
                    });
                });
            },
        });
    };

    return (
        <form 
            className="create-workout-form" 
            onSubmit={handleSubmit(onSubmit)}
        >
            <BaseInput
                label="Nome"
                name="name"
                type="text"
                placeholder="Nome"
                required={true}
                register={register}
                errorMessage={errors.name && errors.name.message}
            />
            <BaseTextArea
                label="Descrição"
                name="description"
                type="text"
                placeholder="Descrição"
                register={register}
            />
            <BaseButton
                type="button"
                classes={['btn-secondary']}
                text="+ Exercicio"
                onClick={addExercise}
            />
            {fields.map((exercise, index) => (
                <div key={exercise.id}>
                    <BaseSelectInput
                        label="Exercício"
                        options={context.selectOptions.exercises}
                        name={`exercises[${index}].exercise_id`}
                        register={register}
                    />
                    <BaseInput
                        label="Séries"
                        name={`exercises[${index}].sets`}
                        type="number"
                        required={true}
                        register={register}
                    />
                    <BaseInput
                        label="Repetições"
                        name={`exercises[${index}].repetitions`}
                        type="number"
                        required={true}
                        register={register}
                    />
                    <BaseInput
                        label="Pesos (Kg)"
                        name={`exercises[${index}].weight_in_kg`}
                        type="number"
                        required={true}
                        register={register}
                    />
                </div>
            ))}
            <BaseButton
                type="submit"
                classes={['btn-primary', 'btn-blue']}
                text="Criar Treino"
                onClick={() => console.log(errors)}
            />
        </form>
    );
}