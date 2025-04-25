#coding: utf-8

import re
import os 


# get the head(part) of the given src string，return a head list 
def geth(head, src):
    hlist = []
    ptstr = '(\n\n'+head+'\s)(.*)(\n\n)'
    pth = re.compile(ptstr)
    result = re.findall(pth, src)
    for r in result:
        hlist.append(r[1])
    return hlist

'''
get head-simple, just keep the charachter, and 
replace the space to '-', uppercase to lowercase.
'''
def gethsmp(head):
    r1 = re.sub('[^a-zA-Z\s\-\d]', ' ', head).strip().lower()
    r2 = re.sub('\s+', ' ', r1)
    hsmp = re.sub('\s', '-', r2)
    return hsmp

# Read the source markdown string from the markdown file 
def getcontent(srcfile):
    fin = open(srcfile, 'r')
    mdstr = fin.read()
    return mdstr

# Split markdown string by the given head
def splitmd(src, head):
    # 定义分隔符: 匹配对应标题
    ptstr = '(\n\n'+head+'\s.*\n\n)'
    pt = re.compile(ptstr)
    # 以模式 pt 对 src 字符串进行匹配与分割
    mdlist = re.split(pt, src)
    return mdlist


# get the content, exclude the head title
def getmd(mdlist):  
    md = []
    for i in range(len(mdlist)):
        if (i!=0) and (i%2 == 0):
            md.append(mdlist[i])
    return md


def getmdroot(mdlist, subhead):
    mdroot = []
    for md in mdlist:
        mdtmp = splitmd(md, subhead)
        mdroot.append(mdtmp[0])
    return mdroot

def clearfn(src):
    p = re.compile(r'\* \* \*\n\n1')
    flag = re.search(p, src)
    if flag == None:
        return src
    else:
        pagelist = re.split(p, src)
        return pagelist[0]

# get the chapter's foot notes 
def getfn(src):
    p = re.compile(r'\* \* \*\n\n1')
    flag = re.search(p, src)
    if flag == None:
        return []
    else:
        fn = []
        pagelist = re.split(p, src)  
        note = '1' + pagelist[1]      
        fn.append(note)
        return fn 

# change the foot notes to fn dict 
def getnotes(fn):
    notedict = {}
    if len(fn) > 0:
        src = fn[0]
        p = re.compile(r'(\d+)\.  ([^↩]*)\[↩\]')
        notelist = re.findall(p, src)
        for note in notelist:
            k = note[0]
            v = note[1]
            notedict[k] = v
    return notedict


def getmdfn(cmd):
    fnlist = []
    mdlist = []
    for md in cmd:
        fn = getfn(md)
        notedict = getnotes(fn)
        fnlist.append(notedict)
    for md in cmd:
        newmd = clearfn(md)
        mdlist.append(newmd)
    return mdlist, fnlist


def getfirst(srcfile):
    h1 = '#'
    h2 = '##'
    mdstr = getcontent(srcfile)
    hlist1 = geth(h1, mdstr)
    mdlist1 = splitmd(mdstr, h1)
    md = getmd(mdlist1)               # not include h1 head(title)
    # cmd = pchapter(md)
    md1, fnlist = getmdfn(md)
    mdroot1 = getmdroot(md1, h2)       # save the root content of h1 level
    # print(md1[1])
    # print(len(md1))           # len(md1) == 43
    # print(hlist1)
    # print(len(hlist1))
    # print(mdlist1[3])
    # print(len(mdroot1))
    # print(mdroot1[1])
    return hlist1, md1, mdroot1, fnlist


