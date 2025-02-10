
import type { PageServerLoad, Actions } from "./$types.js";
import { superValidate } from "sveltekit-superforms";
import { submissionSchema } from "$lib/schemas";
import { zod } from "sveltekit-superforms/adapters";

import { fail } from "@sveltejs/kit";

export const load: PageServerLoad = async () => {
    return {
        form: await superValidate(zod(submissionSchema)),
    };
};

export const actions: Actions = {
    default: async (event) => {
        const form = await superValidate(event, zod(submissionSchema));
        if (!form.valid) {
            return fail(400, {
                form,
            });
        }

        const cookieHeader = event.request.headers.get('cookie');

        const response = await fetch("https://localhost:8002/events", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(cookieHeader ? { Cookie: cookieHeader } : {}), // Include cookies if available
            },
            body: JSON.stringify(form.data),
            credentials: "include", // Ensures cookies are sent with the request
        });

        return {
            form,
        };
    },
};

