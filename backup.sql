--
-- PostgreSQL database dump
--

\restrict PEQeSaC71AHI5mX7jOo9w8rATUbkLxN7PqmxqLUgVUGPkCrH1JkSszQ6pVKgdAh

-- Dumped from database version 17.12 (Debian 17.12-1.pgdg13+1)
-- Dumped by pg_dump version 17.12 (Debian 17.12-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.ventas DROP CONSTRAINT IF EXISTS "ventas_ID_metodos_fd57bd27_fk_metodos_pago_ID_metodos";
ALTER TABLE IF EXISTS ONLY public.usuarios_x_roles DROP CONSTRAINT IF EXISTS "usuarios_x_roles_ID_usuarios_a0fd5f7b_fk_usuarios_ID_usuarios";
ALTER TABLE IF EXISTS ONLY public.usuarios_x_roles DROP CONSTRAINT IF EXISTS "usuarios_x_roles_ID_roles_b66222d0_fk_roles_ID_roles";
ALTER TABLE IF EXISTS ONLY public.usuarios_user_permissions DROP CONSTRAINT IF EXISTS usuarios_user_permis_usuario_id_232fd58d_fk_usuarios_;
ALTER TABLE IF EXISTS ONLY public.usuarios_user_permissions DROP CONSTRAINT IF EXISTS usuarios_user_permis_permission_id_af615ca1_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.usuarios_groups DROP CONSTRAINT IF EXISTS "usuarios_groups_usuario_id_1132ca50_fk_usuarios_ID_usuarios";
ALTER TABLE IF EXISTS ONLY public.usuarios_groups DROP CONSTRAINT IF EXISTS usuarios_groups_group_id_18c61092_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.proveedores_x_insumos DROP CONSTRAINT IF EXISTS "proveedores_x_insumos_ID_insumos_60721ae4_fk_insumos_ID_insumos";
ALTER TABLE IF EXISTS ONLY public.proveedores_x_insumos DROP CONSTRAINT IF EXISTS "proveedores_x_insumo_ID_proveedores_dda42c15_fk_proveedor";
ALTER TABLE IF EXISTS ONLY public.productos_x_insumos DROP CONSTRAINT IF EXISTS "productos_x_insumos_ID_productos_f6ea820a_fk_productos";
ALTER TABLE IF EXISTS ONLY public.productos_x_insumos DROP CONSTRAINT IF EXISTS "productos_x_insumos_ID_insumos_e300d21f_fk_insumos_ID_insumos";
ALTER TABLE IF EXISTS ONLY public.pedidos DROP CONSTRAINT IF EXISTS "pedidos_ID_empleados_dc487bb8_fk_empleados_ID_empleados";
ALTER TABLE IF EXISTS ONLY public.movimientos_caja DROP CONSTRAINT IF EXISTS "movimientos_caja_ID_ventas_3a75543f_fk_ventas_ID_ventas";
ALTER TABLE IF EXISTS ONLY public.movimientos_caja DROP CONSTRAINT IF EXISTS "movimientos_caja_ID_metodos_c59a5ebf_fk_metodos_pago_ID_metodos";
ALTER TABLE IF EXISTS ONLY public.movimientos_caja DROP CONSTRAINT IF EXISTS "movimientos_caja_ID_compras_d2b0b618_fk_compras_ID_compras";
ALTER TABLE IF EXISTS ONLY public.movimientos_caja DROP CONSTRAINT IF EXISTS "movimientos_caja_ID_cajas_5a6a50a2_fk_cajas_ID_cajas";
ALTER TABLE IF EXISTS ONLY public.insumos DROP CONSTRAINT IF EXISTS "insumos_ID_categorias_a8603f21_fk_categorias_ID_categorias";
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS "empleados_ID_usuarios_bfd72eb0_fk_usuarios_ID_usuarios";
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS "empleados_ID_locales_6a406bf7_fk_locales_ID_locales";
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.detalles_ventas DROP CONSTRAINT IF EXISTS "detalles_ventas_ID_ventas_6b1d9400_fk_ventas_ID_ventas";
ALTER TABLE IF EXISTS ONLY public.detalles_ventas DROP CONSTRAINT IF EXISTS "detalles_ventas_ID_productos_9f2b2ef2_fk_productos_ID_productos";
ALTER TABLE IF EXISTS ONLY public.detalles_ventas DROP CONSTRAINT IF EXISTS "detalles_ventas_ID_menus_73928115_fk_menus_ID_menus";
ALTER TABLE IF EXISTS ONLY public.detalles_ventas DROP CONSTRAINT IF EXISTS "detalles_ventas_ID_bebidas_8913caee_fk_bebidas_ID_bebidas";
ALTER TABLE IF EXISTS ONLY public.detalles_pedidos DROP CONSTRAINT IF EXISTS "detalles_pedidos_ID_productos_0f6135e9_fk_productos";
ALTER TABLE IF EXISTS ONLY public.detalles_pedidos DROP CONSTRAINT IF EXISTS "detalles_pedidos_ID_pedidos_4b484066_fk_pedidos_ID_pedidos";
ALTER TABLE IF EXISTS ONLY public.detalles_pedidos DROP CONSTRAINT IF EXISTS "detalles_pedidos_ID_menus_346aa29f_fk_menus_ID_menus";
ALTER TABLE IF EXISTS ONLY public.detalles_pedidos DROP CONSTRAINT IF EXISTS "detalles_pedidos_ID_bebidas_455c7b3a_fk_bebidas_ID_bebidas";
ALTER TABLE IF EXISTS ONLY public.detalles_menus DROP CONSTRAINT IF EXISTS "detalles_menus_ID_productos_916ea542_fk_productos_ID_productos";
ALTER TABLE IF EXISTS ONLY public.detalles_menus DROP CONSTRAINT IF EXISTS "detalles_menus_ID_menus_bef9c4b8_fk_menus_ID_menus";
ALTER TABLE IF EXISTS ONLY public.detalles_menus DROP CONSTRAINT IF EXISTS "detalles_menus_ID_bebidas_e3eb27d2_fk_bebidas_ID_bebidas";
ALTER TABLE IF EXISTS ONLY public.detalles_compras DROP CONSTRAINT IF EXISTS "detalles_compras_ID_insumos_51e60a73_fk_insumos_ID_insumos";
ALTER TABLE IF EXISTS ONLY public.detalles_compras DROP CONSTRAINT IF EXISTS "detalles_compras_ID_compras_55a183e8_fk_compras_ID_compras";
ALTER TABLE IF EXISTS ONLY public.detalles_compras DROP CONSTRAINT IF EXISTS "detalles_compras_ID_bebidas_ff1996e1_fk_bebidas_ID_bebidas";
ALTER TABLE IF EXISTS ONLY public.compras DROP CONSTRAINT IF EXISTS "compras_ID_proveedores_9cd5bc8d_fk_proveedores_ID_proveedores";
ALTER TABLE IF EXISTS ONLY public.compras DROP CONSTRAINT IF EXISTS "compras_ID_metodos_9ae1fccd_fk_metodos_pago_ID_metodos";
ALTER TABLE IF EXISTS ONLY public.cajas DROP CONSTRAINT IF EXISTS "cajas_ID_usuarios_50c2a5e6_fk_usuarios_ID_usuarios";
ALTER TABLE IF EXISTS ONLY public.cajas DROP CONSTRAINT IF EXISTS "cajas_ID_locales_28ef83d6_fk_locales_ID_locales";
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS "authtoken_token_user_id_35299eff_fk_usuarios_ID_usuarios";
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public."ventas_ID_metodos_fd57bd27";
DROP INDEX IF EXISTS public."usuarios_x_roles_ID_usuarios_a0fd5f7b";
DROP INDEX IF EXISTS public."usuarios_x_roles_ID_roles_b66222d0";
DROP INDEX IF EXISTS public.usuarios_user_permissions_usuario_id_232fd58d;
DROP INDEX IF EXISTS public.usuarios_user_permissions_permission_id_af615ca1;
DROP INDEX IF EXISTS public.usuarios_groups_usuario_id_1132ca50;
DROP INDEX IF EXISTS public.usuarios_groups_group_id_18c61092;
DROP INDEX IF EXISTS public."usuarios_Usuario_d070f9f8_like";
DROP INDEX IF EXISTS public."usuarios_Email_ed42e3ee_like";
DROP INDEX IF EXISTS public.unique_caja_abierta_por_local;
DROP INDEX IF EXISTS public."proveedores_x_insumos_ID_proveedores_dda42c15";
DROP INDEX IF EXISTS public."proveedores_x_insumos_ID_insumos_60721ae4";
DROP INDEX IF EXISTS public."productos_x_insumos_ID_productos_f6ea820a";
DROP INDEX IF EXISTS public."productos_x_insumos_ID_insumos_e300d21f";
DROP INDEX IF EXISTS public."pedidos_ID_empleados_dc487bb8";
DROP INDEX IF EXISTS public."movimientos_caja_ID_ventas_3a75543f";
DROP INDEX IF EXISTS public."movimientos_caja_ID_metodos_c59a5ebf";
DROP INDEX IF EXISTS public."movimientos_caja_ID_compras_d2b0b618";
DROP INDEX IF EXISTS public."movimientos_caja_ID_cajas_5a6a50a2";
DROP INDEX IF EXISTS public."insumos_ID_categorias_a8603f21";
DROP INDEX IF EXISTS public."empleados_ID_locales_6a406bf7";
DROP INDEX IF EXISTS public."empleados_DNI_f6383a0f_like";
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public."detalles_ventas_ID_menus_73928115";
DROP INDEX IF EXISTS public."detalles_ventas_ID_bebidas_8913caee";
DROP INDEX IF EXISTS public."detalles_ventas_ID_Ventas_23ed946a";
DROP INDEX IF EXISTS public."detalles_ventas_ID_Producto_87aa0904";
DROP INDEX IF EXISTS public."detalles_pedidos_ID_productos_0f6135e9";
DROP INDEX IF EXISTS public."detalles_pedidos_ID_pedidos_4b484066";
DROP INDEX IF EXISTS public."detalles_pedidos_ID_menus_346aa29f";
DROP INDEX IF EXISTS public."detalles_pedidos_ID_bebidas_455c7b3a";
DROP INDEX IF EXISTS public."detalles_menus_ID_productos_916ea542";
DROP INDEX IF EXISTS public."detalles_menus_ID_menus_bef9c4b8";
DROP INDEX IF EXISTS public."detalles_menus_ID_bebidas_e3eb27d2";
DROP INDEX IF EXISTS public."detalles_compras_ID_insumos_51e60a73";
DROP INDEX IF EXISTS public."detalles_compras_ID_compras_55a183e8";
DROP INDEX IF EXISTS public."detalles_compras_ID_bebidas_ff1996e1";
DROP INDEX IF EXISTS public."compras_ID_proveedores_9cd5bc8d";
DROP INDEX IF EXISTS public."compras_ID_metodos_9ae1fccd";
DROP INDEX IF EXISTS public."cajas_ID_usuarios_50c2a5e6";
DROP INDEX IF EXISTS public."cajas_ID_locales_28ef83d6";
DROP INDEX IF EXISTS public.authtoken_token_key_10f0b77e_like;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.ventas DROP CONSTRAINT IF EXISTS ventas_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios_x_roles DROP CONSTRAINT IF EXISTS usuarios_x_roles_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios_user_permissions DROP CONSTRAINT IF EXISTS usuarios_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios_user_permissions DROP CONSTRAINT IF EXISTS usuarios_user_permission_usuario_id_permission_id_474b33a5_uniq;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS usuarios_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios_groups DROP CONSTRAINT IF EXISTS usuarios_groups_usuario_id_group_id_a66c5ef3_uniq;
ALTER TABLE IF EXISTS ONLY public.usuarios_groups DROP CONSTRAINT IF EXISTS usuarios_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS "usuarios_Usuario_d070f9f8_uniq";
ALTER TABLE IF EXISTS ONLY public.usuarios DROP CONSTRAINT IF EXISTS "usuarios_Email_key";
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_pkey;
ALTER TABLE IF EXISTS ONLY public.proveedores_x_insumos DROP CONSTRAINT IF EXISTS proveedores_x_insumos_pkey;
ALTER TABLE IF EXISTS ONLY public.proveedores DROP CONSTRAINT IF EXISTS proveedores_pkey;
ALTER TABLE IF EXISTS ONLY public.productos_x_insumos DROP CONSTRAINT IF EXISTS productos_x_insumos_pkey;
ALTER TABLE IF EXISTS ONLY public.productos DROP CONSTRAINT IF EXISTS productos_pkey;
ALTER TABLE IF EXISTS ONLY public.pedidos DROP CONSTRAINT IF EXISTS pedidos_pkey;
ALTER TABLE IF EXISTS ONLY public.movimientos_caja DROP CONSTRAINT IF EXISTS movimientos_caja_pkey;
ALTER TABLE IF EXISTS ONLY public.metodos_pago DROP CONSTRAINT IF EXISTS metodos_pago_pkey;
ALTER TABLE IF EXISTS ONLY public.menus DROP CONSTRAINT IF EXISTS menus_pkey;
ALTER TABLE IF EXISTS ONLY public.locales DROP CONSTRAINT IF EXISTS locales_pkey;
ALTER TABLE IF EXISTS ONLY public.insumos DROP CONSTRAINT IF EXISTS insumos_pkey;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS empleados_pkey;
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS "empleados_ID_usuarios_key";
ALTER TABLE IF EXISTS ONLY public.empleados DROP CONSTRAINT IF EXISTS "empleados_DNI_f6383a0f_uniq";
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.detalles_ventas DROP CONSTRAINT IF EXISTS detalles_ventas_pkey;
ALTER TABLE IF EXISTS ONLY public.detalles_pedidos DROP CONSTRAINT IF EXISTS detalles_pedidos_pkey;
ALTER TABLE IF EXISTS ONLY public.detalles_menus DROP CONSTRAINT IF EXISTS detalles_menus_pkey;
ALTER TABLE IF EXISTS ONLY public.detalles_compras DROP CONSTRAINT IF EXISTS detalles_compras_pkey;
ALTER TABLE IF EXISTS ONLY public.compras DROP CONSTRAINT IF EXISTS compras_pkey;
ALTER TABLE IF EXISTS ONLY public.categorias DROP CONSTRAINT IF EXISTS categorias_pkey;
ALTER TABLE IF EXISTS ONLY public.cajas DROP CONSTRAINT IF EXISTS cajas_pkey;
ALTER TABLE IF EXISTS ONLY public.bebidas DROP CONSTRAINT IF EXISTS bebidas_pkey;
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS authtoken_token_user_id_key;
ALTER TABLE IF EXISTS ONLY public.authtoken_token DROP CONSTRAINT IF EXISTS authtoken_token_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.ventas;
DROP TABLE IF EXISTS public.usuarios_x_roles;
DROP TABLE IF EXISTS public.usuarios_user_permissions;
DROP TABLE IF EXISTS public.usuarios_groups;
DROP TABLE IF EXISTS public.usuarios;
DROP TABLE IF EXISTS public.roles;
DROP TABLE IF EXISTS public.proveedores_x_insumos;
DROP TABLE IF EXISTS public.proveedores;
DROP TABLE IF EXISTS public.productos_x_insumos;
DROP TABLE IF EXISTS public.productos;
DROP TABLE IF EXISTS public.pedidos;
DROP TABLE IF EXISTS public.movimientos_caja;
DROP TABLE IF EXISTS public.metodos_pago;
DROP TABLE IF EXISTS public.menus;
DROP TABLE IF EXISTS public.locales;
DROP TABLE IF EXISTS public.insumos;
DROP TABLE IF EXISTS public.empleados;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.detalles_ventas;
DROP TABLE IF EXISTS public.detalles_pedidos;
DROP TABLE IF EXISTS public.detalles_menus;
DROP TABLE IF EXISTS public.detalles_compras;
DROP TABLE IF EXISTS public.compras;
DROP TABLE IF EXISTS public.categorias;
DROP TABLE IF EXISTS public.cajas;
DROP TABLE IF EXISTS public.bebidas;
DROP TABLE IF EXISTS public.authtoken_token;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
-- *not* dropping schema, since initdb creates it
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: bebidas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bebidas (
    "ID_bebidas" integer NOT NULL,
    "Nombre" character varying(200) NOT NULL,
    "Descripcion" character varying(200),
    "Estado" boolean NOT NULL,
    "Stock_actual" numeric(10,2) NOT NULL,
    "Stock_minimo" integer NOT NULL,
    "Precio_unitario" numeric(10,2) NOT NULL,
    "Unidad" character varying(20) NOT NULL
);


--
-- Name: bebidas_ID_bebidas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.bebidas ALTER COLUMN "ID_bebidas" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."bebidas_ID_bebidas_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cajas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cajas (
    "ID_cajas" integer NOT NULL,
    "Monto_apertura" numeric(9,2) NOT NULL,
    "Monto_cierre" numeric(9,2),
    "Estado" boolean NOT NULL,
    "ID_locales" integer NOT NULL,
    "ID_usuarios" integer NOT NULL,
    "Fecha_hora_apertura" timestamp with time zone NOT NULL,
    "Fecha_hora_cierre" timestamp with time zone,
    "Diferencia_total" numeric(10,2),
    "Digital_esperado" numeric(10,2),
    "Digital_real" numeric(10,2),
    "Efectivo_esperado" numeric(10,2),
    "Efectivo_real" numeric(10,2),
    "Observaciones_cierre" text,
    "Ajuste_apertura" numeric(10,2)
);


--
-- Name: cajas_ID_cajas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cajas ALTER COLUMN "ID_cajas" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."cajas_ID_cajas_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: categorias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categorias (
    "ID_categorias" integer NOT NULL,
    "Nombre" character varying(30) NOT NULL,
    "Descripcion" character varying(200) NOT NULL
);