def getsecond(md1):
    h2 = '##'
    h3 = '###'
    hlist2 = []
    md2 = []
    mdroot2 = []

    for i in range(len(md1)):
        head2 = geth(h2, md1[i])
        hlist2.append(head2)
        tmpmd = splitmd(md1[i], h2)
        md2.append(tmpmd)

    for md in md2:         # md2[0] is a list, but for...in behaves a string (by using md2[0][0] ?).
        if checklist(md):
            tmproot = []
            md2list = getmd(md)
            for md in md2list:
                tmproot.append(splitmd(md, h3)[0])
            mdroot2.append(tmproot)
            # print(md2list)
        else:
            mdroot2.append([''])

    # print(len(hlist2))        # len(hlist2) == 43
    # print(hlist2)

    # print(len(md2))           # len(md2) == 43
    # print(len(md2[0]))
    # print(md2[1])
    # print(type(md2[0]))
    # print(md2[1][0])
    # print(md2[1][1])
    # print(md2[2][1])
    # print(md2[3][12])
    # print(type(md2[1]))

    # print(len(mdroot2))       # len(mdroot2) == 43

    # print(checklist(md2[0]))

    # print(md2[0])

    # print(len(hlist2s))

    # print(md2[1][0])

    # print(len(splitmd(md2[3][12], '###')))

    # print(splitmd(md2[3][12], '###')[1])

    # print(len(mdroot2))
    # print(len(mdroot2[2]))
    # print(mdroot2[1][0])

    # print(mdroot2[0])
    # print(mdroot2[41])

    return hlist2, md2, mdroot2


def getmdpre(mdlist):
    mdpre = []
    for md in mdlist:
        if len(md)==1:
            mdpre.append([])
        else:
            mdpre.append(getmd(md))
    return mdpre

def getthird(md2):
    h3 = '###'
    h4 = '####'
    hlist3 = []
    mdroot3 = []
    md3 = []
    md3pre =  getmdpre(md2)

    # print(len(md3pre))
    # print(len(md3pre[0]))
    # print(md3pre[3][0])
    # print(md3pre[0])

    # print(md3pre[1][6])

    for md in md3pre:
        if len(md)==0:
            hlist3.append([])
            md3.append([])
            mdroot3.append([])
        else:
            t3 = []
            t3smp = []
            r3 = []
            root3 = []
            for e in md:
                h3t = geth(h3, e)
                t3.append(h3t)
                sp3 = splitmd(e, h3)
                if len(sp3)>1:
                    md3list = getmd(sp3)
                    r3.append(md3list)
                    tmproot = []
                    for mdl in md3list:
                        md4list = splitmd(mdl, h4)
                        tmproot.append(md4list[0])
                    root3.append(tmproot)
                else:
                    r3.append([])
                    root3.append([])
            hlist3.append(t3)
            md3.append(r3)
            mdroot3.append(root3)
    # print(len(hlist3))       # len(hlist3) == 43
    # print(hlist3[1])            # len(hsmp3) == 43
    # print(len(md3))      # len(md3) == 43
    # print(md3[1])
    # print(len(mdroot3[25][1]))
    # print(mdroot3[25][1][2])
    # print(mdroot3[1])
    return hlist3, md3, mdroot3


def getfourth(md3):
    h4 = '####'
    hlist4 = []
    mdroot4 = []
    lenmd3 = len(md3)
    # print(lenmd3)
    # print(md3[1])
    # print(len(md3[5][1]))
    # print(md3[5][1])
    for i in range(lenmd3):
        md31 = md3[i]
        lenmd31 = len(md31)
    for md41 in md3:
        lenmd41 = len(md41)
        hlist41 = []
        mdroot41 = []
        if lenmd41 == 0:
            hlist4.append(hlist41)
            mdroot4.append(mdroot41)
        else:
            for md42 in md41:
                lenmd42 = len(md42)
                # print('lenmd42: ',lenmd42)
                mdroot42 = []
                hlist42 = []
                if lenmd42 == 0:
                    hlist42.append([])
                    mdroot42.append([])
                else:
                    for md43 in md42:
                        h4tmp = geth(h4, md43)
                        hlist42.append(h4tmp)
                        # hlist41.append(hlist42)
                        mdlist4 = splitmd(md43 ,h4)
                        lenmdlist4 = len(mdlist4)
                        if lenmdlist4 == 1:
                            mdroot42.append([])
                        else:
                            roo4tmp = splitmd(md43, h4)
                            root4 = getmd(roo4tmp)
                            mdroot42.append(root4)
                hlist41.append(hlist42)
                mdroot41.append(mdroot42)
            hlist4.append(hlist41)
            mdroot4.append(mdroot41)
    # print(len(hlist4[5]))
    # print(hlist4[5])
    # print(len(mdroot4[5]))
    # print(mdroot4[5])
    return hlist4, mdroot4

