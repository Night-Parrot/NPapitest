/*
 Navicat Premium Data Transfer

 Source Server         : 集约化稳定环境
 Source Server Type    : PostgreSQL
 Source Server Version : 90604
 Source Host           : 172.18.17.116:6543
 Source Catalog        : apitesting_dev
 Source Schema         : db_apitesting

 Target Server Type    : PostgreSQL
 Target Server Version : 90604
 File Encoding         : 65001

 Date: 19/04/2020 16:27:20
*/


-- ----------------------------
-- Table structure for c_at_tc
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."c_at_tc";
CREATE TABLE "db_apitesting"."c_at_tc" (
  "c_id" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_name" varchar(255) COLLATE "pg_catalog"."default",
  "c_text" varchar(1000) COLLATE "pg_catalog"."default",
  "dt_tjsj" timestamp(6),
  "c_fkxx" varchar(1000) COLLATE "pg_catalog"."default",
  "c_fkzt" varchar(255) COLLATE "pg_catalog"."default",
  "dt_fksj" timestamp(6)
)
;
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."c_id" IS '主键编号';
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."c_name" IS '提交人姓名';
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."c_text" IS '吐槽内容';
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."dt_tjsj" IS '提交时间';
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."c_fkxx" IS '反馈信息';
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."c_fkzt" IS '反馈状态，0待处理，1处理中，2已处理';
COMMENT ON COLUMN "db_apitesting"."c_at_tc"."dt_fksj" IS '反馈时间';