--
-- Name: categorias_ID_categorias_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.categorias ALTER COLUMN "ID_categorias" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."categorias_ID_categorias_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: compras; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compras (
    "ID_compras" integer NOT NULL,
    "Precio_total" numeric(9,2) NOT NULL,
    "ID_metodos" integer NOT NULL,
    "ID_proveedores" integer,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL
);


--
-- Name: compras_ID_compras_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.compras ALTER COLUMN "ID_compras" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."compras_ID_compras_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: detalles_compras; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.detalles_compras (
    "ID_detalles_compras" integer NOT NULL,
    "Cantidad" integer NOT NULL,
    "Subtotal" numeric(9,2) NOT NULL,
    "ID_compras" integer NOT NULL,
    "ID_insumos" integer,
    "ID_bebidas" integer
);


--
-- Name: detalles_compras_ID_detalles_compras_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.detalles_compras ALTER COLUMN "ID_detalles_compras" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."detalles_compras_ID_detalles_compras_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: detalles_menus; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.detalles_menus (
    "ID_detalles_menus" integer NOT NULL,
    "Cantidad" integer NOT NULL,
    "Descuento" integer NOT NULL,
    "ID_menus" integer NOT NULL,
    "ID_productos" integer,
    "ID_bebidas" integer
);


--
-- Name: detalles_menus_ID_detalles_menus_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.detalles_menus ALTER COLUMN "ID_detalles_menus" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."detalles_menus_ID_detalles_menus_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: detalles_pedidos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.detalles_pedidos (
    "ID_detalles_pedidos" integer NOT NULL,
    "Cantidad" integer NOT NULL,
    "Subtotal" numeric(9,2) NOT NULL,
    "ID_pedidos" integer NOT NULL,
    "ID_productos" integer,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL,
    "ID_bebidas" integer,
    "ID_menus" integer
);


--
-- Name: detalles_pedidos_ID_detalles_pedidos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.detalles_pedidos ALTER COLUMN "ID_detalles_pedidos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."detalles_pedidos_ID_detalles_pedidos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: detalles_ventas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.detalles_ventas (
    "ID_detalles_ventas" integer NOT NULL,
    "Cantidad" integer NOT NULL,
    "Subtotal" numeric(9,2) NOT NULL,
    "ID_productos" integer,
    "ID_ventas" integer NOT NULL,
    "ID_bebidas" integer,
    "ID_menus" integer
);


--
-- Name: detalles_ventas_ID_detalles_ventas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.detalles_ventas ALTER COLUMN "ID_detalles_ventas" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."detalles_ventas_ID_detalles_ventas_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: empleados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.empleados (
    "ID_empleados" integer NOT NULL,
    "DNI" character varying(8) NOT NULL,
    "Nombre" character varying(50) NOT NULL,
    "Apellido" character varying(50) NOT NULL,
    "Telefono" character varying(20) NOT NULL,
    "Domicilio" character varying(200),
    "Estado" boolean NOT NULL,
    "ID_usuarios" integer,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL,
    "ID_locales" integer NOT NULL
);


--
-- Name: empleados_ID_empleados_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.empleados ALTER COLUMN "ID_empleados" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."empleados_ID_empleados_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insumos (
    "ID_insumos" integer NOT NULL,
    "Nombre" character varying(50) NOT NULL,
    "Descripcion" character varying(200),
    "Unidad" character varying(20) NOT NULL,
    "Stock_actual" numeric(10,2) NOT NULL,
    "Stock_minimo" integer NOT NULL,
    "ID_categorias" integer NOT NULL
);


--
-- Name: insumos_ID_insumos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.insumos ALTER COLUMN "ID_insumos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."insumos_ID_insumos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: locales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locales (
    "ID_locales" integer NOT NULL,
    "Nombre" character varying(50) NOT NULL,
    "Direccion" character varying(200) NOT NULL,
    "Telefono" character varying(20),
    "Red_social" character varying(50),
    "Fecha_hora_creacion" timestamp with time zone NOT NULL
);


--
-- Name: locales_ID_locales_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.locales ALTER COLUMN "ID_locales" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."locales_ID_locales_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: menus; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.menus (
    "ID_menus" integer NOT NULL,
    "Nombre" character varying(100) NOT NULL,
    "Estado" boolean NOT NULL,
    "Fecha_hora_fin" timestamp with time zone,
    "Fecha_hora_inicio" timestamp with time zone
);


--
-- Name: menus_ID_menus_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.menus ALTER COLUMN "ID_menus" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."menus_ID_menus_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: metodos_pago; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.metodos_pago (
    "ID_metodos" integer NOT NULL,
    "Nombre" character varying(50) NOT NULL,
    "Descripcion" character varying(200) NOT NULL,
    "Estado" boolean NOT NULL
);


--
-- Name: metodos_pago_ID_metodos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.metodos_pago ALTER COLUMN "ID_metodos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."metodos_pago_ID_metodos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: movimientos_caja; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.movimientos_caja (
    "ID_movimientos" integer NOT NULL,
    "Concepto" character varying(50) NOT NULL,
    "Monto" numeric(9,2) NOT NULL,
    "ID_cajas" integer NOT NULL,
    "ID_compras" integer,
    "ID_ventas" integer,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL,
    "Tipo_movimiento" character varying(10) NOT NULL,
    "ID_metodos" integer
);


--
-- Name: movimientos_caja_ID_movimientos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.movimientos_caja ALTER COLUMN "ID_movimientos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."movimientos_caja_ID_movimientos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pedidos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pedidos (
    "ID_pedidos" integer NOT NULL,
    "Cliente" character varying(50) NOT NULL,
    "Direccion" character varying(200) NOT NULL,
    "Precio_total" numeric(9,2) NOT NULL,
    "Estado" character varying(20) NOT NULL,
    "ID_empleados" integer NOT NULL,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL,
    "Pagado" boolean NOT NULL
);


--
-- Name: pedidos_ID_pedidos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.pedidos ALTER COLUMN "ID_pedidos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."pedidos_ID_pedidos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: productos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.productos (
    "ID_productos" integer NOT NULL,
    "Nombre" character varying(100) NOT NULL,
    "Descripcion" character varying(200) NOT NULL,
    "Precio_unitario" numeric(9,2) NOT NULL,
    "Estado" boolean NOT NULL
);


--
-- Name: productos_ID_productos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.productos ALTER COLUMN "ID_productos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."productos_ID_productos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: productos_x_insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.productos_x_insumos (
    "ID_productos_insumos" integer NOT NULL,
    "ID_insumos" integer NOT NULL,
    "ID_productos" integer NOT NULL,
    "Cantidad" numeric(9,2) NOT NULL
);


--
-- Name: productos_x_insumos_ID_productos_insumos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.productos_x_insumos ALTER COLUMN "ID_productos_insumos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."productos_x_insumos_ID_productos_insumos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: proveedores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.proveedores (
    "ID_proveedores" integer NOT NULL,
    "Nombre" character varying(100) NOT NULL,
    "Direccion" character varying(200),
    "Telefono" character varying(20),
    "Email" character varying(30),
    "CUIT" character varying(30),
    "Descripcion" character varying(200) NOT NULL
);


--
-- Name: proveedores_ID_proveedores_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.proveedores ALTER COLUMN "ID_proveedores" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."proveedores_ID_proveedores_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: proveedores_x_insumos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.proveedores_x_insumos (
    "ID_proveedores_insumos" integer NOT NULL,
    "ID_insumos" integer NOT NULL,
    "ID_proveedores" integer NOT NULL
);


--
-- Name: proveedores_x_insumos_ID_proveedores_insumos_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.proveedores_x_insumos ALTER COLUMN "ID_proveedores_insumos" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."proveedores_x_insumos_ID_proveedores_insumos_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    "ID_roles" integer NOT NULL,
    "Nombre" character varying(50) NOT NULL,
    "Descripcion" character varying(200) NOT NULL,
    "Estado" boolean NOT NULL
);


--
-- Name: roles_ID_roles_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.roles ALTER COLUMN "ID_roles" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."roles_ID_roles_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    "ID_usuarios" integer NOT NULL,
    "Usuario" character varying(30) NOT NULL,
    "Password" character varying(128) NOT NULL,
    "Estado" boolean NOT NULL,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL,
    "Fecha_hora_modificacion" timestamp with time zone,
    "Is_staff" boolean NOT NULL,
    "Is_superuser" boolean NOT NULL,
    "Email" character varying(254)
);


--
-- Name: usuarios_ID_usuarios_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.usuarios ALTER COLUMN "ID_usuarios" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."usuarios_ID_usuarios_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: usuarios_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios_groups (
    id bigint NOT NULL,
    usuario_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: usuarios_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.usuarios_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuarios_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: usuarios_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios_user_permissions (
    id bigint NOT NULL,
    usuario_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: usuarios_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.usuarios_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuarios_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: usuarios_x_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios_x_roles (
    "ID_usuarios_roles" integer NOT NULL,
    "ID_roles" integer NOT NULL,
    "ID_usuarios" integer NOT NULL
);


--
-- Name: usuarios_x_roles_ID_usuarios_roles_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.usuarios_x_roles ALTER COLUMN "ID_usuarios_roles" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."usuarios_x_roles_ID_usuarios_roles_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ventas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ventas (
    "ID_ventas" integer NOT NULL,
    "Precio_total" numeric(9,2) NOT NULL,
    "Fecha_hora_creacion" timestamp with time zone NOT NULL,
    "ID_metodos" integer NOT NULL
);


--
-- Name: ventas_ID_ventas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.ventas ALTER COLUMN "ID_ventas" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public."ventas_ID_ventas_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Categoría	7	add_categoria
26	Can change Categoría	7	change_categoria
27	Can delete Categoría	7	delete_categoria
28	Can view Categoría	7	view_categoria
29	Can add Compra	8	add_compra
30	Can change Compra	8	change_compra
31	Can delete Compra	8	delete_compra
32	Can view Compra	8	view_compra
33	Can add Empleado	9	add_empleado
34	Can change Empleado	9	change_empleado
35	Can delete Empleado	9	delete_empleado
36	Can view Empleado	9	view_empleado
37	Can add Local	10	add_local
38	Can change Local	10	change_local
39	Can delete Local	10	delete_local
40	Can view Local	10	view_local
41	Can add Menú	11	add_menu
42	Can change Menú	11	change_menu
43	Can delete Menú	11	delete_menu
44	Can view Menú	11	view_menu
45	Can add Método de pago	12	add_metodopago
46	Can change Método de pago	12	change_metodopago
47	Can delete Método de pago	12	delete_metodopago
48	Can view Método de pago	12	view_metodopago
49	Can add Producto	13	add_producto
50	Can change Producto	13	change_producto
51	Can delete Producto	13	delete_producto
52	Can view Producto	13	view_producto
53	Can add Proveedor	14	add_proveedor
54	Can change Proveedor	14	change_proveedor
55	Can delete Proveedor	14	delete_proveedor
56	Can view Proveedor	14	view_proveedor
57	Can add Rol	15	add_rol
58	Can change Rol	15	change_rol
59	Can delete Rol	15	delete_rol
60	Can view Rol	15	view_rol
61	Can add Usuario	16	add_usuario
62	Can change Usuario	16	change_usuario
63	Can delete Usuario	16	delete_usuario
64	Can view Usuario	16	view_usuario
65	Can add Insumo	17	add_insumo
66	Can change Insumo	17	change_insumo
67	Can delete Insumo	17	delete_insumo
68	Can view Insumo	17	view_insumo
69	Can add Detalle de compra	18	add_detallecompra
70	Can change Detalle de compra	18	change_detallecompra
71	Can delete Detalle de compra	18	delete_detallecompra
72	Can view Detalle de compra	18	view_detallecompra
73	Can add Caja	19	add_caja
74	Can change Caja	19	change_caja
75	Can delete Caja	19	delete_caja
76	Can view Caja	19	view_caja
77	Can add Pedido	20	add_pedido
78	Can change Pedido	20	change_pedido
79	Can delete Pedido	20	delete_pedido
80	Can view Pedido	20	view_pedido
81	Can add Detalle de pedido	21	add_detallepedido
82	Can change Detalle de pedido	21	change_detallepedido
83	Can delete Detalle de pedido	21	delete_detallepedido
84	Can view Detalle de pedido	21	view_detallepedido
85	Can add Detalle de menú	22	add_detallemenu
86	Can change Detalle de menú	22	change_detallemenu
87	Can delete Detalle de menú	22	delete_detallemenu
88	Can view Detalle de menú	22	view_detallemenu
89	Can add Producto-Insumo	23	add_productoinsumo
90	Can change Producto-Insumo	23	change_productoinsumo
91	Can delete Producto-Insumo	23	delete_productoinsumo
92	Can view Producto-Insumo	23	view_productoinsumo
93	Can add Proveedor-Insumo	24	add_proveedorinsumo
94	Can change Proveedor-Insumo	24	change_proveedorinsumo
95	Can delete Proveedor-Insumo	24	delete_proveedorinsumo
96	Can view Proveedor-Insumo	24	view_proveedorinsumo
97	Can add Usuario-Rol	25	add_usuariorol
98	Can change Usuario-Rol	25	change_usuariorol
99	Can delete Usuario-Rol	25	delete_usuariorol
100	Can view Usuario-Rol	25	view_usuariorol
101	Can add Venta	26	add_venta
102	Can change Venta	26	change_venta
103	Can delete Venta	26	delete_venta
104	Can view Venta	26	view_venta
105	Can add Movimiento de caja	27	add_movimientocaja
106	Can change Movimiento de caja	27	change_movimientocaja
107	Can delete Movimiento de caja	27	delete_movimientocaja
108	Can view Movimiento de caja	27	view_movimientocaja
109	Can add Detalle de venta	28	add_detalleventa
110	Can change Detalle de venta	28	change_detalleventa
111	Can delete Detalle de venta	28	delete_detalleventa
112	Can view Detalle de venta	28	view_detalleventa
113	Can add Token	29	add_token
114	Can change Token	29	change_token
115	Can delete Token	29	delete_token
116	Can view Token	29	view_token
117	Can add Token	30	add_tokenproxy
118	Can change Token	30	change_tokenproxy
119	Can delete Token	30	delete_tokenproxy
120	Can view Token	30	view_tokenproxy
121	Can add Bebida	31	add_bebida
122	Can change Bebida	31	change_bebida
123	Can delete Bebida	31	delete_bebida
124	Can view Bebida	31	view_bebida
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$720000$vxOb1SHq2wNMdTne4bihrV$in/LlqP/3tBZSSNaq4u1Z0WKOd4MK1zzXcgKS7Ja8fs=	2026-10-21 01:03:51.871642+00	t	root				t	t	2026-09-29 17:31:33.873923+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
da71cd385b9e4022eb068218c8d9894f7a485f0c	2026-11-16 05:31:41.266158+00	1
\.


--
-- Data for Name: bebidas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.bebidas ("ID_bebidas", "Nombre", "Descripcion", "Estado", "Stock_actual", "Stock_minimo", "Precio_unitario", "Unidad") FROM stdin;
1	Coca cola zero		t	33.00	1	3400.00	Unidades
2	Coca Cola ZEro 1.5 lts		t	10.00	10	6000.00	unidades
\.