def buildlist4(hlist4, mdroot4):
    list4 = []
    for i in range(len(hlist4)):
        h4i = hlist4[i]
        lenh4i = len(h4i)
        if lenh4i == 0:
            list4.append([])
        else:
            h4tmp1 = []
            for j in range(lenh4i):
                h4j = h4i[j]
                lenh4j = len(h4j)
                if lenh4j==0:
                    h4tmp1.append([])
                else:
                    h4tmp2 = []
                    for k in range(lenh4j):
                        # if i ==5:
                        # 	print('lenh4i:',lenh4i)
                        # 	print('i:'+str(i)+' j:'+str(j)+' k:'+str(k))
                        h4tmp3 = h4j[k]
                        lenh4tmp3 = len(h4tmp3)
                        if lenh4tmp3 == 0:
                            h4tmp2.append([])
                        else:
                            h4tmp4 = []
                            for m in range(lenh4tmp3):
                                h4tmp5 = []
                                h4tmp5.append(h4tmp3[m])
                                h4tmp5.append(mdroot4[i][j][k][m])
                                h4tmp4.append(h4tmp5)
                            h4tmp2.append(h4tmp4)
                    h4tmp1.append(h4tmp2)
            list4.append(h4tmp1)
    # print(len(list4))
    # print(len(list4[5]))
    # print(list4[5])
    return list4


def buildlist3(list4, hlist3, mdroot3):
    list3 = []
    # print(mdroot3[1])
    for i in range(len(hlist3)):
        if len(hlist3[i]) == 0 :
            list3.append([])
            # print('i:',i)
        else:
            sub3 = hlist3[i]
            st3 = []
            # print('i:',i)
            for j in range(len(sub3)):
                # print('j:',j)
                if len(sub3[j]) == 0:
                    st3.append([])
                else:
                    j3 = sub3[j]
                    st4 = []
                    for k in range(len(j3)):
                        # print('k:',k)
                        st5 = []
                        st5.append(j3[k])
                        st5.append(mdroot3[i][j][k])
                        # print('i:',i)
                        # print('j:',j)
                        # print('k:',k)
                        h4tmp = list4[i][j][k]
                        lenh4tmp = len(h4tmp)
                        st6 = []
                        if lenh4tmp > 0:
                            for m in range(lenh4tmp):
                                st7 = list4[i][j][k][m]
                                st6.append(st7)
                        st5.append(st6)
                        st4.append(st5)
                    st3.append(st4)
            list3.append(st3)
    # print(len(hlist3))
    # print(hlist3)
    # print(len(list3))
    # print(list3[1])
    return list3


def buildlist2(list3, hlist2, mdroot2):
    list2 = []
    for i in range(len(hlist2)):
        if len(hlist2[i]) == 0 :
            list2.append([])
        else:
            sub2 = hlist2[i]
            st2 = []
            for j in range(len(sub2)):
                st23 = []
                st23.append(sub2[j])
                st23.append(mdroot2[i][j])
                st23.append(list3[i][j])
                st2.append(st23)
            list2.append(st2)
    # print(len(list2))
    # print(list2[0])
    # print(list2[1][0])
    # print(list2[42][1][2][1])
    return list2


