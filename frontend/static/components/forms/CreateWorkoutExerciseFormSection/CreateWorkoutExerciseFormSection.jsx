import React from "react";
import { BaseInput } from "../../inputs/BaseInput";
import { BaseSelectInput } from "../../selects/BaseSelectInput/BaseSelectInput";
import { TemplateContext } from "../../providers/TemplateContextProvider";

/**
 *  @param {{
 *      exercise: string,
 *      index: int,
 *      onExerciseChange: function
 *  }}
 * @returns  
 */
export function CreateWorkoutExerciseFormSection({
    exercise,
    index,
    onExerciseChange,
}){
    const context = React.useContext(TemplateContext);
    return (
        <div key={exercise.id}>
            <BaseSelectInput
                label="Exercicio"
                options={context.selectOptions.exercises} 
                onChange={e => onExerciseChange(exercise.id, e)}
            />
            <BaseInput
                label="Sets"
                name="sets"
                type="number"
                value={exercise.sets}
                onChange={e => onExerciseChange(exercise.id, e)}
                placeholder={`Exercise #${index + 1} Sets`}
            />
            <BaseInput
                label="Repetitions"
                name="repetitions"
                type="number"
                value={exercise.repetitions} // Fixed: changed from exercise.sets to exercise.repetitions
                onChange={e => onExerciseChange(exercise.id, e)}
                placeholder={`Exercise #${index + 1} Repetitions`}
            />
        </div>
    );
}