--
-- Data for Name: cajas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cajas ("ID_cajas", "Monto_apertura", "Monto_cierre", "Estado", "ID_locales", "ID_usuarios", "Fecha_hora_apertura", "Fecha_hora_cierre", "Diferencia_total", "Digital_esperado", "Digital_real", "Efectivo_esperado", "Efectivo_real", "Observaciones_cierre", "Ajuste_apertura") FROM stdin;
1	0.00	183500.00	f	1	1	2026-09-01 20:30:00+00	2026-09-02 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
2	0.00	187000.00	f	1	2	2026-09-02 20:30:00+00	2026-09-03 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
3	0.00	190500.00	f	1	1	2026-09-03 20:30:00+00	2026-09-04 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
4	0.00	194000.00	f	1	2	2026-09-04 20:30:00+00	2026-09-05 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
5	0.00	197500.00	f	1	1	2026-09-05 20:30:00+00	2026-09-06 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
6	0.00	201000.00	f	1	2	2026-09-06 20:30:00+00	2026-09-07 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
7	0.00	204500.00	f	1	1	2026-09-07 20:30:00+00	2026-09-08 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
8	0.00	208000.00	f	1	2	2026-09-08 20:30:00+00	2026-09-09 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
9	0.00	211500.00	f	1	1	2026-09-09 20:30:00+00	2026-09-10 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
10	0.00	215000.00	f	1	2	2026-09-10 20:30:00+00	2026-09-11 01:00:00+00	\N	\N	\N	\N	\N	\N	\N
11	1550.00	1.00	f	1	13	2026-11-03 20:54:22.701767+00	2026-11-10 20:17:07+00	\N	\N	\N	\N	\N	\N	\N
18	1111.00	155033.00	f	1	20	2026-11-10 20:21:53.738458+00	2026-11-10 21:14:11.736032+00	\N	\N	\N	\N	\N	\N	\N
20	33434.00	5656.00	f	1	20	2026-11-10 23:42:20.575635+00	2026-11-10 23:44:23.365501+00	\N	\N	\N	\N	\N	\N	\N
19	45521.00	7000.00	f	1	20	2026-11-10 23:25:38.027443+00	2026-11-11 15:51:30+00	\N	\N	\N	\N	\N	\N	\N
22	150000.00	8000.00	f	1	20	2026-11-13 23:42:35.240649+00	2026-11-13 23:48:10.10655+00	\N	\N	\N	\N	\N	\N	\N
23	150000.00	800000.00	f	1	20	2026-11-13 23:42:35.130582+00	2026-11-13 23:48:27.24612+00	\N	\N	\N	\N	\N	\N	\N
21	1000.00	2.00	f	1	20	2026-11-11 15:50:05.19778+00	2026-11-15 07:16:09.903864+00	\N	\N	\N	\N	\N	\N	\N
17	676767.00	1.00	f	1	20	2026-11-10 20:16:34.909298+00	2026-11-15 07:27:08.310366+00	\N	\N	\N	\N	\N	\N	\N
24	3000.00	1.00	f	1	20	2026-11-15 07:27:19.330756+00	2026-11-16 05:26:51.297843+00	\N	\N	\N	\N	\N	\N	\N
25	9000.00	1.00	f	1	1	2026-11-16 05:38:26.910476+00	2026-11-17 03:50:33.963582+00	\N	\N	\N	\N	\N	\N	\N
27	9000.00	9000.00	f	1	20	2026-11-18 17:11:36.311699+00	2026-11-18 17:14:26.115749+00	\N	\N	\N	\N	\N	\N	\N
26	7000.00	30200.00	f	1	2	2026-11-17 20:25:15.77534+00	2026-11-18 19:10:29.683315+00	\N	\N	\N	\N	\N	\N	\N
28	9999.00	9999.00	f	1	20	2026-11-18 21:26:09.847755+00	2026-11-19 16:28:28.419557+00	\N	\N	\N	\N	\N	\N	\N
29	9000.00	9000.00	f	1	20	2026-11-20 03:56:31.001819+00	2026-11-20 04:31:30.89956+00	0.00	0.00	0.00	9000.00	9000.00	\N	\N
30	6000.00	6000.00	f	1	20	2026-11-20 04:35:45.00625+00	2026-11-20 04:43:43.72251+00	0.00	0.00	0.00	6000.00	6000.00	\N	\N
31	1000.00	11000.00	f	1	20	2026-11-20 13:57:43.362101+00	2026-11-20 14:13:32.279245+00	10000.00	0.00	9000.00	1000.00	2000.00	Matías robó 10k	\N
32	8000.00	-18600.00	f	1	20	2026-11-20 14:44:52.594279+00	2026-11-20 16:42:11.28975+00	0.00	-125600.00	-125600.00	107000.00	107000.00	\N	\N
33	30000.00	37200.00	f	1	20	2026-11-20 17:49:18.132678+00	2026-11-20 17:58:39.466453+00	0.00	-24000.00	-24000.00	61200.00	61200.00	\N	\N
34	9000.00	9000.00	f	1	20	2026-11-20 18:19:45.091444+00	2026-11-20 18:26:36.091601+00	0.00	0.00	0.00	9000.00	9000.00	\N	\N
35	9000.00	99400.00	f	1	20	2026-11-20 19:44:12.725709+00	2026-11-20 19:53:33.463859+00	0.00	84000.00	84000.00	15400.00	15400.00	\N	\N
36	15400.00	23800.00	f	1	20	2026-11-20 19:53:52.72945+00	2026-11-20 20:05:04.329861+00	0.00	-12000.00	-12000.00	35800.00	35800.00	\N	\N
37	40000.00	-410000.00	f	1	20	2026-11-20 20:14:23.398334+00	2026-11-20 20:20:22.228085+00	0.00	-450000.00	-450000.00	40000.00	40000.00	\N	\N
38	45000.00	45000.00	f	1	20	2026-11-20 21:14:15.069105+00	2026-11-20 21:22:12.308482+00	0.00	0.00	0.00	45000.00	45000.00	\N	\N
39	45000.00	37000.00	f	1	20	2026-11-20 21:37:22.565426+00	2026-11-20 21:43:32.483856+00	0.00	-3000.00	-3000.00	40000.00	40000.00	\N	\N
40	50000.00	50000.00	f	1	20	2026-11-20 21:44:24.514818+00	2026-11-20 21:45:36.548539+00	0.00	0.00	0.00	50000.00	50000.00	\N	\N
41	30000.00	50000.00	f	1	20	2026-11-20 21:46:09.258989+00	2026-11-21 17:57:05.57602+00	0.00	0.00	0.00	50000.00	50000.00	\N	\N
42	50000.00	60000.00	f	1	20	2026-11-21 18:29:20.230739+00	2026-11-21 18:29:57.998392+00	0.00	0.00	0.00	60000.00	60000.00	\N	\N
43	60000.00	60000.00	f	1	20	2026-11-21 18:30:05.493969+00	2026-11-21 18:30:14.320847+00	0.00	0.00	0.00	60000.00	60000.00	\N	\N
44	60000.00	40000.00	f	1	20	2026-11-21 18:30:25.853503+00	2026-11-21 18:34:40.31891+00	0.00	0.00	0.00	40000.00	40000.00	\N	\N
45	40000.00	111200.00	f	1	20	2026-11-21 18:35:26.809019+00	2026-11-21 18:51:51.064454+00	0.00	0.00	0.00	111200.00	111200.00	\N	\N
46	111200.00	150000.00	f	1	20	2026-11-21 18:52:44.244978+00	2026-11-21 19:21:28.742357+00	0.00	0.00	0.00	150000.00	150000.00	\N	38800.00
\.


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categorias ("ID_categorias", "Nombre", "Descripcion") FROM stdin;
1	Carnes	Carnes y fiambres
2	Panificados	Panes para sándwiches
3	Verduras	Verduras frescas
4	Lácteos	Quesos y aderezos
5	Acompañamientos	Papas y guarniciones
6	Bebidas	Bebidas sin alcohol
\.


--
-- Data for Name: compras; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.compras ("ID_compras", "Precio_total", "ID_metodos", "ID_proveedores", "Fecha_hora_creacion") FROM stdin;
1	18500.00	1	2	2026-09-01 09:17:00+00
2	24000.00	1	3	2026-09-01 09:34:00+00
3	12500.00	1	4	2026-09-02 09:51:00+00
4	9800.00	2	5	2026-09-02 10:08:00+00
5	31000.00	1	6	2026-09-03 10:25:00+00
6	14500.00	1	1	2026-09-03 09:12:00+00
7	18500.00	1	2	2026-09-04 09:29:00+00
8	24000.00	2	3	2026-09-04 09:46:00+00
9	12500.00	1	4	2026-09-05 10:03:00+00
10	9800.00	1	5	2026-09-05 10:20:00+00
11	31000.00	1	6	2026-09-06 09:07:00+00
12	14500.00	2	1	2026-09-06 09:24:00+00
13	18500.00	1	2	2026-09-07 09:41:00+00
14	24000.00	1	3	2026-09-07 09:58:00+00
15	12500.00	1	4	2026-09-08 10:15:00+00
16	9800.00	2	5	2026-09-08 09:02:00+00
17	31000.00	1	6	2026-09-09 09:19:00+00
18	14500.00	1	1	2026-09-09 09:36:00+00
19	18500.00	1	2	2026-09-10 09:53:00+00
20	24000.00	2	3	2026-09-10 10:10:00+00
21	12500.00	1	4	2026-09-11 10:27:00+00
22	9800.00	1	5	2026-09-11 09:14:00+00
23	31000.00	1	6	2026-09-12 09:31:00+00
24	14500.00	2	1	2026-09-12 09:48:00+00
25	18500.00	1	2	2026-09-13 10:05:00+00
26	24000.00	1	3	2026-09-13 10:22:00+00
27	12500.00	1	4	2026-09-14 09:09:00+00
28	9800.00	2	5	2026-09-14 09:26:00+00
29	31000.00	1	6	2026-09-15 09:43:00+00
30	14500.00	1	1	2026-09-15 10:00:00+00
31	18500.00	1	2	2026-09-16 10:17:00+00
32	24000.00	2	3	2026-09-16 09:04:00+00
33	12500.00	1	4	2026-09-17 09:21:00+00
34	9800.00	1	5	2026-09-17 09:38:00+00
35	31000.00	1	6	2026-09-18 09:55:00+00
36	14500.00	2	1	2026-09-18 10:12:00+00
37	18500.00	1	2	2026-09-19 10:29:00+00
38	24000.00	1	3	2026-09-19 09:16:00+00
39	12500.00	1	4	2026-09-20 09:33:00+00
40	9800.00	2	5	2026-09-20 09:50:00+00
41	31000.00	1	6	2026-09-21 10:07:00+00
42	14500.00	1	1	2026-09-21 10:24:00+00
43	18500.00	1	2	2026-09-22 09:11:00+00
44	24000.00	2	3	2026-09-22 09:28:00+00
45	12500.00	1	4	2026-09-23 09:45:00+00
46	9800.00	1	5	2026-09-23 10:02:00+00
47	31000.00	1	6	2026-09-24 10:19:00+00
48	14500.00	2	1	2026-09-24 09:06:00+00
49	18500.00	1	2	2026-09-25 09:23:00+00
50	24000.00	1	3	2026-09-25 09:40:00+00
51	5000.00	1	8	2026-11-18 20:36:34.218222+00
52	10000.00	1	8	2026-11-18 20:38:46.82811+00
53	80000.00	1	1	2026-11-18 20:39:21.401657+00
54	26000.00	1	3	2026-11-19 20:28:29.854208+00
55	9000.00	2	8	2026-11-19 20:28:41.769869+00
56	18000.00	1	3	2026-11-20 14:47:04.464502+00
57	150000.00	2	3	2026-11-20 14:51:06.842594+00
58	24000.00	2	5	2026-11-20 17:54:29.161152+00
59	16000.00	2	11	2026-11-20 19:48:17.910849+00
60	20000.00	1	2	2026-11-20 19:53:06.196837+00
61	12000.00	2	2	2026-11-20 20:01:28.739817+00
62	450000.00	2	8	2026-11-20 20:17:52.884728+00
63	5000.00	1	\N	2026-11-20 21:38:02.578508+00
64	3000.00	2	\N	2026-11-20 21:38:02.593828+00
\.


--
-- Data for Name: detalles_compras; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.detalles_compras ("ID_detalles_compras", "Cantidad", "Subtotal", "ID_compras", "ID_insumos", "ID_bebidas") FROM stdin;
1	6	18500.00	1	1	\N
2	7	24000.00	2	2	\N
3	8	12500.00	3	3	\N
4	9	9800.00	4	4	\N
5	10	31000.00	5	5	\N
6	11	14500.00	6	6	\N
7	12	18500.00	7	7	\N
8	13	24000.00	8	8	\N
9	14	12500.00	9	9	\N
10	15	9800.00	10	10	\N
11	16	31000.00	11	1	\N
12	17	14500.00	12	2	\N
13	18	18500.00	13	3	\N
14	19	24000.00	14	4	\N
15	20	12500.00	15	5	\N
16	21	9800.00	16	6	\N
17	22	31000.00	17	7	\N
18	23	14500.00	18	8	\N
19	24	18500.00	19	9	\N
20	5	24000.00	20	10	\N
21	6	12500.00	21	1	\N
22	7	9800.00	22	2	\N
23	8	31000.00	23	3	\N
24	9	14500.00	24	4	\N
25	10	18500.00	25	5	\N
26	11	24000.00	26	6	\N
27	12	12500.00	27	7	\N
28	13	9800.00	28	8	\N
29	14	31000.00	29	9	\N
30	15	14500.00	30	10	\N
31	16	18500.00	31	1	\N
32	17	24000.00	32	2	\N
33	18	12500.00	33	3	\N
34	19	9800.00	34	4	\N
35	20	31000.00	35	5	\N
36	21	14500.00	36	6	\N
37	22	18500.00	37	7	\N
38	23	24000.00	38	8	\N
39	24	12500.00	39	9	\N
40	5	9800.00	40	10	\N
41	6	31000.00	41	1	\N
42	7	14500.00	42	2	\N
43	8	18500.00	43	3	\N
44	9	24000.00	44	4	\N
45	10	12500.00	45	5	\N
46	11	9800.00	46	6	\N
47	12	31000.00	47	7	\N
48	13	14500.00	48	8	\N
49	14	18500.00	49	9	\N
50	15	24000.00	50	10	\N
51	1	5000.00	51	10	\N
52	10	10000.00	52	\N	1
53	10	80000.00	53	1	\N
54	1	8000.00	54	2	\N
55	2	18000.00	54	2	\N
56	1	9000.00	55	3	\N
57	20	18000.00	56	3	\N
58	10	150000.00	57	1	\N
59	4	24000.00	58	\N	2
60	2	16000.00	59	6	\N
61	4	20000.00	60	9	\N
62	1	12000.00	61	3	\N
63	10	450000.00	62	\N	2
64	1	8000.00	63	8	\N
\.


--
-- Data for Name: detalles_menus; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.detalles_menus ("ID_detalles_menus", "Cantidad", "Descuento", "ID_menus", "ID_productos", "ID_bebidas") FROM stdin;
23	30	0	7	10	\N
30	10	0	8	9	\N
31	16	0	8	2	\N
32	12	0	8	1	\N
33	5	0	9	8	\N
34	2	0	9	7	\N
39	1	0	5	4	\N
40	1	0	5	3	\N
41	10	0	6	5	\N
42	15	0	6	6	\N
44	1	0	10	7	\N
45	1	0	10	5	\N
46	1	0	10	3	\N
47	2	0	11	3	\N
48	2	50	11	\N	2
\.


--
-- Data for Name: detalles_pedidos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.detalles_pedidos ("ID_detalles_pedidos", "Cantidad", "Subtotal", "ID_pedidos", "ID_productos", "Fecha_hora_creacion", "ID_bebidas", "ID_menus") FROM stdin;
1	2	17000.00	1	1	2026-09-01 20:41:00+00	\N	\N
2	1	7200.00	2	2	2026-09-01 20:52:00+00	\N	\N
3	2	13600.00	3	3	2026-09-02 21:03:00+00	\N	\N
4	1	5200.00	4	4	2026-09-02 21:14:00+00	\N	\N
5	2	15000.00	5	5	2026-09-03 21:25:00+00	\N	\N
6	1	6200.00	6	6	2026-09-03 21:36:00+00	\N	\N
7	2	5000.00	7	7	2026-09-04 21:47:00+00	\N	\N
8	1	3800.00	8	8	2026-09-04 21:58:00+00	\N	\N
9	2	21000.00	9	9	2026-09-05 22:09:00+00	\N	\N
10	1	1800.00	10	10	2026-09-05 22:20:00+00	\N	\N
11	2	17000.00	11	1	2026-09-06 22:31:00+00	\N	\N
12	1	7200.00	12	2	2026-09-06 22:42:00+00	\N	\N
13	2	13600.00	13	3	2026-09-07 22:53:00+00	\N	\N
14	1	5200.00	14	4	2026-09-07 23:04:00+00	\N	\N
15	2	15000.00	15	5	2026-09-08 23:15:00+00	\N	\N
16	1	6200.00	16	6	2026-09-08 23:26:00+00	\N	\N
17	2	5000.00	17	7	2026-09-09 23:37:00+00	\N	\N
18	1	3800.00	18	8	2026-09-09 23:48:00+00	\N	\N
19	2	21000.00	19	9	2026-09-10 23:59:00+00	\N	\N
20	1	1800.00	20	10	2026-09-10 20:40:00+00	\N	\N
21	2	17000.00	21	1	2026-09-11 20:51:00+00	\N	\N
22	1	7200.00	22	2	2026-09-11 21:02:00+00	\N	\N
23	2	13600.00	23	3	2026-09-12 21:13:00+00	\N	\N
24	1	5200.00	24	4	2026-09-12 21:24:00+00	\N	\N
25	2	15000.00	25	5	2026-09-13 21:35:00+00	\N	\N
26	1	6200.00	26	6	2026-09-13 21:46:00+00	\N	\N
27	2	5000.00	27	7	2026-09-14 21:57:00+00	\N	\N
28	1	3800.00	28	8	2026-09-14 22:08:00+00	\N	\N
29	2	21000.00	29	9	2026-09-15 22:19:00+00	\N	\N
30	1	1800.00	30	10	2026-09-15 22:30:00+00	\N	\N
31	2	17000.00	31	1	2026-09-16 22:41:00+00	\N	\N
32	1	7200.00	32	2	2026-09-16 22:52:00+00	\N	\N
33	2	13600.00	33	3	2026-09-17 23:03:00+00	\N	\N
34	1	5200.00	34	4	2026-09-17 23:14:00+00	\N	\N
35	2	15000.00	35	5	2026-09-18 23:25:00+00	\N	\N
36	1	6200.00	36	6	2026-09-18 23:36:00+00	\N	\N
37	2	5000.00	37	7	2026-09-19 23:47:00+00	\N	\N
38	1	3800.00	38	8	2026-09-19 23:58:00+00	\N	\N
39	2	21000.00	39	9	2026-09-20 20:39:00+00	\N	\N
40	1	1800.00	40	10	2026-09-20 20:50:00+00	\N	\N
41	2	17000.00	41	1	2026-09-21 21:01:00+00	\N	\N
42	1	7200.00	42	2	2026-09-21 21:12:00+00	\N	\N
43	2	13600.00	43	3	2026-09-22 21:23:00+00	\N	\N
44	1	5200.00	44	4	2026-09-22 21:34:00+00	\N	\N
45	2	15000.00	45	5	2026-09-23 21:45:00+00	\N	\N
46	1	6200.00	46	6	2026-09-23 21:56:00+00	\N	\N
47	2	5000.00	47	7	2026-09-24 22:07:00+00	\N	\N
48	1	3800.00	48	8	2026-09-24 22:18:00+00	\N	\N
49	2	21000.00	49	9	2026-09-25 22:29:00+00	\N	\N
50	1	1800.00	50	10	2026-09-25 22:40:00+00	\N	\N
51	2	5000.00	51	7	2026-11-11 18:12:21+00	\N	\N
52	2	15000.00	53	5	2026-11-13 22:00:11.285955+00	\N	\N
53	1	3800.00	53	8	2026-11-13 22:00:11.347774+00	\N	\N
54	1	3800.00	54	8	2026-11-13 22:09:59.832144+00	\N	\N
55	3	22500.00	54	5	2026-11-13 22:09:59.889258+00	\N	\N
56	1	6800.00	55	3	2026-11-13 22:20:38.853773+00	\N	\N
57	2	12400.00	55	6	2026-11-13 22:20:38.915851+00	\N	\N
58	2	15000.00	56	5	2026-11-13 22:34:34.406692+00	\N	\N
59	1	3800.00	56	8	2026-11-13 22:34:34.463339+00	\N	\N
60	2	17000.00	57	1	2026-11-13 23:37:37.822009+00	\N	\N
61	1	6200.00	58	6	2026-11-15 07:18:30.57751+00	\N	\N
62	1	5200.00	58	4	2026-11-15 07:18:30.639371+00	\N	\N
63	2	14400.00	59	2	2026-11-15 07:39:03.737584+00	\N	\N
64	3	5400.00	59	10	2026-11-15 07:39:03.801587+00	\N	\N
65	1	7200.00	60	2	2026-11-15 07:39:59.358242+00	\N	\N
66	1	6800.00	61	3	2026-11-15 07:49:20.674279+00	\N	\N
67	1	6800.00	62	3	2026-11-15 07:55:19.989584+00	\N	\N
68	1	6800.00	63	3	2026-11-15 07:59:14.501916+00	\N	\N
70	3	15600.00	65	4	2026-11-17 20:26:05.818117+00	\N	\N
71	2	7600.00	65	8	2026-11-17 20:26:05.820351+00	\N	\N
72	1	5200.00	66	4	2026-11-20 04:36:26.920707+00	\N	\N
73	1	7200.00	67	2	2026-11-20 04:36:50.79034+00	\N	\N
74	3	21000.00	68	3	2026-11-20 14:45:15.085675+00	\N	\N
75	1	3400.00	68	\N	2026-11-20 14:45:15.087724+00	1	\N
76	9	22500.00	69	7	2026-11-20 14:45:44.703099+00	\N	\N
77	9	94500.00	69	9	2026-11-20 14:45:44.705096+00	\N	\N
78	1	7200.00	70	2	2026-11-20 17:57:08.810056+00	\N	\N
79	4	24000.00	70	\N	2026-11-20 17:57:08.818059+00	2	\N
80	3	5400.00	71	10	2026-11-20 19:44:47.041195+00	\N	\N
81	2	21000.00	71	9	2026-11-20 19:44:47.047691+00	\N	\N
82	2	17000.00	72	1	2026-11-20 19:58:52.530983+00	\N	\N
83	1	3400.00	72	\N	2026-11-20 19:58:52.537279+00	1	\N
84	2	12000.00	73	\N	2026-11-20 20:19:32.665986+00	2	\N
85	1	20000.00	77	\N	2026-11-21 18:39:03.790794+00	\N	11
86	1	20000.00	78	\N	2026-11-21 18:49:07.325521+00	\N	11
87	1	3800.00	79	8	2026-11-21 18:49:53.8424+00	\N	\N
88	2	10400.00	79	4	2026-11-21 18:49:53.8429+00	\N	\N
89	1	17000.00	79	\N	2026-11-21 18:49:53.844444+00	\N	10
90	1	7200.00	80	2	2026-11-21 18:59:31.346805+00	\N	\N
91	1	7200.00	81	2	2026-11-21 19:00:18.623096+00	\N	\N
\.