def buildlist1(list2, hlist1, mdroot1):
    list1 = []
    for i in range(len(hlist1)):
        st1 = []
        st1.append(hlist1[i])
        st1.append(mdroot1[i])
        st1.append(list2[i])
        list1.append(st1)
    # print(len(list1))
    # print(list1[0])
    return list1


# [
# 	[h1, h1root, [[h2, h2root, [[h3, h3root, h3ct], [h3, h3root, h3ct]]], [h2, h2root, [[h3, h3root, h3ct], [h3, h3root, h3ct]]]]],
# 	[h1, h1root, [[h2, h2root, [[h3, h3root, h3ct], [h3, h3root, h3ct]]], [h2, h2root, [[h3, h3root, h3ct], [h3, h3root, h3ct]]]]]
# ]
def buildlist(hlist1, mdroot1, hlist2, mdroot2, hlist3, mdroot3, hlist4, mdroot4):
    list4 = buildlist4(hlist4, mdroot4)
    # print(list4[5][4])
    list3 = buildlist3(list4, hlist3, mdroot3)
    list2 = buildlist2(list3, hlist2, mdroot2)
    list1 = buildlist1(list2, hlist1, mdroot1)
    return list1


# Buid book list tree from the source markdown file
def booktree(srcfile, outputdir):
    booklist = []
    hlist = []
    hlist1, md1, mdroot1, fnlist = getfirst(srcfile)
    hlist2, md2, mdroot2 = getsecond(md1)
    hlist3, md3, mdroot3 = getthird(md2)
    hlist4, mdroot4 = getfourth(md3)
    hlist.append(hlist1)
    hlist.append(hlist2)
    hlist.append(hlist3)
    hlist.append(hlist4)
    booklist = buildlist(hlist1, mdroot1, hlist2, mdroot2, hlist3, mdroot3, hlist4, mdroot4)
    return hlist, booklist, fnlist


def checklist(ele):
    return isinstance(ele, list)

def formath1(id, h1):
    return '{:02d}-'.format(id) + gethsmp(h1)


# Create the readme file 
def creadme(outputdir):
    rm = 'README.md'
    fout = open(outputdir + rm, 'w')
    fline = 'This is README file.\n\n'
    fout.write(fline)
    fout.close()

# Create the summary file 
def csummary(outputdir):
    sm = 'SUMMARY.md'
    fline = '# Summary\n\n* [Readme](README.md)\n'
    fout = open(outputdir + sm, 'w')
    fout.write(fline)
    fout.close()

def cassets(outputdir):
    ast = 'assets'
    os.mkdir(outputdir + ast)

# Add one line to file 'SUMMARY.md'
def addline(outputdir, line):
    sm = 'SUMMARY.md'
    fout = open(outputdir + sm, 'a')
    fout.write(line)
    fout.close()


def buildline(level, name, path):
    tab = '\t'
    s = '* '
    return (level-1)*tab+s+'['+name+']'+'('+path+'.md'+')'+'\n'


def cfile(name, fstr, outputdir):
    fname = name + '.md'
    fout = open(outputdir + fname, 'w')
    fout.write(fstr)
    fout.close()

def cdir(name, outputdir):
    os.mkdir(outputdir + name)

def subref(matched):
    num = matched.group(1)
    substr = '[^' + num + ']'
    return substr

def pref(s):
    p = re.compile(r'\[(\d+)\]\((#calibre_link-\d+)\)')
    substr = p.sub(subref, s)
    return substr



# get foot note ref number list of the sub-page 
# s='object.[1](#calibre_link-78) You  object.[2](#calibre_link-88) You '
# rflist = ['1', '2']
def getref(src):
    rflist = []
    p = re.compile(r'\[(\d+)\]\(#calibre_link-\d+\)')
    flag = re.search(p, src)
    if flag != None:
        rflist = re.findall(p, src)
    return rflist


