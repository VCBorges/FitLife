import React from "react";

/**
 * @param {{
 *    workouts: [{
 *      id: string,
 *      name: string,
 *      description: string
 *      created_by: string
 *      created_at: string
 *   }]
 *  }} 
 * @returns 
 */
export function WorkoutsTable({ workouts }) {

    const onClickRow = async (workoutId) => {
        console.log(workoutId);
    }

    return (
        <table className="table table-dark table-hover">
            <thead>
                <tr>
                    <th></th>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Exercícios</th>
                    <th>Criador</th>
                    <th>Criado em</th>
                </tr>
            </thead>
            <tbody>
                {workouts?.map((workout, index) => (
                    <tr 
                        key={workout.id} 
                        onClick={() => onClickRow(workout.id)}
                    >
                        <td>{index + 1}</td>
                        <td>{workout.name}</td>
                        <td>{workout.description}</td>
                        <td>{workout.exercises_count}</td>
                        <td>{workout.created_by}</td>
                        <td>{workout.created_at}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}