--
-- Data for Name: detalles_ventas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.detalles_ventas ("ID_detalles_ventas", "Cantidad", "Subtotal", "ID_productos", "ID_ventas", "ID_bebidas", "ID_menus") FROM stdin;
1	2	17000.00	1	1	\N	\N
2	1	7200.00	2	2	\N	\N
3	2	13600.00	3	3	\N	\N
4	1	5200.00	4	4	\N	\N
5	2	15000.00	5	5	\N	\N
6	1	6200.00	6	6	\N	\N
7	2	5000.00	7	7	\N	\N
8	1	3800.00	8	8	\N	\N
9	2	21000.00	9	9	\N	\N
10	1	1800.00	10	10	\N	\N
11	2	17000.00	1	11	\N	\N
12	1	7200.00	2	12	\N	\N
13	2	13600.00	3	13	\N	\N
14	1	5200.00	4	14	\N	\N
15	2	15000.00	5	15	\N	\N
16	1	6200.00	6	16	\N	\N
17	2	5000.00	7	17	\N	\N
18	1	3800.00	8	18	\N	\N
19	2	21000.00	9	19	\N	\N
20	1	1800.00	10	20	\N	\N
21	2	17000.00	1	21	\N	\N
22	1	7200.00	2	22	\N	\N
23	2	13600.00	3	23	\N	\N
24	1	5200.00	4	24	\N	\N
25	2	15000.00	5	25	\N	\N
26	1	6200.00	6	26	\N	\N
27	2	5000.00	7	27	\N	\N
28	1	3800.00	8	28	\N	\N
29	2	21000.00	9	29	\N	\N
30	1	1800.00	10	30	\N	\N
31	2	17000.00	1	31	\N	\N
32	1	7200.00	2	32	\N	\N
33	2	13600.00	3	33	\N	\N
34	1	5200.00	4	34	\N	\N
35	2	15000.00	5	35	\N	\N
36	1	6200.00	6	36	\N	\N
37	2	5000.00	7	37	\N	\N
38	1	3800.00	8	38	\N	\N
39	2	21000.00	9	39	\N	\N
40	1	1800.00	10	40	\N	\N
41	2	17000.00	1	41	\N	\N
42	1	7200.00	2	42	\N	\N
43	2	13600.00	3	43	\N	\N
44	1	5200.00	4	44	\N	\N
45	2	15000.00	5	45	\N	\N
46	1	6200.00	6	46	\N	\N
47	2	5000.00	7	47	\N	\N
48	1	3800.00	8	48	\N	\N
49	2	21000.00	9	49	\N	\N
50	1	1800.00	10	50	\N	\N
51	2	7600.00	8	50	\N	\N
52	3	5400.00	10	56	\N	\N
53	3	5400.00	10	57	\N	\N
54	2	10400.00	4	57	\N	\N
55	3	5400.00	10	58	\N	\N
56	2	10400.00	4	58	\N	\N
57	2	15000.00	5	59	\N	\N
58	1	3800.00	8	59	\N	\N
59	1	3800.00	8	60	\N	\N
60	3	22500.00	5	60	\N	\N
61	1	6800.00	3	61	\N	\N
62	2	12400.00	6	61	\N	\N
63	2	15000.00	5	62	\N	\N
64	1	3800.00	8	62	\N	\N
65	2	15000.00	5	63	\N	\N
66	1	3800.00	8	63	\N	\N
67	1	6800.00	3	64	\N	\N
68	2	12400.00	6	64	\N	\N
69	1	3800.00	8	65	\N	\N
70	3	22500.00	5	65	\N	\N
71	2	17000.00	1	66	\N	\N
72	1	6200.00	6	67	\N	\N
73	1	5200.00	4	67	\N	\N
74	2	14400.00	2	68	\N	\N
75	3	5400.00	10	68	\N	\N
76	1	7200.00	2	69	\N	\N
77	1	6800.00	3	70	\N	\N
78	1	6800.00	3	71	\N	\N
79	3	15600.00	4	72	\N	\N
80	2	7600.00	8	72	\N	\N
81	3	21000.00	3	73	\N	\N
82	1	3400.00	\N	73	1	\N
83	9	22500.00	7	74	\N	\N
84	9	94500.00	9	74	\N	\N
85	1	7200.00	2	75	\N	\N
86	4	24000.00	\N	75	2	\N
87	3	5400.00	10	76	\N	\N
88	2	21000.00	9	76	\N	\N
89	2	17000.00	1	77	\N	\N
90	1	3400.00	\N	77	1	\N
91	1	20000.00	\N	78	\N	11
92	1	20000.00	\N	79	\N	11
93	1	3800.00	8	80	\N	\N
94	2	10400.00	4	80	\N	\N
95	1	17000.00	\N	80	\N	10
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-09-29 18:09:09.046103+00	1	Dueño	1	[{"added": {}}]	15	1
2	2026-09-29 23:01:47.604898+00	1	CuartelDelivery	1	[{"added": {}}]	10	1
3	2026-09-29 23:03:18.010507+00	1	matias	1	[{"added": {}}]	16	1
4	2026-09-29 23:05:42.897069+00	1	Caja #1 - CuartelDelivery	1	[{"added": {}}]	19	1
5	2026-09-30 00:00:31.353466+00	1	stepke, rocio	1	[{"added": {}}]	9	1
6	2026-09-30 00:00:40.920387+00	1	Hamburguesas Clasica Aguila	1	[{"added": {}}]	13	1
7	2026-09-30 00:00:50.159438+00	1	stepke, rocio	2	[{"changed": {"fields": ["Dni"]}}]	9	1
8	2026-09-30 00:03:54.916236+00	1	Pedido #1 - Matias	1	[{"added": {}}]	20	1
9	2026-09-30 00:05:00.03432+00	1	Pedido #1 - Matias	2	[{"changed": {"fields": ["Estado"]}}]	20	1
10	2026-09-30 00:06:36.716897+00	2	Hamburguesas Clasica Aguila	1	[{"added": {}}]	13	1
11	2026-09-30 00:06:49.09604+00	1	Efectivo	1	[{"added": {}}]	12	1
12	2026-09-30 00:07:06.685046+00	2	Hamburguesas Clasica Aguila Doble	2	[{"changed": {"fields": ["Nombre"]}}]	13	1
13	2026-09-30 00:07:10.43832+00	1	Compra #1 - $15000	1	[{"added": {}}]	8	1
14	2026-09-30 00:07:51.546068+00	3	Hamburguesas Clasica Aguila Triple	1	[{"added": {}}]	13	1
15	2026-09-30 00:09:46.57316+00	1	Carne	1	[{"added": {}}]	7	1
16	2026-09-30 00:10:06.384339+00	4	Bubba Gum Simple	1	[{"added": {}}]	13	1
17	2026-09-30 00:11:04.650533+00	5	Bubba Gum Doble	1	[{"added": {}}]	13	1
18	2026-09-30 00:11:32.602436+00	6	Bubba Gum Doble	1	[{"added": {}}]	13	1
19	2026-09-30 00:11:37.670611+00	1	Hamburguesa	1	[{"added": {}}]	17	1
20	2026-09-30 00:11:46.447525+00	1	Compra #Compra #1 - $15000.00 - Hamburguesa x123	1	[{"added": {}}]	18	1
21	2026-09-30 00:11:56.822911+00	7	Bubba Gum Triple	1	[{"added": {}}]	13	1
22	2026-09-30 00:12:17.284067+00	1	Compra #Compra #1 - $15000.00 - Hamburguesa x123	2	[]	18	1
23	2026-09-30 00:12:36.210069+00	1	Hamburguesa	2	[]	17	1
24	2026-09-30 00:13:17.84825+00	8	Mato on Fire Simple	1	[{"added": {}}]	13	1
25	2026-09-30 00:13:59.107645+00	9	Mato on Fire Doble	1	[{"added": {}}]	13	1
26	2026-09-30 00:14:29.941409+00	10	Mato on Fire Triple	1	[{"added": {}}]	13	1
27	2026-09-30 00:14:31.273528+00	1	Hamburguesa	2	[{"changed": {"fields": ["Unidad"]}}]	17	1
28	2026-09-30 00:15:56.689693+00	11	Hamburguesa de Cerdo Simple	1	[{"added": {}}]	13	1
29	2026-09-30 00:16:47.404573+00	1	Menu General	1	[{"added": {}}]	11	1
30	2026-09-30 00:17:15.227914+00	12	Hamburguesa de Cerdo Doble	1	[{"added": {}}]	13	1
31	2026-09-30 00:17:55.063654+00	12	Hamburguesa de Cerdo Triple	2	[{"changed": {"fields": ["Nombre", "Precio unitario"]}}]	13	1
32	2026-09-30 00:18:40.227301+00	13	Hamburguesa de Lentejas Simple	1	[{"added": {}}]	13	1
33	2026-09-30 00:19:09.003055+00	1	Menu General - Hamburguesas Clasica Aguila	1	[{"added": {}}]	22	1
34	2026-09-30 00:19:17.733916+00	14	Hamburguesa de Espinaca	1	[{"added": {}}]	13	1
35	2026-09-30 00:20:19.688988+00	15	La Cuartelera Simple	1	[{"added": {}}]	13	1
36	2026-09-30 00:21:30.922343+00	1	Pedido #Pedido #1 - Matias - Hamburguesas Clasica Aguila x30	1	[{"added": {}}]	21	1
37	2026-09-30 00:21:50.122003+00	16	La Cuartelera Doble	1	[{"added": {}}]	13	1
38	2026-09-30 00:22:20.289314+00	17	Lomito Soldado	1	[{"added": {}}]	13	1
39	2026-09-30 00:22:21.258549+00	1	Venta #1 - $173854	1	[{"added": {}}]	26	1
40	2026-09-30 00:22:52.715062+00	18	Lomito Cuartel	1	[{"added": {}}]	13	1
41	2026-09-30 00:23:34.43719+00	19	Bondiola de Cerdo	1	[{"added": {}}]	13	1
42	2026-09-30 00:23:49.659145+00	1	Venta #Venta #1 - $173854.00 - La Cuartelera Simple x2	1	[{"added": {}}]	28	1
43	2026-09-30 00:24:55.595698+00	20	Mila Guerrera	1	[{"added": {}}]	13	1
44	2026-09-30 00:26:30.520163+00	1	Hamburguesas Clasica Aguila Triple - Hamburguesa	1	[{"added": {}}]	23	1
45	2026-09-30 00:28:05.522197+00	21	Mila-Napo Terrorista	1	[{"added": {}}]	13	1
46	2026-09-30 00:29:46.23365+00	1	Super vea	1	[{"added": {}}]	14	1
47	2026-09-30 00:30:13.811483+00	1	Super vea - Hamburguesa	1	[{"added": {}}]	24	1
48	2026-09-30 00:31:47.073052+00	1	matias - Dueño	1	[{"added": {}}]	25	1
49	2026-09-30 00:35:26.803184+00	22	Mila-Napo Terrorista	1	[{"added": {}}]	13	1
50	2026-09-30 00:56:06.276994+00	2	Verduras	1	[{"added": {}}]	7	1
51	2026-09-30 00:56:17.462403+00	3	Bebidas	1	[{"added": {}}]	7	1
52	2026-09-30 00:56:42.128625+00	4	Aderesos	1	[{"added": {}}]	7	1
53	2026-09-30 00:58:24.981274+00	2	Tomate	1	[{"added": {}}]	17	1
54	2026-09-30 00:58:48.562344+00	3	Cebolla	1	[{"added": {}}]	17	1
55	2026-09-30 01:00:47.376169+00	2	cdaniel	1	[{"added": {}}]	16	1
56	2026-09-30 01:05:03.278104+00	3	karen	1	[{"added": {}}]	16	1
57	2026-09-30 01:08:16.462339+00	4	brisa	1	[{"added": {}}]	16	1
58	2026-09-30 01:25:19.775429+00	1	Super vea	2	[{"changed": {"fields": ["Telefono"]}}]	14	1
59	2026-09-30 03:58:20.763196+00	2	Colque, Daniel	1	[{"added": {}}]	9	1
60	2026-09-30 03:59:50.294973+00	3	mamaní, pablo	1	[{"added": {}}]	9	1
61	2026-10-01 20:28:51.367334+00	4	Lechuga	1	[{"added": {}}]	17	1
62	2026-10-14 23:27:49.296135+00	5	matias2	1	[{"added": {}}]	16	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	core	categoria
8	core	compra
9	core	empleado
10	core	local
11	core	menu
12	core	metodopago
13	core	producto
14	core	proveedor
15	core	rol
16	core	usuario
17	core	insumo
18	core	detallecompra
19	core	caja
20	core	pedido
21	core	detallepedido
22	core	detallemenu
23	core	productoinsumo
24	core	proveedorinsumo
25	core	usuariorol
26	core	venta
27	core	movimientocaja
28	core	detalleventa
29	authtoken	token
30	authtoken	tokenproxy
31	core	bebida
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-09-29 17:29:40.519861+00
2	auth	0001_initial	2026-09-29 17:29:44.659161+00
3	admin	0001_initial	2026-09-29 17:29:47.247065+00
4	admin	0002_logentry_remove_auto_add	2026-09-29 17:29:48.364949+00
5	admin	0003_logentry_add_action_flag_choices	2026-09-29 17:29:48.658229+00
6	contenttypes	0002_remove_content_type_name	2026-09-29 17:29:49.549645+00
7	auth	0002_alter_permission_name_max_length	2026-09-29 17:29:49.938466+00
8	auth	0003_alter_user_email_max_length	2026-09-29 17:29:51.232929+00
9	auth	0004_alter_user_username_opts	2026-09-29 17:29:52.035137+00
10	auth	0005_alter_user_last_login_null	2026-09-29 17:29:52.822157+00
11	auth	0006_require_contenttypes_0002	2026-09-29 17:29:53.616642+00
12	auth	0007_alter_validators_add_error_messages	2026-09-29 17:29:54.516767+00
13	auth	0008_alter_user_username_max_length	2026-09-29 17:29:55.305334+00
14	auth	0009_alter_user_last_name_max_length	2026-09-29 17:29:55.695737+00
15	auth	0010_alter_group_name_max_length	2026-09-29 17:29:56.39974+00
16	auth	0011_update_proxy_permissions	2026-09-29 17:29:56.90041+00
17	auth	0012_alter_user_first_name_max_length	2026-09-29 17:29:58.892719+00
18	core	0001_initial	2026-09-29 17:30:21.081848+00
19	core	0002_alter_productoinsumo_options_and_more	2026-09-29 17:30:21.202719+00
20	sessions	0001_initial	2026-09-29 17:30:22.888277+00
21	core	0003_alter_empleado_usuario	2026-10-15 00:22:01.051357+00
22	core	0004_remove_caja_fecha_apertura_remove_caja_fecha_cierre_and_more	2026-10-16 05:12:33.339621+00
23	core	0005_remove_venta_metodo_venta_id_metodo_and_more	2026-10-16 05:48:06.530775+00
24	core	0006_movimientocaja_tipo_movimiento	2026-10-16 06:19:48.207141+00
25	core	0007_alter_pedido_estado	2026-10-16 06:26:27.403961+00
26	core	0008_alter_pedido_estado	2026-10-16 06:27:11.131349+00
27	core	0009_alter_usuario_fecha_hora_modificacion	2026-10-16 07:56:24.07391+00
28	core	0010_alter_usuario_password	2026-10-16 08:51:19.964752+00
29	core	0011_alter_usuario_usuario	2026-10-16 09:08:33.866878+00
30	authtoken	0001_initial	2026-10-16 09:19:21.770133+00
31	authtoken	0002_auto_20160226_1747	2026-10-16 09:19:21.843345+00
32	authtoken	0003_tokenproxy	2026-10-16 09:19:22.004236+00
33	authtoken	0004_alter_tokenproxy_options	2026-10-16 09:19:22.166297+00
34	core	0012_usuario_groups_usuario_is_staff_usuario_is_superuser_and_more	2026-10-25 01:08:06.055308+00
35	core	0013_usuario_email	2026-10-29 20:42:41.007463+00
36	core	0013_rename_id_locales_empleado_local	2026-11-03 00:47:36.606805+00
37	core	0014_usuario_email	2026-11-03 20:06:59.353283+00
38	core	0015_rename_id_metodo_venta_metodo	2026-11-05 05:04:52.329369+00
39	core	0016_alter_empleado_dni	2026-11-06 04:53:48.973099+00
40	core	0017_pedido_pagado	2026-11-13 22:31:21.147624+00
41	core	0018_alter_pedido_direccion	2026-11-15 07:55:00.204633+00
42	core	0019_unique_caja_abierta_por_usuario	2026-11-18 17:05:51.708117+00
43	core	0020_bebida_remove_caja_unique_caja_abierta_por_usuario_and_more	2026-11-18 18:34:51.971608+00
44	core	0021_alter_empleado_dni_alter_proveedor_descripcion	2026-11-18 20:54:21.178562+00
45	core	0022_caja_diferencia_total_caja_digital_esperado_and_more	2026-11-20 04:29:48.270144+00
46	core	0023_movimientocaja_metodo	2026-11-20 19:30:57.534619+00
47	core	0024_detallepedido_menu_detalleventa_menu_and_more	2026-11-21 18:38:38.173306+00
48	core	0025_caja_ajuste_apertura	2026-11-21 18:48:26.004144+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
uiehhh103qmug2v0ungzpmso9bah8fea	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xBbg7:6DEYG65BOKvkqtPnnwj9D05-TUUVrLt22f2iK8wqPbk	2026-10-13 17:31:43.962958+00
79bi9xv5hff2kyf6r40s09z0l75mr3lp	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xBbgC:MWGSvsxnrVzCBOPe57WimBDe9co-lUYFSuW20dd5qns	2026-10-13 17:31:48.524988+00
0sx41xc3hjxwjfgn4maa9bukk8u7j9sr	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xBcFw:ZZD68JZ7R3ty6hsAXDCB11fCy9xKJkToolsoHuhfKwo	2026-10-13 18:08:44.043399+00
iwblvl7fgs9qhq1qb2mydwnj2q3nuevi	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xBgbS:fecbEANwOHZwYMXClPNkbF2ELgOSLi1Fe0Q1xWDqJh0	2026-10-13 22:47:14.419476+00
of2hssvpu6spqzgjm3vtwqxuwjh9dmci	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xBhKb:TJ6zdX7McbAm6dFR0FV9MVl-abgxxjBt10YhHkGBDzs	2026-10-13 23:33:53.648637+00
xx51xu8t5apceux55n5uox1w1coagm3v	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xBiCm:QBmI2_vT6RIfKz2bKgg7zLw-cCJT5FMtGVuv3v3PwCg	2026-10-14 00:29:52.676782+00
bi88ox7g0mlpbzidvsbqjetywy1ioug1	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xCP5O:ZawksnOfAaNhWJp-kPPKRciO3MvhZou-iTdFkm4WF7M	2026-10-15 22:17:06.258508+00
4viut3g3osgcn584gbz4g39x64m5ys04	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xEWCx:4NDQDWp__qJLydEaJcmHJTaNyynUTRkxx67xwDrJP5g	2026-10-21 18:17:39.569954+00
jmvhshf1n6z3uqemxferv1sxsgd8d3xr	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xEcMT:YEGeWCg-rGAJ4k5IRnJbKp4GH9K6BbroGKJv5g56gfE	2026-10-22 00:51:53.402049+00
ievc07rer7uytdtfkkqlgdvlxa5v3n6b	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xGnCk:k4A3FuBgl-Hojj2Cv5HFfZWDsLAEpit1YCLHuat6Dd8	2026-10-28 00:50:50.481823+00
60j0mle773sc4qpvp9rqcv2n7rsvcoa8	.eJxVjEEOwiAQRe_C2hAogoxL9z0DmWFAqoYmpV0Z7y5NutDtf-_9twi4rSVsLS1hYnEVWpx-N8L4THUH_MB6n2Wc67pMJHdFHrTJceb0uh3u30HBVnqN6pwNDkYTZrLOaEZAYO3tAJ6Msj6DV-yUwqQvGYAcO0jYAxe7Jj5f4Eg3zw:1xH7MO:LfgCzw7TPB-syEArzFPqisE8Asd4xQHNXp7pxn78lIQ	2026-10-28 22:22:08.927077+00
zu592oplwywfzqgc68u1ht583szeobri	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xKmpv:q3s3ZhxEyRQTEcPLcNmnDzzJScGskYdwm3R0ZayVdMY	2026-11-08 01:15:47.357798+00
ynrreznyqli521nm71afqao7m09tm2x2	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xKnB4:Kzhn74nUeGfaDgYBaWUIwl8Nax8dYTSxvCdlqmUcz5g	2026-11-08 01:37:38.54123+00
redenaitsmwb0ct7jxhdqzmmcd9j5opm	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xLrXR:3UHS8GedAmG9qdBaB5sQOGwpLjdEPaLMphh2S0hv9kM	2026-11-11 00:29:09.044879+00
179v5l4kibvfzrznos4cck6pcebjir0g	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xLrzT:5ppEqyVWoDcpIEakVf8kDrtoHSKZZ358AgUzYsqdez8	2026-11-11 00:58:07.29109+00
wlsu05eptjbmajdi5e2xxczexrgq0apn	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xNFA4:wYpLuwVb8e62VedsTUF_ZZ981eNjQAo4xncOURJVRec	2026-11-14 19:54:44.92266+00
c7jehhsoopysvxksgi73kie7red9unvo	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xOPR1:TLoemJolny9VwLcnFEGqWs1kf1cYy3ezSTFJiIIVxNo	2026-11-18 01:05:03.388101+00
ms80v5tbpi6tb98rqduckdrlxc8losbe	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xQsvO:9z07N1cPiu6i_IAkqJsZJYEz-vIq6MXrLpdNJrmC-Jk	2026-11-24 20:58:38.321284+00
y48g0smoaz04tb7rtn65mv4doarrnzl0	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xS0DW:QCxmMnjvlItQQcyrhHFgd4PpVCsT18TEbmWY8BWDj9I	2026-11-27 22:57:58.167311+00
275gphevc47r2cgl1e5n6ek6po3m335s	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xTMtI:gC5rrwsRHVeGDIpVzSHL9eapcPf0pW8_hxneYiTgh8I	2026-12-01 17:22:44.464533+00
g51wi1tju4oaz398butdy964tgrr2dz2	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xTMte:1tZ1DEQ8kMRtN_3d3XXd8WdGnTVBiOiltB4S1FxDYuU	2026-12-01 17:23:06.487278+00
5lvqm1yav0294h2wzpycpevr2v826a58	.eJxVjE0OgyAYBe_CuiHyJ9Jl956BPD6g2DaYiK6a3r2auGi3M_Pem3lsa_FbS4ufIrsyYdjlFwbQM9XDxAfqfeY013WZAj8SftrGxzmm1-1s_w4KWtnX1MscBMFpCBPIKW2hukFkhaykIBdcwk4oCGul7qWCNrBDRxEK1rDPFxHHOBU:1xTMtz:ddRbOjLTtx_ksqn-h1t3Ww-QaWCUD7ANa7RPHy1_3ts	2026-12-01 17:23:27.505718+00
\.