-- ----------------------------
-- Table structure for t_at_ci
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_ci";
CREATE TABLE "db_apitesting"."t_at_ci" (
  "c_bh" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "c_api" varchar(500) COLLATE "pg_catalog"."default",
  "c_yl_list" varchar(20000) COLLATE "pg_catalog"."default",
  "dt_zxdysj" timestamp(6),
  "c_zxcs" int4,
  "c_bh_xm" varchar(255) COLLATE "pg_catalog"."default",
  "c_ylsl" varchar(255) COLLATE "pg_catalog"."default",
  "dt_cjsj" timestamp(6)
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."c_bh" IS 'CI集成编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."c_api" IS '接口地址';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."c_yl_list" IS '关联用例';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."dt_zxdysj" IS '最新调用时间';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."c_zxcs" IS '执行次数';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."c_bh_xm" IS '项目编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."c_ylsl" IS '用例数量';
COMMENT ON COLUMN "db_apitesting"."t_at_ci"."dt_cjsj" IS '创建时间';

-- ----------------------------
-- Table structure for t_at_org
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_org";
CREATE TABLE "db_apitesting"."t_at_org" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_mc" varchar(255) COLLATE "pg_catalog"."default",
  "c_pid" varchar(32) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_org"."c_bh" IS '项目组id';
COMMENT ON COLUMN "db_apitesting"."t_at_org"."c_mc" IS '项目组名称';
COMMENT ON COLUMN "db_apitesting"."t_at_org"."c_pid" IS '上级id';

-- ----------------------------
-- Table structure for t_at_qqxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_qqxx";
CREATE TABLE "db_apitesting"."t_at_qqxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_zx" varchar(32) COLLATE "pg_catalog"."default",
  "n_xh" int4,
  "n_qqmc" varchar(255) COLLATE "pg_catalog"."default",
  "c_qqdz" varchar(255) COLLATE "pg_catalog"."default",
  "c_xysj" varchar(255) COLLATE "pg_catalog"."default",
  "dt_zxsj" timestamp(6),
  "n_jkzt" varchar(255) COLLATE "pg_catalog"."default",
  "c_yzjg" varchar(255) COLLATE "pg_catalog"."default",
  "c_qqcs" varchar(20000) COLLATE "pg_catalog"."default",
  "c_yqfhz" varchar(20000) COLLATE "pg_catalog"."default",
  "c_sjfhz" varchar(20000) COLLATE "pg_catalog"."default",
  "c_bh_yl" varchar(32) COLLATE "pg_catalog"."default",
  "c_xylx" varchar(255) COLLATE "pg_catalog"."default",
  "c_matchinfo" varchar(200000) COLLATE "pg_catalog"."default",
  "c_ycxx" varchar(200000) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_bh" IS '请求编号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_bh_zx" IS '执行编号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."n_xh" IS '执行序号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."n_qqmc" IS '请求名称';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_qqdz" IS '请求地址';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_xysj" IS '响应时间';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."dt_zxsj" IS '执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."n_jkzt" IS '接口返回状态';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_yzjg" IS '验证结果';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_qqcs" IS '请求参数';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_yqfhz" IS '预期返回值';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_sjfhz" IS '实际返回值';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_bh_yl" IS '用例编号';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_xylx" IS '协议类型';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_matchinfo" IS '校验信息';
COMMENT ON COLUMN "db_apitesting"."t_at_qqxx"."c_ycxx" IS '当用例执行过程中出现异常时，保存异常信息';

-- ----------------------------
-- Table structure for t_at_xmxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_xmxx";
CREATE TABLE "db_apitesting"."t_at_xmxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_xmmc" varchar(300) COLLATE "pg_catalog"."default",
  "c_url" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "dt_zxscsj" timestamp(6),
  "dt_zxzxsj" timestamp(6),
  "c_zxtgl" numeric(7,2),
  "c_zxfgl" numeric(7,2),
  "c_code_team" varchar(255) COLLATE "pg_catalog"."default",
  "c_test_team" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_bh" IS '项目编号';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_xmmc" IS '项目名称';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_url" IS '项目根地址';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."dt_zxscsj" IS '最新上传时间';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."dt_zxzxsj" IS '最新执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_zxtgl" IS '最新通过率';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_zxfgl" IS '最新覆盖率';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_code_team" IS '研发团队编号';
COMMENT ON COLUMN "db_apitesting"."t_at_xmxx"."c_test_team" IS '测试团队编号';

-- ----------------------------
-- Table structure for t_at_ylxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_ylxx";
CREATE TABLE "db_apitesting"."t_at_ylxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_xm" varchar(32) COLLATE "pg_catalog"."default",
  "c_ylmc" varchar(255) COLLATE "pg_catalog"."default",
  "dt_scsj" timestamp(6),
  "dt_zxzxsj" timestamp(6),
  "n_zxcs" int4,
  "c_bclj" varchar(500) COLLATE "pg_catalog"."default",
  "c_edit_key" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_sfbj" varchar(255) COLLATE "pg_catalog"."default",
  "c_api_count" varchar(500) COLLATE "pg_catalog"."default",
  "dt_gxsj" timestamp(6),
  "c_code_team" varchar(255) COLLATE "pg_catalog"."default",
  "c_test_team" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_bh" IS '用例编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_bh_xm" IS '项目编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_ylmc" IS '用例名称';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."dt_scsj" IS '上传时间';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."dt_zxzxsj" IS '最新执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."n_zxcs" IS '执行次数';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_bclj" IS '保存路径';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_edit_key" IS '编辑识别码';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_sfbj" IS '是否正在编辑：1是2否';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_api_count" IS 'swagger地址或接口的总数';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."dt_gxsj" IS '更新时间';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_code_team" IS '研发团队编号';
COMMENT ON COLUMN "db_apitesting"."t_at_ylxx"."c_test_team" IS '测试团队编号';

-- ----------------------------
-- Table structure for t_at_zxcs
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_zxcs";
CREATE TABLE "db_apitesting"."t_at_zxcs" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_yl" varchar(32) COLLATE "pg_catalog"."default",
  "c_key" varchar(255) COLLATE "pg_catalog"."default",
  "c_value" varchar(5000) COLLATE "pg_catalog"."default",
  "n_xh" int4
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_bh" IS '执行参数的主键';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_bh_yl" IS '执行参数所属用例的编号';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_key" IS '执行参数的名称';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."c_value" IS '执行参数的内容';
COMMENT ON COLUMN "db_apitesting"."t_at_zxcs"."n_xh" IS '参数的序号，用来展示时排序的';

-- ----------------------------
-- Table structure for t_at_zxxx
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_at_zxxx";
CREATE TABLE "db_apitesting"."t_at_zxxx" (
  "c_bh" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_bh_yl" varchar(32) COLLATE "pg_catalog"."default",
  "dt_zxsj" timestamp(6),
  "c_fgl" varchar(255) COLLATE "pg_catalog"."default",
  "c_cgl" varchar(255) COLLATE "pg_catalog"."default",
  "c_tgl" varchar(255) COLLATE "pg_catalog"."default",
  "n_zt" varchar(255) COLLATE "pg_catalog"."default",
  "c_cg" varchar(8) COLLATE "pg_catalog"."default",
  "c_wcg" varchar(8) COLLATE "pg_catalog"."default",
  "c_tg" varchar(8) COLLATE "pg_catalog"."default",
  "c_wtg" varchar(8) COLLATE "pg_catalog"."default",
  "c_jd" numeric,
  "c_sfci" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_bh" IS '执行编号';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_bh_yl" IS '用例编号';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."dt_zxsj" IS '执行时间';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_fgl" IS '覆盖率';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_cgl" IS '成功率';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_tgl" IS '通过率';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."n_zt" IS '执行状态（0：正在执行，1：已完成，2：异常中断）';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_cg" IS '成功数';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_wcg" IS '未成功数';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_tg" IS '通过数';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_wtg" IS '未通过数';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_jd" IS '进度';
COMMENT ON COLUMN "db_apitesting"."t_at_zxxx"."c_sfci" IS '是否CI调用，0是CI调用，1是正常执行，2是定时任务';

-- ----------------------------
-- Table structure for t_zx_user
-- ----------------------------
DROP TABLE IF EXISTS "db_apitesting"."t_zx_user";
CREATE TABLE "db_apitesting"."t_zx_user" (
  "c_id" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "c_username" varchar(255) COLLATE "pg_catalog"."default",
  "c_password" varchar(255) COLLATE "pg_catalog"."default",
  "c_name" varchar(255) COLLATE "pg_catalog"."default",
  "c_xmxx" text COLLATE "pg_catalog"."default",
  "dt_zhdlsj" timestamp(6)
)
;
COMMENT ON COLUMN "db_apitesting"."t_zx_user"."c_id" IS '用户主键';
COMMENT ON COLUMN "db_apitesting"."t_zx_user"."c_username" IS '用户名';
COMMENT ON COLUMN "db_apitesting"."t_zx_user"."c_password" IS '用户密码';
COMMENT ON COLUMN "db_apitesting"."t_zx_user"."c_name" IS '用户姓名';
COMMENT ON COLUMN "db_apitesting"."t_zx_user"."c_xmxx" IS '参与项目';
COMMENT ON COLUMN "db_apitesting"."t_zx_user"."dt_zhdlsj" IS '最后登录时间';

-- ----------------------------
-- Primary Key structure for table t_at_ci
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_ci" ADD CONSTRAINT "t_at_ci_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_org
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_org" ADD CONSTRAINT "t_at_org_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_qqxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_qqxx" ADD CONSTRAINT "t_at_qqxx_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_xmxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_xmxx" ADD CONSTRAINT "t_at_xmxx_pkey" PRIMARY KEY ("c_bh", "c_url");

-- ----------------------------
-- Primary Key structure for table t_at_ylxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_ylxx" ADD CONSTRAINT "t_at_ylxx_pkey" PRIMARY KEY ("c_bh", "c_edit_key");

-- ----------------------------
-- Primary Key structure for table t_at_zxcs
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_zxcs" ADD CONSTRAINT "t_at_zxcs_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_at_zxxx
-- ----------------------------
ALTER TABLE "db_apitesting"."t_at_zxxx" ADD CONSTRAINT "t_at_zxxx_pkey" PRIMARY KEY ("c_bh");

-- ----------------------------
-- Primary Key structure for table t_zx_user
-- ----------------------------
ALTER TABLE "db_apitesting"."t_zx_user" ADD CONSTRAINT "t_zx_user_pkey" PRIMARY KEY ("c_id");