# <b id="fn_1">1. </b> Footnote content here. [↩](#reffn_1)
def buildnote(k, v):
    return '<b id="fn_' + k +'">' + k + '. </b> ' + v + '[↩](#reffn_' + k + ')\n\n'


def proot(roottmp, index, fnlist):
    rflist = getref(roottmp)
    if len(rflist) > 0:
        ws = '\n\n---\n\n'
        rmd = pref(roottmp) + ws
        rootnew = rmd
        for rf in rflist:
            d = fnlist[index]
            v = d[rf]
            rootnew = rootnew + buildnote(rf, v)
        return rootnew
    else:
        return roottmp


def exlist(hlist, booklist, outputdir, fnlist):
    p1 = '# '
    p2 = '## '
    p3 = '### '
    p4 = '#### '
    sp = '/'
    br = '\n'
    br2 = '\n\n'
    ChapLink.hlist = hlist

    for i in range(len(booklist)):
        bk1 = booklist[i]
        h1 = bk1[0]
        h1roottmp = bk1[1]
        chstr1 = proot(h1roottmp, i, fnlist)
        h1root = ChapLink.pclink(chstr1)
        h1smp = formath1(i, h1)
        # h1smp = gethsmp(h1)
        h1str = p1 + h1 + br2 + h1root + br
        cfile(h1smp, h1str, outputdir)
        line1 = buildline(1, h1, h1smp)
        addline(outputdir, line1)
        list2 = bk1[2]
        if len(list2)>0:
            cdir(h1smp, outputdir)
            dir1 = outputdir + h1smp + sp
            for j in range(len(list2)):
                bk2 = list2[j]
                h2 = bk2[0]
                h2roottmp = bk2[1]
                chstr2 = proot(h2roottmp, i, fnlist)
                h2root = ChapLink.pclink(chstr2)
                h2smp = gethsmp(h2)
                h2str = p2 + h2 + br2 + h2root + br
                cfile(h2smp, h2str, dir1)
                path1 = h1smp + sp + h2smp
                line2 = buildline(2, h2, path1)
                addline(outputdir, line2)
                list3 = bk2[2]
                if len(list3)>0:
                    cdir(h2smp, dir1)
                    dir2 = dir1 + h2smp + sp
                    for k in range(len(list3)):
                        bk3 = list3[k]
                        h3 = bk3[0]
                        h3roottmp = bk3[1]
                        chstr3 = proot(h3roottmp, i, fnlist)
                        h3root = ChapLink.pclink(chstr3)
                        h3smp = gethsmp(h3)
                        h3str = p3 + h3 + br2 + h3root + br
                        cfile(h3smp, h3str, dir2)
                        path2 = path1 + sp + h3smp
                        line3 = buildline(3, h3, path2)
                        addline(outputdir, line3)
                        list4 = bk3[2]
                        if len(list4)>0:
                            cdir(h3smp, dir2)
                            dir3 = dir2 + h3smp + sp
                            for m in range(len(list4)):
                                bk4 = list4[m]
                                h4 = bk4[0]
                                h4roottmp = bk4[1]
                                chstr4 = proot(h4roottmp, i, fnlist)
                                h4root = ChapLink.pclink(chstr4)
                                h4smp = gethsmp(h4)
                                h4str = p4 + h4 + br2 + h4root + br
                                cfile(h4smp, h4str, dir3)
                                path3 = path2 + sp + h4smp
                                line4 = buildline(4, h4, path3)
                                addline(outputdir, line4)


def buildbook(srcfile, outputdir):
    hlist, booklist, fnlist =  booktree(srcfile, outputdir)
    # print(booklist[4])
    creadme(outputdir)
    csummary(outputdir)
    cassets(outputdir)
    exlist(hlist, booklist, outputdir, fnlist)