--
-- Data for Name: empleados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.empleados ("ID_empleados", "DNI", "Nombre", "Apellido", "Telefono", "Domicilio", "Estado", "ID_usuarios", "Fecha_hora_creacion", "ID_locales") FROM stdin;
2	30100002	Facundo	López	3875000002	Barrio Centro, Salta	t	2	2026-09-02 10:00:00+00	1
3	30100003	Nicolás	Gómez	3875000003	Barrio Centro, Salta	t	\N	2026-09-03 10:00:00+00	1
4	30100004	Matías	Rojas	3875000004	Barrio Centro, Salta	t	\N	2026-09-04 10:00:00+00	1
5	30100005	Santiago	Pérez	3875000005	Barrio Centro, Salta	t	\N	2026-09-05 10:00:00+00	1
6	30100006	Luciano	Díaz	3875000006	Barrio Centro, Salta	t	\N	2026-09-06 10:00:00+00	1
7	30100007	Tomás	Molina	3875000007	Barrio Centro, Salta	t	\N	2026-09-07 10:00:00+00	1
1	30100001	Gabriel	Pardo	3875000001	Barrio Centro, Salta	t	1	2026-09-01 10:00:00+00	1
9	34657653	Matías	Velazquez	3875110973	Av. prueba	t	18	2026-11-03 18:29:07.595915+00	1
12	44565019	Alejandro	Colque	3875110796		t	21	2026-11-18 19:02:56.638656+00	1
13	44956904	Mozo	Perón	38742389		t	22	2026-11-20 16:32:58.196284+00	1
11	44565010	Daniel	Colque	3875110796	B. Autódromo	t	20	2026-11-04 00:10:46.525867+00	1
14	40899819	Karen	Zalazar	3875440569		t	23	2026-11-20 18:32:57.171973+00	1
\.


--
-- Data for Name: insumos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.insumos ("ID_insumos", "Nombre", "Descripcion", "Unidad", "Stock_actual", "Stock_minimo", "ID_categorias") FROM stdin;
7	Tomate	Insumo gastronómico: tomaco	kg	18.00	5	3
17	Zanahoria	Insumo gastronómico	kg	23.00	2	3
18	verdura aji	,,,a	gr	3.00	1	3
19	Harina 000		kg	34.00	2	2
10	Mayonesa	Insumo gastronómico: Mayonesa	kg	2.00	2	6
1	Lomo vacuno	Insumo gastronómico: lomo vacuno	kg	55.00	10	1
9	Queso	Insumo gastronómico: queso	kg	14.00	3	4
3	Pan de lomito	Insumo gastronómico: pan de lomito	unidad	82.00	15	2
5	Papas	Insumo gastronómico: papas	kg	88.00	10	5
6	Lechuga	Insumo gastronómico: lechuga	l	8.00	4	3
4	Pan de hamburguesa	Insumo gastronómico: pan de hamburguesa	kg	44.00	12	2
2	Carne para hamburguesa	Insumo gastronómico: carne para hamburguesa	unidad	77.00	20	1
8	Jamón	Insumo gastronómico: jamón	kg	4.00	2	1
\.


--
-- Data for Name: locales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.locales ("ID_locales", "Nombre", "Direccion", "Telefono", "Red_social", "Fecha_hora_creacion") FROM stdin;
1	El Cuartel Delivery	Av. Reyes Católicos 2096, Salta, Argentina	0387-4000000	@elcuarteldelivery	2026-09-01 10:00:00+00
\.


--
-- Data for Name: menus; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.menus ("ID_menus", "Nombre", "Estado", "Fecha_hora_fin", "Fecha_hora_inicio") FROM stdin;
7	Gaseosas	t	\N	\N
8	Lomitos	t	\N	2026-11-10 23:42:00+00
9	Papas  fritas	t	\N	\N
5	Hamburguesas	t	\N	2026-11-10 23:40:00+00
6	Milanesas	t	\N	2026-11-10 23:40:00+00
10	Menú especial	t	\N	\N
11	Menu Black Friday	t	\N	\N
12	asd	t	\N	\N
\.


--
-- Data for Name: metodos_pago; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.metodos_pago ("ID_metodos", "Nombre", "Descripcion", "Estado") FROM stdin;
1	Efectivo	Pago en efectivo	t
2	Transferencia	Transferencia bancaria o billetera virtual	t
\.


