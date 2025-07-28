/*
---------------------------------------------------------------------------
版權               :      上海菱通軟件技術有限公司
  系統名稱           :      Mitsubishi
模塊名稱           :      商品管理
文件代碼           :      MG0900S.vb
iSolution編號      :      ME15081001
創建人             :      Zy
創建日期           :      2015/10/13
---------------------------------------------------------------------------
*/
//本画面初始化的特别函数,被fInit()调用
function PageSpecialInit() {
    fInit();
}

//画面提交之前的檢查
function bPageChk() {
    Distinguish("");
    var bRtn;
    bRtn = false;

    switch (sSubmitCtl) {
        case ("LINKBUTTON"):
            bRtn = true;
            break;

        case ("cmdSearch"):
            bRtn = true;
            break;

        case ("cmdUp"):
            Distinguish("Up");
            bRtn = true;
            break;

        case ("cmdDown"):
            Distinguish("Down");
            bRtn = true;
            break;

        case ("txtPgIndex"):
            Distinguish("TextBox");
            bRtn = true;
            break;

        case ("cmdDelete"):

            if (doSelExist(RowCountStart, RowCountEnd) == false) {
                NormalErrMsgBox(EC9013_Err, EC9013_Type, "");
                bRtn = false;
                break;
            }

            if (NormalErrMsgBox(QC9001_Err, QC9001_Type, "") == false) {
                bRtn = false;
                break;
            }
            bRtn = true;
            break;

        case ("cmdDisUsing"):
            if (doSelExist(RowCountStart, RowCountEnd) == false) {
                NormalErrMsgBox(EC9052_Err, EC9052_Type, "");
                bRtn = false;
                break;
            }

            if (NormalErrMsgBox(QC9003_Err, QC9003_Type, "") == false) {
                bRtn = false;
                break;
            }

            bRtn = true;
            break;

        case ("cmdEnUsing"):
            if (doSelExist(RowCountStart, RowCountEnd) == false) {
                NormalErrMsgBox(EC9053_Err, EC9053_Type, "");
                bRtn = false;
                break;
            }

            if (NormalErrMsgBox(QC9004_Err, QC9004_Type, "") == false) {
                bRtn = false;
                break;
            }

            bRtn = true;
            break;



        case ("cmdInsert"):
            doMst('../Update/MG0900E.aspx');
            bRtn = false;
            break;
        default:
            bRtn = false;
            break;
    }

    if (bRtn) initAd();
    return bRtn;

}

//区分换頁类型是按BUTTON还是TEXTBOX
function Distinguish(sType) {
    const pageMoveType = document.getElementById("PageMoveType");
    if (!pageMoveType) return;
    pageMoveType.value = sType.toUpperCase();
}

function fillReturnInfo(POPWINDOW) {
    var tempinfo;
    var s = "";
    var arr;
    var oCtl;
    switch (POPWINDOW) {

        case (POPWINDOW_PRODUCT):

            const txtProdID = document.getElementById('txtProdID');
            s = escape(txtProdID.value) || null;
            tempinfo = popQuickWindow(s, POPWINDOW_PRODUCT)
            if (tempinfo[0].PRODID == "") { return false; }
            document.all.txtProdID.value = tempinfo[0].PRODID;
            document.all.lblProdNameCN.innerText = tempinfo[0].PRODNAMECN;
            break;

        case (POPWINDOW_COMPARISONPRODUCT):
            s = escape(document.all.txtComparisonProdID.value);
            tempinfo = popQuickWindow(s, POPWINDOW_PRODUCT)
            if (tempinfo[0].PRODID == "") { return false; }
            document.all.txtComparisonProdID.value = tempinfo[0].PRODID;
            document.all.lblComparisonProdNameCN.innerText = tempinfo[0].PRODNAMECN;
            break;


        default:
            break;
    }
    return false;
}

function checkComparisonProdID() {
    if ((event.keyCode == 13) || (event.keyCode == 9)) {
        //alert("enter checkpageinfo");
        var oCtl;
        var sLineNo;
        var sResult;
        oCtl = document.all.txtComparisonProdID;
        if (sTrim(oCtl.value) == "") {
            oCtl = document.all.lblComparisonProdNameCN;
            oCtl.innerText = ""
            event.keyCode = 9;
            return true;
        }
        sResult = checkProdInfo(escape(sTrim(oCtl.value)));
        if (sResult.PRODID == "") {
            //没有取到数据说明输入的产品代码不存在（不需要自己写报错信息）
            try {
                //清空原来的产品名稱等数据
                oCtl = document.all.lblComparisonProdNameCN;
                oCtl.innerText = "";
                oCtl = document.webForm.txtComparisonProdID;
                oCtl.value = "";
            } catch (e) {
            }
            event.returnValue = false;
            return false;
        } else {
            //开始将取到的产品名稱等数据填到画面控件中	

            oCtl = document.all.lblComparisonProdNameCN;
            oCtl.innerText = sResult.PRODNAMECN;
            oCtl = document.webForm.txtComparisonProdID;
            oCtl.value = sResult.PRODID;

        }
        event.keyCode = 9;
        return true;
    }
}

function checkProdID() {
    if ((event.keyCode == 13) || (event.keyCode == 9)) {
        //alert("enter checkpageinfo");
        var oCtl;
        var sLineNo;
        var sResult;
        oCtl = document.all.txtProdID;
        if (sTrim(oCtl.value) == "") {
            oCtl = document.all.lblProdNameCN;
            oCtl.innerText = ""
            event.keyCode = 9;
            return true;
        }
        sResult = checkProdInfo(escape(sTrim(oCtl.value)));
        if (sResult.PRODID == "") {
            //没有取到数据说明输入的产品代码不存在（不需要自己写报错信息）
            try {
                //清空原来的产品名稱等数据
                oCtl = document.all.lblProdNameCN;
                oCtl.innerText = "";
                oCtl = document.webForm.txtProdID;
                oCtl.value = "";
            } catch (e) {
            }
            event.returnValue = false;
            return false;
        } else {
            //开始将取到的产品名稱等数据填到画面控件中	

            oCtl = document.all.lblProdNameCN;
            oCtl.innerText = sResult.PRODNAMECN;
            oCtl = document.webForm.txtProdID;
            oCtl.value = sResult.PRODID;

        }
        event.keyCode = 9;
        return true;
    }
}