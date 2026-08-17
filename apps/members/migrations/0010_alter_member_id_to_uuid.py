# Migration to alter members.id and all referencing foreign key columns to UUID in PostgreSQL

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20260625_2036'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                -- Drop all foreign key constraints referencing the members table using pg_constraint catalog
                FOR r IN (
                    SELECT conrelid::regclass::text AS table_name, conname AS constraint_name
                    FROM pg_constraint
                    WHERE contype = 'f' AND (confrelid = 'members'::regclass OR conname LIKE '%_fk_members_%')
                ) LOOP
                    EXECUTE 'ALTER TABLE ' || r.table_name || ' DROP CONSTRAINT IF EXISTS ' || quote_ident(r.constraint_name);
                END LOOP;

                -- Alter primary key column members.id to UUID
                ALTER TABLE members ALTER COLUMN id DROP DEFAULT;
                ALTER TABLE members 
                ALTER COLUMN id TYPE uuid USING (
                    CASE 
                        WHEN id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' 
                        THEN id::text::uuid 
                        ELSE gen_random_uuid() 
                    END
                );

                -- Alter all FK columns pointing to members.id across all tables
                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_directorate' AND column_name='director_id') THEN
                    ALTER TABLE departments_directorate ALTER COLUMN director_id TYPE uuid USING (
                        CASE WHEN director_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN director_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_department' AND column_name='hod_id') THEN
                    ALTER TABLE departments_department ALTER COLUMN hod_id TYPE uuid USING (
                        CASE WHEN hod_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN hod_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_department' AND column_name='assistant_hod_id') THEN
                    ALTER TABLE departments_department ALTER COLUMN assistant_hod_id TYPE uuid USING (
                        CASE WHEN assistant_hod_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN assistant_hod_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_unit' AND column_name='unit_head_id') THEN
                    ALTER TABLE departments_unit ALTER COLUMN unit_head_id TYPE uuid USING (
                        CASE WHEN unit_head_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN unit_head_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_departmentmembership' AND column_name='member_id') THEN
                    ALTER TABLE departments_departmentmembership ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_unitmembership' AND column_name='member_id') THEN
                    ALTER TABLE departments_unitmembership ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='connect_groups_connectgroupmember' AND column_name='member_id') THEN
                    ALTER TABLE connect_groups_connectgroupmember ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='events_eventparticipation' AND column_name='member_id') THEN
                    ALTER TABLE events_eventparticipation ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='growth_track_growthtrackenrollment' AND column_name='member_id') THEN
                    ALTER TABLE growth_track_growthtrackenrollment ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='members_firsttimers' AND column_name='member_id') THEN
                    ALTER TABLE members_firsttimers ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='attendance' AND column_name='member_id') THEN
                    ALTER TABLE attendance ALTER COLUMN member_id TYPE uuid USING (
                        CASE WHEN member_id::text ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN member_id::text::uuid ELSE NULL END
                    );
                END IF;

                -- Re-create Foreign Keys referencing members(id)
                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_directorate' AND column_name='director_id') THEN
                    ALTER TABLE departments_directorate 
                    ADD CONSTRAINT departments_directorate_director_id_fk_members_id 
                    FOREIGN KEY (director_id) REFERENCES members(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_department' AND column_name='hod_id') THEN
                    ALTER TABLE departments_department 
                    ADD CONSTRAINT departments_department_hod_id_fk_members_id 
                    FOREIGN KEY (hod_id) REFERENCES members(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_department' AND column_name='assistant_hod_id') THEN
                    ALTER TABLE departments_department 
                    ADD CONSTRAINT departments_department_assistant_hod_id_fk_members_id 
                    FOREIGN KEY (assistant_hod_id) REFERENCES members(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_unit' AND column_name='unit_head_id') THEN
                    ALTER TABLE departments_unit 
                    ADD CONSTRAINT departments_unit_unit_head_id_fk_members_id 
                    FOREIGN KEY (unit_head_id) REFERENCES members(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_departmentmembership' AND column_name='member_id') THEN
                    ALTER TABLE departments_departmentmembership 
                    ADD CONSTRAINT departments_departmentmembership_member_id_fk_members_id 
                    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments_unitmembership' AND column_name='member_id') THEN
                    ALTER TABLE departments_unitmembership 
                    ADD CONSTRAINT departments_unitmembership_member_id_fk_members_id 
                    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='connect_groups_connectgroupmember' AND column_name='member_id') THEN
                    ALTER TABLE connect_groups_connectgroupmember 
                    ADD CONSTRAINT connect_groups_connectgroupmember_member_id_fk_members_id 
                    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='events_eventparticipation' AND column_name='member_id') THEN
                    ALTER TABLE events_eventparticipation 
                    ADD CONSTRAINT events_eventparticipation_member_id_fk_members_id 
                    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='growth_track_growthtrackenrollment' AND column_name='member_id') THEN
                    ALTER TABLE growth_track_growthtrackenrollment 
                    ADD CONSTRAINT growth_track_growthtrackenrollment_member_id_fk_members_id 
                    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='members_firsttimers' AND column_name='member_id') THEN
                    ALTER TABLE members_firsttimers 
                    ADD CONSTRAINT members_firsttimers_member_id_fk_members_id 
                    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
                END IF;
            END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]