--
-- Data for Name: movimientos_caja; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.movimientos_caja ("ID_movimientos", "Concepto", "Monto", "ID_cajas", "ID_compras", "ID_ventas", "Fecha_hora_creacion", "Tipo_movimiento", "ID_metodos") FROM stdin;
1	Venta #1	17000.00	1	\N	1	2026-09-01 20:43:00+00	Ingreso	\N
2	Venta #2	7200.00	2	\N	2	2026-09-01 20:56:00+00	Ingreso	\N
3	Venta #3	13600.00	3	\N	3	2026-09-02 21:09:00+00	Ingreso	\N
4	Venta #4	5200.00	4	\N	4	2026-09-02 21:22:00+00	Ingreso	\N
5	Venta #5	15000.00	5	\N	5	2026-09-03 21:35:00+00	Ingreso	\N
6	Venta #6	6200.00	6	\N	6	2026-09-03 21:48:00+00	Ingreso	\N
7	Venta #7	5000.00	7	\N	7	2026-09-04 22:01:00+00	Ingreso	\N
8	Venta #8	3800.00	8	\N	8	2026-09-04 22:14:00+00	Ingreso	\N
9	Venta #9	21000.00	9	\N	9	2026-09-05 22:27:00+00	Ingreso	\N
10	Venta #10	1800.00	10	\N	10	2026-09-05 22:40:00+00	Ingreso	\N
11	Venta #11	17000.00	1	\N	11	2026-09-06 22:53:00+00	Ingreso	\N
12	Venta #12	7200.00	2	\N	12	2026-09-06 23:06:00+00	Ingreso	\N
13	Venta #13	13600.00	3	\N	13	2026-09-07 23:19:00+00	Ingreso	\N
14	Venta #14	5200.00	4	\N	14	2026-09-07 23:32:00+00	Ingreso	\N
15	Venta #15	15000.00	5	\N	15	2026-09-08 23:45:00+00	Ingreso	\N
16	Venta #16	6200.00	6	\N	16	2026-09-08 23:58:00+00	Ingreso	\N
17	Venta #17	5000.00	7	\N	17	2026-09-09 20:31:00+00	Ingreso	\N
18	Venta #18	3800.00	8	\N	18	2026-09-09 20:44:00+00	Ingreso	\N
19	Venta #19	21000.00	9	\N	19	2026-09-10 20:57:00+00	Ingreso	\N
20	Venta #20	1800.00	10	\N	20	2026-09-10 21:10:00+00	Ingreso	\N
21	Venta #21	17000.00	1	\N	21	2026-09-11 21:23:00+00	Ingreso	\N
22	Venta #22	7200.00	2	\N	22	2026-09-11 21:36:00+00	Ingreso	\N
23	Venta #23	13600.00	3	\N	23	2026-09-12 21:49:00+00	Ingreso	\N
24	Venta #24	5200.00	4	\N	24	2026-09-12 22:02:00+00	Ingreso	\N
25	Venta #25	15000.00	5	\N	25	2026-09-13 22:15:00+00	Ingreso	\N
26	Venta #26	6200.00	6	\N	26	2026-09-13 22:28:00+00	Ingreso	\N
27	Venta #27	5000.00	7	\N	27	2026-09-14 22:41:00+00	Ingreso	\N
28	Venta #28	3800.00	8	\N	28	2026-09-14 22:54:00+00	Ingreso	\N
29	Venta #29	21000.00	9	\N	29	2026-09-15 23:07:00+00	Ingreso	\N
30	Venta #30	1800.00	10	\N	30	2026-09-15 23:20:00+00	Ingreso	\N
31	Venta #31	17000.00	1	\N	31	2026-09-16 23:33:00+00	Ingreso	\N
32	Venta #32	7200.00	2	\N	32	2026-09-16 23:46:00+00	Ingreso	\N
33	Venta #33	13600.00	3	\N	33	2026-09-17 23:59:00+00	Ingreso	\N
34	Venta #34	5200.00	4	\N	34	2026-09-17 20:32:00+00	Ingreso	\N
35	Venta #35	15000.00	5	\N	35	2026-09-18 20:45:00+00	Ingreso	\N
36	Compra de insumos #1	18500.00	6	1	\N	2026-09-18 20:58:00+00	Egreso	\N
37	Compra de insumos #2	24000.00	7	2	\N	2026-09-19 21:11:00+00	Egreso	\N
38	Compra de insumos #3	12500.00	8	3	\N	2026-09-19 21:24:00+00	Egreso	\N
39	Compra de insumos #4	9800.00	9	4	\N	2026-09-20 21:37:00+00	Egreso	\N
40	Compra de insumos #5	31000.00	10	5	\N	2026-09-20 21:50:00+00	Egreso	\N
41	Compra de insumos #6	14500.00	1	6	\N	2026-09-21 22:03:00+00	Egreso	\N
42	Compra de insumos #7	18500.00	2	7	\N	2026-09-21 22:16:00+00	Egreso	\N
43	Compra de insumos #8	24000.00	3	8	\N	2026-09-22 22:29:00+00	Egreso	\N
44	Compra de insumos #9	12500.00	4	9	\N	2026-09-22 22:42:00+00	Egreso	\N
45	Compra de insumos #10	9800.00	5	10	\N	2026-09-23 22:55:00+00	Egreso	\N
46	Compra de insumos #11	31000.00	6	11	\N	2026-09-23 23:08:00+00	Egreso	\N
47	Compra de insumos #12	14500.00	7	12	\N	2026-09-24 23:21:00+00	Egreso	\N
48	Compra de insumos #13	18500.00	8	13	\N	2026-09-24 23:34:00+00	Egreso	\N
49	Compra de insumos #14	24000.00	9	14	\N	2026-09-25 23:47:00+00	Egreso	\N
50	Compra de insumos #15	12500.00	10	15	\N	2026-09-26 00:00:00+00	Egreso	\N
51	Venta #59	18800.00	1	\N	59	2026-11-13 21:56:37.850868+00	Ingreso	\N
52	Venta #60	26300.00	17	\N	60	2026-11-13 22:10:01.448294+00	Ingreso	\N
53	Venta #61	19200.00	17	\N	61	2026-11-13 22:21:04.083804+00	Ingreso	\N
54	Venta #62	18800.00	17	\N	62	2026-11-13 22:35:56.857935+00	Ingreso	\N
55	Venta #63	18800.00	17	\N	63	2026-11-13 22:36:09.891533+00	Ingreso	\N
56	Venta #64	19200.00	17	\N	64	2026-11-13 22:36:21.01323+00	Ingreso	\N
57	Venta #65	26300.00	17	\N	65	2026-11-13 23:35:24.194646+00	Ingreso	\N
58	Venta #66	17000.00	21	\N	66	2026-11-13 23:37:40.565571+00	Ingreso	\N
59	Venta #67	11400.00	24	\N	67	2026-11-15 07:27:40.489774+00	Ingreso	\N
60	Venta #68	19800.00	24	\N	68	2026-11-15 07:39:19.056896+00	Ingreso	\N
61	Venta #69	7200.00	24	\N	69	2026-11-15 07:40:00.630017+00	Ingreso	\N
62	Venta #70	6800.00	24	\N	70	2026-11-15 07:55:21.407389+00	Ingreso	\N
63	Venta #71	6800.00	24	\N	71	2026-11-15 07:55:56.520677+00	Ingreso	\N
64	Venta #72	23200.00	26	\N	72	2026-11-17 20:26:39.321776+00	Ingreso	\N
65	Venta #73	24400.00	32	\N	73	2026-11-20 14:45:15.165706+00	Ingreso	\N
66	Venta #74	117000.00	32	\N	74	2026-11-20 14:45:44.735751+00	Ingreso	\N
67	Compra #56	18000.00	32	56	\N	2026-11-20 14:47:04.471686+00	Egreso	\N
68	Compra #57	150000.00	32	57	\N	2026-11-20 14:51:06.84791+00	Egreso	\N
69	Ingreso	20000.00	32	\N	\N	2026-11-20 16:33:42.969925+00	Ingreso	\N
70	Ingreso	100000.00	32	\N	\N	2026-11-20 16:34:26.151335+00	Ingreso	\N
71	Compra #58	24000.00	33	58	\N	2026-11-20 17:54:29.179529+00	Egreso	\N
72	Venta #75	31200.00	33	\N	75	2026-11-20 17:57:09.024205+00	Ingreso	\N
73	Venta #76	26400.00	35	\N	76	2026-11-20 19:44:47.316675+00	Ingreso	\N
74	Compra #59	16000.00	35	59	\N	2026-11-20 19:48:17.934818+00	Egreso	2
75	prueba	100000.00	35	\N	\N	2026-11-20 19:52:26.630846+00	Ingreso	2
76	Compra #60	20000.00	35	60	\N	2026-11-20 19:53:06.220735+00	Egreso	1
77	Venta #77	20400.00	36	\N	77	2026-11-20 19:58:52.731702+00	Ingreso	\N
78	Compra #61	12000.00	36	61	\N	2026-11-20 20:01:28.758575+00	Egreso	2
79	Compra #62	450000.00	37	62	\N	2026-11-20 20:17:52.907695+00	Egreso	2
80	Compra #63	5000.00	39	63	\N	2026-11-20 21:38:02.589971+00	Egreso	1
81	Compra #64	3000.00	39	64	\N	2026-11-20 21:38:02.59502+00	Egreso	2
82	me voy a miami sin mi señora	20000.00	41	\N	\N	2026-11-20 21:59:23.845336+00	Ingreso	1
83	w	10000.00	42	\N	\N	2026-11-21 18:29:20.231897+00	Ingreso	\N
84	asd	20000.00	44	\N	\N	2026-11-21 18:30:25.854147+00	Egreso	\N
85	Venta #78	20000.00	45	\N	78	2026-11-21 18:39:03.910953+00	Ingreso	\N
86	Venta #79	20000.00	45	\N	79	2026-11-21 18:49:07.40034+00	Ingreso	\N
87	Venta #80	31200.00	45	\N	80	2026-11-21 18:49:53.878745+00	Ingreso	\N
88	asds	38800.00	46	\N	\N	2026-11-21 18:52:44.24614+00	Ingreso	\N
\.


--
-- Data for Name: pedidos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pedidos ("ID_pedidos", "Cliente", "Direccion", "Precio_total", "Estado", "ID_empleados", "Fecha_hora_creacion", "Pagado") FROM stdin;
3	Cliente 03	103 - Barrio Portezuelo, Salta	13600.00	Cancelado	3	2026-09-02 21:03:00+00	f
7	Cliente 07	107 - Barrio El Huaico, Salta	5000.00	Cancelado	5	2026-09-04 21:47:00+00	f
11	Cliente 11	111 - Barrio Tres Cerritos, Salta	17000.00	Cancelado	5	2026-09-06 22:31:00+00	f
15	Cliente 15	115 - Barrio Centro, Salta	15000.00	Cancelado	3	2026-09-08 23:15:00+00	f
19	Cliente 19	119 - Barrio Grand Bourg, Salta	21000.00	Cancelado	5	2026-09-10 23:59:00+00	f
23	Cliente 23	123 - Barrio Portezuelo, Salta	13600.00	Cancelado	5	2026-09-12 21:13:00+00	f
27	Cliente 27	127 - Barrio El Huaico, Salta	5000.00	Cancelado	3	2026-09-14 21:57:00+00	f
31	Cliente 31	131 - Barrio Tres Cerritos, Salta	17000.00	Cancelado	5	2026-09-16 22:41:00+00	f
35	Cliente 35	135 - Barrio Centro, Salta	15000.00	Cancelado	5	2026-09-18 23:25:00+00	f
39	Cliente 39	139 - Barrio Grand Bourg, Salta	21000.00	Cancelado	3	2026-09-20 20:39:00+00	f
43	Cliente 43	143 - Barrio Portezuelo, Salta	13600.00	Cancelado	5	2026-09-22 21:23:00+00	f
47	Cliente 47	147 - Barrio El Huaico, Salta	5000.00	Cancelado	5	2026-09-24 22:07:00+00	f
57	Daniel2	Quinas285	17000.00	Finalizado	11	2026-11-13 23:37:37.656363+00	t
55	Matías	San Antonio	19200.00	Finalizado	11	2026-11-13 22:20:38.712205+00	t
53	Juan Pérez	Av. San Martín 1234	18800.00	Finalizado	1	2026-11-13 22:00:11.172738+00	t
56	Juan Pérez	Av. San Martín 1234	18800.00	Finalizado	1	2026-11-13 22:34:34.292402+00	t
54	Daniel	San martín	26300.00	Finalizado	11	2026-11-13 22:09:59.714665+00	t
66	asd	asd	5200.00	Cancelado	11	2026-11-20 04:36:26.858002+00	f
65	Juan	San martín	23200.00	Finalizado	2	2026-11-17 20:26:05.815537+00	t
67	weqe		7200.00	Cancelado	11	2026-11-20 04:36:50.789525+00	f
69	Ramón		117000.00	Finalizado	11	2026-11-20 14:45:44.702417+00	t
68	Juan		24400.00	Finalizado	11	2026-11-20 14:45:15.082493+00	t
70	yo		31200.00	Finalizado	11	2026-11-20 17:57:08.800716+00	t
72	karen	2	20400.00	Finalizado	11	2026-11-20 19:58:52.5185+00	t
58	Brisa	J. A. Fernández 975	11400.00	Finalizado	11	2026-11-15 07:18:30.454114+00	t
59	Martín	Gral. Richieri 601	19800.00	Finalizado	11	2026-11-15 07:39:03.611309+00	t
60	Juan	Gral. Richieri 601	7200.00	Finalizado	11	2026-11-15 07:39:59.245989+00	t
62	Martín		6800.00	Finalizado	11	2026-11-15 07:55:19.869452+00	t
61	asd	w	6800.00	Finalizado	11	2026-11-15 07:49:20.551488+00	t
71	sad		26400.00	Finalizado	11	2026-11-20 19:44:47.032187+00	t
78	asd		20000.00	Cancelado	11	2026-11-21 18:49:07.32345+00	t
79	www		31200.00	Cancelado	11	2026-11-21 18:49:53.841727+00	t
77	asd		20000.00	Cancelado	11	2026-11-21 18:39:03.788128+00	t
80	asd		7200.00	Cancelado	11	2026-11-21 18:59:31.346032+00	f
63	Marcos		6800.00	Cancelado	11	2026-11-15 07:59:14.382681+00	f
81	asd		7200.00	Cancelado	11	2026-11-21 19:00:18.622496+00	f
73	MARTIN RAMOS		12000.00	Cancelado	11	2026-11-20 20:19:32.659251+00	f
64	Juan Perez		1559.00	Cancelado	1	2026-11-16 05:38:55.977641+00	f
51	Jensen Huang	Barrio El Huarico 345	5000.00	Cancelado	11	2026-11-11 18:10:59+00	f
50	Cliente 50	150 - Barrio Centro, Salta	1800.00	Cancelado	5	2026-09-25 22:40:00+00	f
49	Cliente 49	149 - Barrio Grand Bourg, Salta	21000.00	Cancelado	5	2026-09-25 22:29:00+00	f
48	Cliente 48	148 - Barrio Portezuelo, Salta	3800.00	Cancelado	4	2026-09-24 22:18:00+00	f
44	Cliente 44	144 - Barrio Grand Bourg, Salta	5200.00	Cancelado	5	2026-09-22 21:34:00+00	f
46	Cliente 46	146 - Barrio Tres Cerritos, Salta	6200.00	Cancelado	5	2026-09-23 21:56:00+00	f
42	Cliente 42	142 - Barrio El Huaico, Salta	7200.00	Cancelado	4	2026-09-21 21:12:00+00	f
41	Cliente 41	141 - Barrio Tres Cerritos, Salta	17000.00	Cancelado	5	2026-09-21 21:01:00+00	f
40	Cliente 40	140 - Barrio Centro, Salta	1800.00	Cancelado	5	2026-09-20 20:50:00+00	f
38	Cliente 38	138 - Barrio Portezuelo, Salta	3800.00	Cancelado	5	2026-09-19 23:58:00+00	f
37	Cliente 37	137 - Barrio El Huaico, Salta	5000.00	Cancelado	5	2026-09-19 23:47:00+00	f
36	Cliente 36	136 - Barrio Tres Cerritos, Salta	6200.00	Cancelado	4	2026-09-18 23:36:00+00	f
34	Cliente 34	134 - Barrio Grand Bourg, Salta	5200.00	Cancelado	5	2026-09-17 23:14:00+00	f
33	Cliente 33	133 - Barrio Portezuelo, Salta	13600.00	Cancelado	3	2026-09-17 23:03:00+00	f
32	Cliente 32	132 - Barrio El Huaico, Salta	7200.00	Cancelado	5	2026-09-16 22:52:00+00	f
30	Cliente 30	130 - Barrio Centro, Salta	1800.00	Cancelado	4	2026-09-15 22:30:00+00	f
25	Cliente 25	125 - Barrio Centro, Salta	15000.00	Cancelado	5	2026-09-13 21:35:00+00	f
29	Cliente 29	129 - Barrio Grand Bourg, Salta	21000.00	Cancelado	5	2026-09-15 22:19:00+00	f
28	Cliente 28	128 - Barrio Portezuelo, Salta	3800.00	Cancelado	5	2026-09-14 22:08:00+00	f
24	Cliente 24	124 - Barrio Grand Bourg, Salta	5200.00	Cancelado	4	2026-09-12 21:24:00+00	f
22	Cliente 22	122 - Barrio El Huaico, Salta	7200.00	Cancelado	5	2026-09-11 21:02:00+00	f
26	Cliente 26	126 - Barrio Tres Cerritos, Salta	6200.00	Cancelado	5	2026-09-13 21:46:00+00	f
21	Cliente 21	121 - Barrio Tres Cerritos, Salta	17000.00	Cancelado	3	2026-09-11 20:51:00+00	f
20	Cliente 20	120 - Barrio Centro, Salta	1800.00	Cancelado	5	2026-09-10 20:40:00+00	f
18	Cliente 18	118 - Barrio Portezuelo, Salta	3800.00	Cancelado	4	2026-09-09 23:48:00+00	f
17	Cliente 17	117 - Barrio El Huaico, Salta	5000.00	Cancelado	5	2026-09-09 23:37:00+00	f
16	Cliente 16	116 - Barrio Tres Cerritos, Salta	6200.00	Cancelado	5	2026-09-08 23:26:00+00	f
14	Cliente 14	114 - Barrio Grand Bourg, Salta	5200.00	Cancelado	5	2026-09-07 23:04:00+00	f
13	Cliente 13	113 - Barrio Portezuelo, Salta	13600.00	Cancelado	5	2026-09-07 22:53:00+00	f
12	Cliente 12	112 - Barrio El Huaico, Salta	7200.00	Cancelado	4	2026-09-06 22:42:00+00	f
1	Cliente 01	101 - Barrio Tres Cerritos, Salta	17000.00	Cancelado	5	2026-09-01 20:41:00+00	f
10	Cliente 10	110 - Barrio Centro, Salta	1800.00	Cancelado	5	2026-09-05 22:20:00+00	f
9	Cliente 09	109 - Barrio Grand Bourg, Salta	21000.00	Cancelado	3	2026-09-05 22:09:00+00	f
8	Cliente 08	108 - Barrio Portezuelo, Salta	3800.00	Cancelado	5	2026-09-04 21:58:00+00	f
5	Cliente 05	105 - Barrio Centro, Salta	15000.00	Cancelado	5	2026-09-03 21:25:00+00	f
4	Cliente 04	104 - Barrio Grand Bourg, Salta	5200.00	Cancelado	5	2026-09-02 21:14:00+00	f
6	Cliente 06	106 - Barrio Tres Cerritos, Salta	6200.00	Cancelado	4	2026-09-03 21:36:00+00	f
2	Cliente 02	102 - Barrio El Huaico, Salta	7200.00	Cancelado	5	2026-09-01 20:52:00+00	f
45	Cliente 45	145 - Barrio Centro, Salta	15000.00	Cancelado	3	2026-09-23 21:45:00+00	f
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.productos ("ID_productos", "Nombre", "Descripcion", "Precio_unitario", "Estado") FROM stdin;
1	Lomito completo	Sándwich de lomo, jamón, queso, huevo y verduras	8500.00	t
2	Lomito simple	Sándwich de lomo con verduras y aderezos	7200.00	t
4	Hamburguesa simple	Hamburguesa con verduras y aderezos	5200.00	t
9	Lomito con papas	Lomito acompañado de papas fritas	10500.00	t
10	Gaseosa lata	Bebida en lata2	1800.00	t
5	Milanesa completa	Sándwich de milanesa con jamón, queso y verduras	7500.00	t
6	Milanesa simple	Sándwich de milanesa con verduras	6200.00	t
7	Papas fritas chicas	Porción chica de papas fritas	2500.00	t
8	Papas fritas grandes	Porción grande de papas fritas	3800.00	t
3	Hamburguesa completa	Hamburguesa con queso, jamón, huevo y verduras	7000.00	t
\.


--
-- Data for Name: productos_x_insumos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.productos_x_insumos ("ID_productos_insumos", "ID_insumos", "ID_productos", "Cantidad") FROM stdin;
1	1	1	1.00
2	3	1	1.00
3	6	1	1.00
4	7	1	1.00
5	8	1	1.00
6	9	1	1.00
7	10	1	1.00
8	1	2	1.00
9	3	2	1.00
36	6	5	1.00
37	4	5	1.00
38	2	5	1.00
43	2	6	1.00
44	3	6	1.00
45	10	6	1.00
46	8	6	1.00
47	5	7	1.00
56	2	3	1.00
57	4	3	1.00
58	6	3	1.00
59	8	3	1.00
\.


--
-- Data for Name: proveedores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.proveedores ("ID_proveedores", "Nombre", "Direccion", "Telefono", "Email", "CUIT", "Descripcion") FROM stdin;
1	Carnes del Norte	Mercado Cofruthos, Salta	3874001001	ventas1@proveedor.com.ar	30-71000001-4	Proveedor de carne vacuna
2	Panadería San José	Av. San Martín 1200, Salta	3874001002	ventas2@proveedor.com.ar	30-71000002-4	Pan para lomitos y hamburguesas
3	Verdulería El Verde	Mercado Cofruthos, Salta	3874001003	ventas3@proveedor.com.ar	30-71000003-4	Verduras frescas
4	Distribuidora Láctea	Av. Paraguay 450, Salta	3874001004	ventas4@proveedor.com.ar	30-71000004-4	Quesos y aderezos
5	Distribuidora Salta Bebidas	Zona sur, Salta	3874001005	ventas5@proveedor.com.ar	30-71000005-4	Bebidas
6	Papas del Valle	Cerrillos, Salta	3874001006	ventas6@proveedor.com.ar	30-71000006-4	Papas para fritura
8	Sin proveedor	\N	\N	\N	\N	Sin proveedor
10	Supermercado Día					
11	Verdulería San Marcos					
\.