class ChapLink:
    hlist = []

    # get head-simple, just keep the charachter, and
    # replace the space to '-', uppercase to lowercase.
    @staticmethod
    def gethsmp(head):
        r1 = re.sub('[^a-zA-Z\s\-\d]', ' ', head).strip().lower()
        r2 = re.sub('\s+', ' ', r1)
        hsmp = re.sub('\s', '-', r2)
        return hsmp

    @staticmethod
    def formath1(id, h1):
        return '{:02d}-'.format(id) + ChapLink.gethsmp(h1)

    @staticmethod
    def pref(chapname):
        # print(chapname)
        hlist1 = ChapLink.hlist[0]
        hlist2 = ChapLink.hlist[1]
        hlist3 = ChapLink.hlist[2]
        hlist4 = ChapLink.hlist[3]

        len1 = len(hlist1)
        len2 = len(hlist2)
        len3 = len(hlist3)
        len4 = len(hlist4)

        for i in range(len1):
            h1 = hlist1[i]
            h1smp = ChapLink.formath1(i, h1)
            if h1 == chapname:
                return h1smp

        for i in range(len2):
            h1 = hlist1[i]
            h2i = hlist2[i]
            len2i = len(h2i)
            if len2i > 0:
                for j in range(len2i):
                    h2j = h2i[j]
                    if h2j == chapname:
                        h1smp = ChapLink.formath1(i, h1)
                        h2smp = ChapLink.gethsmp(h2j)
                        return h1smp+ '/' + h2smp

        for i in range(len3):
            h1 = hlist1[i]
            h3i = hlist3[i]
            len3i = len(h3i)
            if len3i > 0:
                for j in range(len3i):
                    h3j = h3i[j]
                    len3j = len(h3j)
                    if len3j > 0:
                        for k in range(len3j):
                            h3k = h3j[k]
                            if h3k == chapname:
                                h1smp = ChapLink.formath1(i, h1)
                                h2smp = ChapLink.gethsmp(hlist2[i][j])
                                h3smp = ChapLink.gethsmp(h3k)
                                return h1smp+ '/' + h2smp + '/' + h3smp

        for i in range(len4):
            h1 = hlist1[i]
            h4i = hlist4[i]
            len4i = len(h4i)
            if len4i > 0:
                for j in range(len4i):
                    h4j = h4i[j]
                    len4j = len(h4j)
                    if len4j > 0:
                        for k in range(len4j):
                            h4k = h4j[k]
                            len4k = len(h4k)
                            if len4k > 0:
                                for m in range(len4k):
                                    h4m = h4k[m]
                                    if h4m == chapname:
                                        h1smp = ChapLink.formath1(i, h1)
                                        h2smp = ChapLink.gethsmp(hlist2[i][j])
                                        h3smp = ChapLink.gethsmp(hlist3[i][j][k])
                                        h4smp = ChapLink.gethsmp(h4m)
                                        return h1smp+ '/' + h2smp + '/' + h3smp + '/' + h4smp
        # return ''

    # process the chapter calibre-link such as [Polymorphism](#calibre_link-64)
    @staticmethod
    def subchap(matched):
    #     print(matched.group(1))
        chapname = matched.group(1)
        tmp = '.md'
        pr = ChapLink.pref(chapname)
        linkname = '(/' + pr + tmp + ')'
        substr = '[' + matched.group(1) + ']' + linkname
        # print(substr)
        return substr

    # s = 'the [Polymorphism](#calibre_link-64) chapter).  the [aa-bb$cc](#calibre_link-55) chapter'
    @staticmethod
    def pclink(s):
        p = re.compile(r'\[([a-zA-Z][^\]\n]*)\]\((#calibre_link-\d+)\)')
        substr = p.sub(ChapLink.subchap, s)
        return substr


def main():
    basepath = "/Users/david/Desktop/"
    srcfile = basepath + "OnJava8TDMD.md"
    outputdir = basepath + "outputjava/"
    buildbook(srcfile, outputdir)


if __name__ == '__main__':
    main()

