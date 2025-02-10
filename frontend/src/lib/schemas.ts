
import { z } from "zod";

export const submissionSchema = z.object({
    start: z.date(),
    end: z.date(),
    curriculum_ref: z.string(),
    total_costs: z.number(),
    transportation_costs: z.number(),
    parental_info: z.string(),
    teachers: z.array(z.string()),
    students: z.array(z.string()),
    address: z.object({
        street: z.string(),
        city: z.string(),
        country: z.string(),
        state: z.string(),
        zip: z.string()
    })
});

export type SubmissionSchema = typeof submissionSchema;