--
-- Data for Name: proveedores_x_insumos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.proveedores_x_insumos ("ID_proveedores_insumos", "ID_insumos", "ID_proveedores") FROM stdin;
2	2	1
3	3	2
8	8	1
9	9	4
18	7	3
24	1	1
28	4	2
29	17	8
31	18	3
32	5	6
33	6	8
34	10	1
35	19	8
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles ("ID_roles", "Nombre", "Descripcion", "Estado") FROM stdin;
1	Dueño	Administración y supervisión del local	t
2	Cadete	Entrega de pedidos a domicilio	t
3	Planchero	Preparación de sándwiches en plancha	t
4	Ayudante de cocina	Preparación de ingredientes y empaquetado	t
5	Mozo	Atención a clientes y toma de pedidos	t
6	Administrador	Administrador	t
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios ("ID_usuarios", "Usuario", "Password", "Estado", "Fecha_hora_creacion", "Fecha_hora_modificacion", "Is_staff", "Is_superuser", "Email") FROM stdin;
13	admin	pbkdf2_sha256$720000$BoXkH1ClpahEWgeEROu6Pk$9Mbhow4ORcheAHVS2l6Zr6fk9v9fqqXgBoI4AcP8Hvc=	t	2026-10-16 23:01:44.388576+00	\N	f	f	brisadelmar2799@gmail.com
15	root	pbkdf2_sha256$720000$W0o1QEVVY9yla8tBkTEb8G$Qg8uCUYLCaPT6tK9vokFds/AD6+v3Dcpx8nhjlgkD4w=	t	2026-10-25 01:15:36.062195+00	\N	t	t	root@gmail.com
19	UsuarioPrueba1	pbkdf2_sha256$720000$xf37LqOpzYN0pSyz0WwOiV$nGIEuwFXVV4ThuRbO3f53w/tfdU8zDA3uLs649lqbG4=	t	2026-11-03 20:20:27.434535+00	\N	f	f	juan@gmail.com
1	gabriel	pbkdf2_sha256$720000$zWSrVKj3hPIyDqXHQnfN4f$3dXCL45+Vb78Tzz/L1YWBx/tR59hY1PjRNAmMoiVl4E=	t	2026-09-02 12:00:00+00	2026-10-02 18:00:00+00	f	f	gabriel@gmail.com
18	prueba	pbkdf2_sha256$720000$WqHQwuX1m7oO7N6ecbZKIb$RKBADaZCKT7jJ0xEbFLvRODIZZ3QNt2N5Jc3h96pxwg=	t	2026-11-03 18:29:07.417473+00	\N	f	f	prueba@gmail.com
2	facundo	pbkdf2_sha256$720000$cgFve7a38MMy5Xn1mVKh3J$AKyqiEwJ/+h26LHiF+OkYUePDVqz6SXbCMtbuZrF6rY=	t	2026-09-03 12:00:00+00	2026-10-03 18:00:00+00	f	f	facundo@gmail.com
21	daniel2	pbkdf2_sha256$720000$RT157VwuUYMRmk9nUCh5Ec$l/MAvz3VhBeYacquZNO1uFd+J9bUkf9mhMoTEcqS+WE=	t	2026-11-18 19:02:56.613228+00	\N	f	f	danielcolque2023@gmail.com
22	mozo1	pbkdf2_sha256$720000$B1w2hQei08nYJPMk6ymCnE$dD0HXbBL09smU4S2GoIcFBCPnsy/DXILlg+WisXQb7c=	t	2026-11-20 16:32:58.179014+00	\N	f	f	mozo1@gmail.com
20	Daniel	pbkdf2_sha256$720000$YC9G8Go2F0NFxLRVioBRqn$thx7lVs6KFJz/xjxDTYuz+cYMjyx4QK/fvP7pIMivY0=	t	2026-11-04 00:10:46.290564+00	\N	f	f	dcolque2025@gmail.com
23	Karen	pbkdf2_sha256$720000$RIgTYve3DLDjXJAZAvu4Lf$WzNOCqy8wOAUox2GJGAfTwl9vW2LJmsFy/Uu/STMfJI=	t	2026-11-20 18:32:57.166838+00	\N	f	f	zalazarkaren607@gmail.com
\.


--
-- Data for Name: usuarios_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios_groups (id, usuario_id, group_id) FROM stdin;
\.


--
-- Data for Name: usuarios_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios_user_permissions (id, usuario_id, permission_id) FROM stdin;
\.


--
-- Data for Name: usuarios_x_roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios_x_roles ("ID_usuarios_roles", "ID_roles", "ID_usuarios") FROM stdin;
2	1	2
16	4	19
21	1	1
28	6	13
32	5	18
38	4	21
39	5	22
40	6	20
41	5	23
\.


--
-- Data for Name: ventas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ventas ("ID_ventas", "Precio_total", "Fecha_hora_creacion", "ID_metodos") FROM stdin;
1	17000.00	2026-09-01 20:43:00+00	1
2	7200.00	2026-09-01 20:56:00+00	1
3	13600.00	2026-09-02 21:09:00+00	2
4	5200.00	2026-09-02 21:22:00+00	1
5	15000.00	2026-09-03 21:35:00+00	1
6	6200.00	2026-09-03 21:48:00+00	2
7	5000.00	2026-09-04 22:01:00+00	1
8	3800.00	2026-09-04 22:14:00+00	1
9	21000.00	2026-09-05 22:27:00+00	2
10	1800.00	2026-09-05 22:40:00+00	1
11	17000.00	2026-09-06 22:53:00+00	1
12	7200.00	2026-09-06 23:06:00+00	2
13	13600.00	2026-09-07 23:19:00+00	1
14	5200.00	2026-09-07 23:32:00+00	1
15	15000.00	2026-09-08 23:45:00+00	2
16	6200.00	2026-09-08 23:58:00+00	1
17	5000.00	2026-09-09 20:41:00+00	1
18	3800.00	2026-09-09 20:54:00+00	2
19	21000.00	2026-09-10 21:07:00+00	1
20	1800.00	2026-09-10 21:20:00+00	1
21	17000.00	2026-09-11 21:33:00+00	2
22	7200.00	2026-09-11 21:46:00+00	1
23	13600.00	2026-09-12 21:59:00+00	1
24	5200.00	2026-09-12 22:12:00+00	2
25	15000.00	2026-09-13 22:25:00+00	1
26	6200.00	2026-09-13 22:38:00+00	1
27	5000.00	2026-09-14 22:51:00+00	2
28	3800.00	2026-09-14 23:04:00+00	1
29	21000.00	2026-09-15 23:17:00+00	1
30	1800.00	2026-09-15 23:30:00+00	2
31	17000.00	2026-09-16 23:43:00+00	1
32	7200.00	2026-09-16 23:56:00+00	1
33	13600.00	2026-09-17 20:39:00+00	2
34	5200.00	2026-09-17 20:52:00+00	1
35	15000.00	2026-09-18 21:05:00+00	1
36	6200.00	2026-09-18 21:18:00+00	2
37	5000.00	2026-09-19 21:31:00+00	1
38	3800.00	2026-09-19 21:44:00+00	1
39	21000.00	2026-09-20 21:57:00+00	2
40	1800.00	2026-09-20 22:10:00+00	1
41	17000.00	2026-09-21 22:23:00+00	1
42	7200.00	2026-09-21 22:36:00+00	2
43	13600.00	2026-09-22 22:49:00+00	1
44	5200.00	2026-09-22 23:02:00+00	1
45	15000.00	2026-09-23 23:15:00+00	2
46	6200.00	2026-09-23 23:28:00+00	1
47	5000.00	2026-09-24 23:41:00+00	1
48	3800.00	2026-09-24 23:54:00+00	2
49	21000.00	2026-09-25 20:37:00+00	1
50	1800.00	2026-09-25 20:50:00+00	1
55	9999.00	2026-11-05 05:15:26.983073+00	1
56	20000.00	2026-11-06 23:46:07.789401+00	2
57	15800.00	2026-11-06 23:52:27.090535+00	2
58	15800.00	2026-11-07 00:11:58.213497+00	2
59	18800.00	2026-11-13 21:56:37.533411+00	1
60	26300.00	2026-11-13 22:10:01.160952+00	1
61	19200.00	2026-11-13 22:21:03.785091+00	1
62	18800.00	2026-11-13 22:35:56.5801+00	1
63	18800.00	2026-11-13 22:36:09.613858+00	1
64	19200.00	2026-11-13 22:36:20.740145+00	1
65	26300.00	2026-11-13 23:35:23.187282+00	1
66	17000.00	2026-11-13 23:37:40.230432+00	2
67	11400.00	2026-11-15 07:27:40.209586+00	1
68	19800.00	2026-11-15 07:39:18.760688+00	1
69	7200.00	2026-11-15 07:40:00.399315+00	2
70	6800.00	2026-11-15 07:55:21.170656+00	1
71	6800.00	2026-11-15 07:55:56.270436+00	2
72	23200.00	2026-11-17 20:26:39.317252+00	1
73	24400.00	2026-11-20 14:45:15.159689+00	2
74	117000.00	2026-11-20 14:45:44.733934+00	1
75	31200.00	2026-11-20 17:57:09.007965+00	1
76	26400.00	2026-11-20 19:44:47.299911+00	1
77	20400.00	2026-11-20 19:58:52.713082+00	1
78	20000.00	2026-11-21 18:39:03.902085+00	1
79	20000.00	2026-11-21 18:49:07.392576+00	1
80	31200.00	2026-11-21 18:49:53.870961+00	1
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 124, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: bebidas_ID_bebidas_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."bebidas_ID_bebidas_seq"', 2, true);


--
-- Name: cajas_ID_cajas_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."cajas_ID_cajas_seq"', 46, true);


--
-- Name: categorias_ID_categorias_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."categorias_ID_categorias_seq"', 6, true);


--
-- Name: compras_ID_compras_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."compras_ID_compras_seq"', 64, true);


--
-- Name: detalles_compras_ID_detalles_compras_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."detalles_compras_ID_detalles_compras_seq"', 64, true);


--
-- Name: detalles_menus_ID_detalles_menus_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."detalles_menus_ID_detalles_menus_seq"', 48, true);


--
-- Name: detalles_pedidos_ID_detalles_pedidos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."detalles_pedidos_ID_detalles_pedidos_seq"', 91, true);


--
-- Name: detalles_ventas_ID_detalles_ventas_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."detalles_ventas_ID_detalles_ventas_seq"', 95, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 64, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 31, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 48, true);


--
-- Name: empleados_ID_empleados_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."empleados_ID_empleados_seq"', 14, true);


--
-- Name: insumos_ID_insumos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."insumos_ID_insumos_seq"', 19, true);


--
-- Name: locales_ID_locales_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."locales_ID_locales_seq"', 1, true);


--
-- Name: menus_ID_menus_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."menus_ID_menus_seq"', 12, true);


--
-- Name: metodos_pago_ID_metodos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."metodos_pago_ID_metodos_seq"', 4, true);


--
-- Name: movimientos_caja_ID_movimientos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."movimientos_caja_ID_movimientos_seq"', 88, true);


--
-- Name: pedidos_ID_pedidos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."pedidos_ID_pedidos_seq"', 81, true);


--
-- Name: productos_ID_productos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."productos_ID_productos_seq"', 17, true);


--
-- Name: productos_x_insumos_ID_productos_insumos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."productos_x_insumos_ID_productos_insumos_seq"', 59, true);


--
-- Name: proveedores_ID_proveedores_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."proveedores_ID_proveedores_seq"', 11, true);


--
-- Name: proveedores_x_insumos_ID_proveedores_insumos_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."proveedores_x_insumos_ID_proveedores_insumos_seq"', 35, true);


--
-- Name: roles_ID_roles_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."roles_ID_roles_seq"', 6, true);


--
-- Name: usuarios_ID_usuarios_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."usuarios_ID_usuarios_seq"', 23, true);


--
-- Name: usuarios_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_groups_id_seq', 1, false);


--
-- Name: usuarios_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_user_permissions_id_seq', 1, false);


--
-- Name: usuarios_x_roles_ID_usuarios_roles_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."usuarios_x_roles_ID_usuarios_roles_seq"', 41, true);


--
-- Name: ventas_ID_ventas_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."ventas_ID_ventas_seq"', 80, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: bebidas bebidas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bebidas
    ADD CONSTRAINT bebidas_pkey PRIMARY KEY ("ID_bebidas");


--
-- Name: cajas cajas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT cajas_pkey PRIMARY KEY ("ID_cajas");


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY ("ID_categorias");


--
-- Name: compras compras_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras
    ADD CONSTRAINT compras_pkey PRIMARY KEY ("ID_compras");


--
-- Name: detalles_compras detalles_compras_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_compras
    ADD CONSTRAINT detalles_compras_pkey PRIMARY KEY ("ID_detalles_compras");


--
-- Name: detalles_menus detalles_menus_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_menus
    ADD CONSTRAINT detalles_menus_pkey PRIMARY KEY ("ID_detalles_menus");


--
-- Name: detalles_pedidos detalles_pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_pedidos
    ADD CONSTRAINT detalles_pedidos_pkey PRIMARY KEY ("ID_detalles_pedidos");


--
-- Name: detalles_ventas detalles_ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_ventas
    ADD CONSTRAINT detalles_ventas_pkey PRIMARY KEY ("ID_detalles_ventas");


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: empleados empleados_DNI_f6383a0f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT "empleados_DNI_f6383a0f_uniq" UNIQUE ("DNI");


--
-- Name: empleados empleados_ID_usuarios_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT "empleados_ID_usuarios_key" UNIQUE ("ID_usuarios");


--
-- Name: empleados empleados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_pkey PRIMARY KEY ("ID_empleados");


--
-- Name: insumos insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_pkey PRIMARY KEY ("ID_insumos");


--
-- Name: locales locales_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locales
    ADD CONSTRAINT locales_pkey PRIMARY KEY ("ID_locales");


--
-- Name: menus menus_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_pkey PRIMARY KEY ("ID_menus");


--
-- Name: metodos_pago metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_pkey PRIMARY KEY ("ID_metodos");


--
-- Name: movimientos_caja movimientos_caja_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos_caja
    ADD CONSTRAINT movimientos_caja_pkey PRIMARY KEY ("ID_movimientos");


--
-- Name: pedidos pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_pkey PRIMARY KEY ("ID_pedidos");


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY ("ID_productos");


--
-- Name: productos_x_insumos productos_x_insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos_x_insumos
    ADD CONSTRAINT productos_x_insumos_pkey PRIMARY KEY ("ID_productos_insumos");


--
-- Name: proveedores proveedores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proveedores
    ADD CONSTRAINT proveedores_pkey PRIMARY KEY ("ID_proveedores");


--
-- Name: proveedores_x_insumos proveedores_x_insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proveedores_x_insumos
    ADD CONSTRAINT proveedores_x_insumos_pkey PRIMARY KEY ("ID_proveedores_insumos");


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY ("ID_roles");


--
-- Name: usuarios usuarios_Email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT "usuarios_Email_key" UNIQUE ("Email");


--
-- Name: usuarios usuarios_Usuario_d070f9f8_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT "usuarios_Usuario_d070f9f8_uniq" UNIQUE ("Usuario");


--
-- Name: usuarios_groups usuarios_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_groups
    ADD CONSTRAINT usuarios_groups_pkey PRIMARY KEY (id);


--
-- Name: usuarios_groups usuarios_groups_usuario_id_group_id_a66c5ef3_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_groups
    ADD CONSTRAINT usuarios_groups_usuario_id_group_id_a66c5ef3_uniq UNIQUE (usuario_id, group_id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY ("ID_usuarios");


--
-- Name: usuarios_user_permissions usuarios_user_permission_usuario_id_permission_id_474b33a5_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_user_permissions
    ADD CONSTRAINT usuarios_user_permission_usuario_id_permission_id_474b33a5_uniq UNIQUE (usuario_id, permission_id);


--
-- Name: usuarios_user_permissions usuarios_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_user_permissions
    ADD CONSTRAINT usuarios_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: usuarios_x_roles usuarios_x_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_x_roles
    ADD CONSTRAINT usuarios_x_roles_pkey PRIMARY KEY ("ID_usuarios_roles");


--
-- Name: ventas ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY ("ID_ventas");


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: cajas_ID_locales_28ef83d6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "cajas_ID_locales_28ef83d6" ON public.cajas USING btree ("ID_locales");


--
-- Name: cajas_ID_usuarios_50c2a5e6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "cajas_ID_usuarios_50c2a5e6" ON public.cajas USING btree ("ID_usuarios");


--
-- Name: compras_ID_metodos_9ae1fccd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "compras_ID_metodos_9ae1fccd" ON public.compras USING btree ("ID_metodos");


--
-- Name: compras_ID_proveedores_9cd5bc8d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "compras_ID_proveedores_9cd5bc8d" ON public.compras USING btree ("ID_proveedores");


--
-- Name: detalles_compras_ID_bebidas_ff1996e1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_compras_ID_bebidas_ff1996e1" ON public.detalles_compras USING btree ("ID_bebidas");


--
-- Name: detalles_compras_ID_compras_55a183e8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_compras_ID_compras_55a183e8" ON public.detalles_compras USING btree ("ID_compras");


--
-- Name: detalles_compras_ID_insumos_51e60a73; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_compras_ID_insumos_51e60a73" ON public.detalles_compras USING btree ("ID_insumos");


--
-- Name: detalles_menus_ID_bebidas_e3eb27d2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_menus_ID_bebidas_e3eb27d2" ON public.detalles_menus USING btree ("ID_bebidas");


--
-- Name: detalles_menus_ID_menus_bef9c4b8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_menus_ID_menus_bef9c4b8" ON public.detalles_menus USING btree ("ID_menus");


--
-- Name: detalles_menus_ID_productos_916ea542; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_menus_ID_productos_916ea542" ON public.detalles_menus USING btree ("ID_productos");


--
-- Name: detalles_pedidos_ID_bebidas_455c7b3a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_pedidos_ID_bebidas_455c7b3a" ON public.detalles_pedidos USING btree ("ID_bebidas");


--
-- Name: detalles_pedidos_ID_menus_346aa29f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_pedidos_ID_menus_346aa29f" ON public.detalles_pedidos USING btree ("ID_menus");


--
-- Name: detalles_pedidos_ID_pedidos_4b484066; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_pedidos_ID_pedidos_4b484066" ON public.detalles_pedidos USING btree ("ID_pedidos");


--
-- Name: detalles_pedidos_ID_productos_0f6135e9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_pedidos_ID_productos_0f6135e9" ON public.detalles_pedidos USING btree ("ID_productos");


--
-- Name: detalles_ventas_ID_Producto_87aa0904; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_ventas_ID_Producto_87aa0904" ON public.detalles_ventas USING btree ("ID_productos");


--
-- Name: detalles_ventas_ID_Ventas_23ed946a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_ventas_ID_Ventas_23ed946a" ON public.detalles_ventas USING btree ("ID_ventas");


--
-- Name: detalles_ventas_ID_bebidas_8913caee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_ventas_ID_bebidas_8913caee" ON public.detalles_ventas USING btree ("ID_bebidas");


--
-- Name: detalles_ventas_ID_menus_73928115; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "detalles_ventas_ID_menus_73928115" ON public.detalles_ventas USING btree ("ID_menus");


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: empleados_DNI_f6383a0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "empleados_DNI_f6383a0f_like" ON public.empleados USING btree ("DNI" varchar_pattern_ops);


--
-- Name: empleados_ID_locales_6a406bf7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "empleados_ID_locales_6a406bf7" ON public.empleados USING btree ("ID_locales");


--
-- Name: insumos_ID_categorias_a8603f21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "insumos_ID_categorias_a8603f21" ON public.insumos USING btree ("ID_categorias");


--
-- Name: movimientos_caja_ID_cajas_5a6a50a2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "movimientos_caja_ID_cajas_5a6a50a2" ON public.movimientos_caja USING btree ("ID_cajas");


--
-- Name: movimientos_caja_ID_compras_d2b0b618; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "movimientos_caja_ID_compras_d2b0b618" ON public.movimientos_caja USING btree ("ID_compras");


--
-- Name: movimientos_caja_ID_metodos_c59a5ebf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "movimientos_caja_ID_metodos_c59a5ebf" ON public.movimientos_caja USING btree ("ID_metodos");


--
-- Name: movimientos_caja_ID_ventas_3a75543f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "movimientos_caja_ID_ventas_3a75543f" ON public.movimientos_caja USING btree ("ID_ventas");


--
-- Name: pedidos_ID_empleados_dc487bb8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "pedidos_ID_empleados_dc487bb8" ON public.pedidos USING btree ("ID_empleados");


--
-- Name: productos_x_insumos_ID_insumos_e300d21f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "productos_x_insumos_ID_insumos_e300d21f" ON public.productos_x_insumos USING btree ("ID_insumos");


--
-- Name: productos_x_insumos_ID_productos_f6ea820a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "productos_x_insumos_ID_productos_f6ea820a" ON public.productos_x_insumos USING btree ("ID_productos");


--
-- Name: proveedores_x_insumos_ID_insumos_60721ae4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "proveedores_x_insumos_ID_insumos_60721ae4" ON public.proveedores_x_insumos USING btree ("ID_insumos");


--
-- Name: proveedores_x_insumos_ID_proveedores_dda42c15; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "proveedores_x_insumos_ID_proveedores_dda42c15" ON public.proveedores_x_insumos USING btree ("ID_proveedores");


--
-- Name: unique_caja_abierta_por_local; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_caja_abierta_por_local ON public.cajas USING btree ("ID_locales") WHERE ("Estado" AND ("Fecha_hora_cierre" IS NULL));


--
-- Name: usuarios_Email_ed42e3ee_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "usuarios_Email_ed42e3ee_like" ON public.usuarios USING btree ("Email" varchar_pattern_ops);


--
-- Name: usuarios_Usuario_d070f9f8_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "usuarios_Usuario_d070f9f8_like" ON public.usuarios USING btree ("Usuario" varchar_pattern_ops);


--
-- Name: usuarios_groups_group_id_18c61092; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX usuarios_groups_group_id_18c61092 ON public.usuarios_groups USING btree (group_id);


--
-- Name: usuarios_groups_usuario_id_1132ca50; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX usuarios_groups_usuario_id_1132ca50 ON public.usuarios_groups USING btree (usuario_id);


--
-- Name: usuarios_user_permissions_permission_id_af615ca1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX usuarios_user_permissions_permission_id_af615ca1 ON public.usuarios_user_permissions USING btree (permission_id);


--
-- Name: usuarios_user_permissions_usuario_id_232fd58d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX usuarios_user_permissions_usuario_id_232fd58d ON public.usuarios_user_permissions USING btree (usuario_id);


--
-- Name: usuarios_x_roles_ID_roles_b66222d0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "usuarios_x_roles_ID_roles_b66222d0" ON public.usuarios_x_roles USING btree ("ID_roles");


--
-- Name: usuarios_x_roles_ID_usuarios_a0fd5f7b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "usuarios_x_roles_ID_usuarios_a0fd5f7b" ON public.usuarios_x_roles USING btree ("ID_usuarios");


--
-- Name: ventas_ID_metodos_fd57bd27; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ventas_ID_metodos_fd57bd27" ON public.ventas USING btree ("ID_metodos");


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_usuarios_ID_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT "authtoken_token_user_id_35299eff_fk_usuarios_ID_usuarios" FOREIGN KEY (user_id) REFERENCES public.usuarios("ID_usuarios") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cajas cajas_ID_locales_28ef83d6_fk_locales_ID_locales; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT "cajas_ID_locales_28ef83d6_fk_locales_ID_locales" FOREIGN KEY ("ID_locales") REFERENCES public.locales("ID_locales") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cajas cajas_ID_usuarios_50c2a5e6_fk_usuarios_ID_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cajas
    ADD CONSTRAINT "cajas_ID_usuarios_50c2a5e6_fk_usuarios_ID_usuarios" FOREIGN KEY ("ID_usuarios") REFERENCES public.usuarios("ID_usuarios") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: compras compras_ID_metodos_9ae1fccd_fk_metodos_pago_ID_metodos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras
    ADD CONSTRAINT "compras_ID_metodos_9ae1fccd_fk_metodos_pago_ID_metodos" FOREIGN KEY ("ID_metodos") REFERENCES public.metodos_pago("ID_metodos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: compras compras_ID_proveedores_9cd5bc8d_fk_proveedores_ID_proveedores; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras
    ADD CONSTRAINT "compras_ID_proveedores_9cd5bc8d_fk_proveedores_ID_proveedores" FOREIGN KEY ("ID_proveedores") REFERENCES public.proveedores("ID_proveedores") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_compras detalles_compras_ID_bebidas_ff1996e1_fk_bebidas_ID_bebidas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_compras
    ADD CONSTRAINT "detalles_compras_ID_bebidas_ff1996e1_fk_bebidas_ID_bebidas" FOREIGN KEY ("ID_bebidas") REFERENCES public.bebidas("ID_bebidas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_compras detalles_compras_ID_compras_55a183e8_fk_compras_ID_compras; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_compras
    ADD CONSTRAINT "detalles_compras_ID_compras_55a183e8_fk_compras_ID_compras" FOREIGN KEY ("ID_compras") REFERENCES public.compras("ID_compras") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_compras detalles_compras_ID_insumos_51e60a73_fk_insumos_ID_insumos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_compras
    ADD CONSTRAINT "detalles_compras_ID_insumos_51e60a73_fk_insumos_ID_insumos" FOREIGN KEY ("ID_insumos") REFERENCES public.insumos("ID_insumos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_menus detalles_menus_ID_bebidas_e3eb27d2_fk_bebidas_ID_bebidas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_menus
    ADD CONSTRAINT "detalles_menus_ID_bebidas_e3eb27d2_fk_bebidas_ID_bebidas" FOREIGN KEY ("ID_bebidas") REFERENCES public.bebidas("ID_bebidas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_menus detalles_menus_ID_menus_bef9c4b8_fk_menus_ID_menus; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_menus
    ADD CONSTRAINT "detalles_menus_ID_menus_bef9c4b8_fk_menus_ID_menus" FOREIGN KEY ("ID_menus") REFERENCES public.menus("ID_menus") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_menus detalles_menus_ID_productos_916ea542_fk_productos_ID_productos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_menus
    ADD CONSTRAINT "detalles_menus_ID_productos_916ea542_fk_productos_ID_productos" FOREIGN KEY ("ID_productos") REFERENCES public.productos("ID_productos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_pedidos detalles_pedidos_ID_bebidas_455c7b3a_fk_bebidas_ID_bebidas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_pedidos
    ADD CONSTRAINT "detalles_pedidos_ID_bebidas_455c7b3a_fk_bebidas_ID_bebidas" FOREIGN KEY ("ID_bebidas") REFERENCES public.bebidas("ID_bebidas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_pedidos detalles_pedidos_ID_menus_346aa29f_fk_menus_ID_menus; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_pedidos
    ADD CONSTRAINT "detalles_pedidos_ID_menus_346aa29f_fk_menus_ID_menus" FOREIGN KEY ("ID_menus") REFERENCES public.menus("ID_menus") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_pedidos detalles_pedidos_ID_pedidos_4b484066_fk_pedidos_ID_pedidos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_pedidos
    ADD CONSTRAINT "detalles_pedidos_ID_pedidos_4b484066_fk_pedidos_ID_pedidos" FOREIGN KEY ("ID_pedidos") REFERENCES public.pedidos("ID_pedidos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_pedidos detalles_pedidos_ID_productos_0f6135e9_fk_productos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_pedidos
    ADD CONSTRAINT "detalles_pedidos_ID_productos_0f6135e9_fk_productos" FOREIGN KEY ("ID_productos") REFERENCES public.productos("ID_productos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_ventas detalles_ventas_ID_bebidas_8913caee_fk_bebidas_ID_bebidas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_ventas
    ADD CONSTRAINT "detalles_ventas_ID_bebidas_8913caee_fk_bebidas_ID_bebidas" FOREIGN KEY ("ID_bebidas") REFERENCES public.bebidas("ID_bebidas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_ventas detalles_ventas_ID_menus_73928115_fk_menus_ID_menus; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_ventas
    ADD CONSTRAINT "detalles_ventas_ID_menus_73928115_fk_menus_ID_menus" FOREIGN KEY ("ID_menus") REFERENCES public.menus("ID_menus") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_ventas detalles_ventas_ID_productos_9f2b2ef2_fk_productos_ID_productos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_ventas
    ADD CONSTRAINT "detalles_ventas_ID_productos_9f2b2ef2_fk_productos_ID_productos" FOREIGN KEY ("ID_productos") REFERENCES public.productos("ID_productos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: detalles_ventas detalles_ventas_ID_ventas_6b1d9400_fk_ventas_ID_ventas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalles_ventas
    ADD CONSTRAINT "detalles_ventas_ID_ventas_6b1d9400_fk_ventas_ID_ventas" FOREIGN KEY ("ID_ventas") REFERENCES public.ventas("ID_ventas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empleados empleados_ID_locales_6a406bf7_fk_locales_ID_locales; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT "empleados_ID_locales_6a406bf7_fk_locales_ID_locales" FOREIGN KEY ("ID_locales") REFERENCES public.locales("ID_locales") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empleados empleados_ID_usuarios_bfd72eb0_fk_usuarios_ID_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT "empleados_ID_usuarios_bfd72eb0_fk_usuarios_ID_usuarios" FOREIGN KEY ("ID_usuarios") REFERENCES public.usuarios("ID_usuarios") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: insumos insumos_ID_categorias_a8603f21_fk_categorias_ID_categorias; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT "insumos_ID_categorias_a8603f21_fk_categorias_ID_categorias" FOREIGN KEY ("ID_categorias") REFERENCES public.categorias("ID_categorias") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: movimientos_caja movimientos_caja_ID_cajas_5a6a50a2_fk_cajas_ID_cajas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos_caja
    ADD CONSTRAINT "movimientos_caja_ID_cajas_5a6a50a2_fk_cajas_ID_cajas" FOREIGN KEY ("ID_cajas") REFERENCES public.cajas("ID_cajas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: movimientos_caja movimientos_caja_ID_compras_d2b0b618_fk_compras_ID_compras; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos_caja
    ADD CONSTRAINT "movimientos_caja_ID_compras_d2b0b618_fk_compras_ID_compras" FOREIGN KEY ("ID_compras") REFERENCES public.compras("ID_compras") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: movimientos_caja movimientos_caja_ID_metodos_c59a5ebf_fk_metodos_pago_ID_metodos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos_caja
    ADD CONSTRAINT "movimientos_caja_ID_metodos_c59a5ebf_fk_metodos_pago_ID_metodos" FOREIGN KEY ("ID_metodos") REFERENCES public.metodos_pago("ID_metodos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: movimientos_caja movimientos_caja_ID_ventas_3a75543f_fk_ventas_ID_ventas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos_caja
    ADD CONSTRAINT "movimientos_caja_ID_ventas_3a75543f_fk_ventas_ID_ventas" FOREIGN KEY ("ID_ventas") REFERENCES public.ventas("ID_ventas") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pedidos pedidos_ID_empleados_dc487bb8_fk_empleados_ID_empleados; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT "pedidos_ID_empleados_dc487bb8_fk_empleados_ID_empleados" FOREIGN KEY ("ID_empleados") REFERENCES public.empleados("ID_empleados") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: productos_x_insumos productos_x_insumos_ID_insumos_e300d21f_fk_insumos_ID_insumos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos_x_insumos
    ADD CONSTRAINT "productos_x_insumos_ID_insumos_e300d21f_fk_insumos_ID_insumos" FOREIGN KEY ("ID_insumos") REFERENCES public.insumos("ID_insumos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: productos_x_insumos productos_x_insumos_ID_productos_f6ea820a_fk_productos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos_x_insumos
    ADD CONSTRAINT "productos_x_insumos_ID_productos_f6ea820a_fk_productos" FOREIGN KEY ("ID_productos") REFERENCES public.productos("ID_productos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: proveedores_x_insumos proveedores_x_insumo_ID_proveedores_dda42c15_fk_proveedor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proveedores_x_insumos
    ADD CONSTRAINT "proveedores_x_insumo_ID_proveedores_dda42c15_fk_proveedor" FOREIGN KEY ("ID_proveedores") REFERENCES public.proveedores("ID_proveedores") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: proveedores_x_insumos proveedores_x_insumos_ID_insumos_60721ae4_fk_insumos_ID_insumos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proveedores_x_insumos
    ADD CONSTRAINT "proveedores_x_insumos_ID_insumos_60721ae4_fk_insumos_ID_insumos" FOREIGN KEY ("ID_insumos") REFERENCES public.insumos("ID_insumos") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios_groups usuarios_groups_group_id_18c61092_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_groups
    ADD CONSTRAINT usuarios_groups_group_id_18c61092_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios_groups usuarios_groups_usuario_id_1132ca50_fk_usuarios_ID_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_groups
    ADD CONSTRAINT "usuarios_groups_usuario_id_1132ca50_fk_usuarios_ID_usuarios" FOREIGN KEY (usuario_id) REFERENCES public.usuarios("ID_usuarios") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios_user_permissions usuarios_user_permis_permission_id_af615ca1_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_user_permissions
    ADD CONSTRAINT usuarios_user_permis_permission_id_af615ca1_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios_user_permissions usuarios_user_permis_usuario_id_232fd58d_fk_usuarios_; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_user_permissions
    ADD CONSTRAINT usuarios_user_permis_usuario_id_232fd58d_fk_usuarios_ FOREIGN KEY (usuario_id) REFERENCES public.usuarios("ID_usuarios") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios_x_roles usuarios_x_roles_ID_roles_b66222d0_fk_roles_ID_roles; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_x_roles
    ADD CONSTRAINT "usuarios_x_roles_ID_roles_b66222d0_fk_roles_ID_roles" FOREIGN KEY ("ID_roles") REFERENCES public.roles("ID_roles") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuarios_x_roles usuarios_x_roles_ID_usuarios_a0fd5f7b_fk_usuarios_ID_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios_x_roles
    ADD CONSTRAINT "usuarios_x_roles_ID_usuarios_a0fd5f7b_fk_usuarios_ID_usuarios" FOREIGN KEY ("ID_usuarios") REFERENCES public.usuarios("ID_usuarios") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ventas ventas_ID_metodos_fd57bd27_fk_metodos_pago_ID_metodos; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT "ventas_ID_metodos_fd57bd27_fk_metodos_pago_ID_metodos" FOREIGN KEY ("ID_metodos") REFERENCES public.metodos_pago("ID_metodos") DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict PEQeSaC71AHI5mX7jOo9w8rATUbkLxN7PqmxqLUgVUGPkCrH1JkSszQ6pVKgdAh

